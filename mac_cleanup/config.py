"""Config handler."""

from inspect import getmembers, isfunction
from pathlib import Path
from typing import Callable, Final, Optional, TypedDict, final

from mac_cleanup import default_modules
from mac_cleanup.console import console


@final
class ConfigFile(TypedDict):
    """Config file structure."""

    enabled: list[str]
    custom_path: Optional[str]


@final
class Config:
    """
    Class for config initialization and validation.

    :param config_path_: Path to config location
    """

    def __init__(self, config_path_: Path):
        # Set config path
        self.__path: Final = config_path_

        # Set modules in the class
        self.__modules: dict[str, Callable[..., None]] = dict()

        # Load default modules
        self.__load_default()

        # Load config
        self.__config_data: Final[ConfigFile]

        try:
            self.__config_data = self.__read()
        except FileNotFoundError:
            console.print("[danger]Modules not configured, opening configuration screen...[/danger]")

            # Set config to empty dict
            # Why: self.configure will call dict.update
            self.__config_data = ConfigFile(enabled=list(), custom_path=None)

            # Launch configuration
            self.__configure(all_modules=list(self.__modules.keys()), enabled_modules=list())

        # Get custom modules path
        self.__custom_modules_path: Optional[str] = self.__config_data.get("custom_path")

        # Load custom modules
        self.__load_custom()

    def __call__(self, *, configuration_prompted: bool):
        """Checks config and launches additional configuration if needed."""

        # Configure and exit on prompt
        if configuration_prompted:
            # Configure modules
            self.__configure(
                all_modules=list(self.__modules.keys()), enabled_modules=self.__config_data.get("enabled", list[str]())
            )

            # Exit
            self.full_exit(failed=False)

        # If config doesn't have modules configuration - launch configuration
        if not self.__config_data.get("enabled"):
            # Notify user
            console.print("[danger]Modules not configured, opening configuration screen...[/danger]")

            # Configure modules
            self.__configure(all_modules=list(self.__modules.keys()), enabled_modules=list())

        # Create list with faulty modules
        remove_list: list[str] = list()

        # Invoke modules
        for module_name in self.__config_data["enabled"]:
            module = self.__modules.get(module_name)

            # Add faulty module to remove list - if modules wasn't found
            if not module:
                remove_list.append(module_name)
                continue

            # Call module
            module()

        # Pop faulty modules from module list
        for faulty_module in remove_list:
            self.__config_data["enabled"].remove(faulty_module)

        # Write updated config if faulty modules were found
        if remove_list:
            self.__write()

    def __read(self) -> ConfigFile:
        """Gets the config or creates it if it doesn't exist :return: Config as a dict."""

        from toml import TomlDecodeError, load

        # Creates config if it's not already created
        self.__path.parent.mkdir(exist_ok=True, parents=True)
        self.__path.touch(exist_ok=True)

        # Loads config
        # If something got wrong there is try -> except
        try:
            config = ConfigFile(**load(self.__path))
        except TomlDecodeError as err:
            raise FileNotFoundError from err
        return config

    def __write(self) -> None:
        """Updates and writes config as toml."""

        from toml import dump

        with open(self.__path, "w+") as f:
            dump(self.__config_data, f)

    @staticmethod
    def full_exit(failed: bool) -> None:
        """
        Gracefully exits from cleaner.

        :param failed: Status code of exit
        """

        console.print("Config saved, exiting...")
        exit(failed)

    def set_custom_path(self) -> None:
        """Sets path for custom modules in config."""

        from rich.prompt import Prompt

        # Ask for user input
        custom_path = Prompt.ask("Enter path to custom modules", default="~/Documents/mac-cleanup/", show_default=True)

        # Get temps path
        tmp_custom_path = Path(custom_path).expanduser()

        # Creates directory if it doesn't exist
        tmp_custom_path.mkdir(exist_ok=True, parents=True)

        # Changes custom_path in config
        self.__config_data["custom_path"] = tmp_custom_path.as_posix()

        # Update config
        self.__write()

        # Exit
        self.full_exit(failed=False)

    def __configure(self, *, all_modules: list[str], enabled_modules: list[str]) -> None:
        """
        Opens modules configuration screen.

        :param all_modules: List w/ all modules
        :param enabled_modules: List w/ all enabled modules
        :return: List w/ all modules user enabled
        """

        import inquirer  # pyright: ignore [reportMissingTypeStubs]

        from mac_cleanup.console import print_panel

        # Prints the legend
        print_panel(
            text="[success]Enable: [yellow][warning]<space>[/warning] | [warning]<--[/warning] | [warning]-->[/warning]"
            "\t[success]Confirm: [warning]<enter>[/warning]",
            title="[info]Controls",
        )

        questions = inquirer.Checkbox(  # pyright: ignore [reportUnknownMemberType]
            "modules", message="Active modules", choices=all_modules, default=enabled_modules, carousel=True
        )

        # Get user answers
        answers = inquirer.prompt(  # pyright: ignore [reportUnknownVariableType, reportUnknownMemberType]
            questions=[questions], raise_keyboard_interrupt=True
        )

        # Clear console after checkbox
        console.clear()

        if not answers or not answers["modules"]:
            console.print("Config cannot be empty. Enable some modules")

            return self.__configure(all_modules=all_modules, enabled_modules=enabled_modules)

        # Update config
        self.__config_data["enabled"] = answers["modules"]

        # Write new config
        self.__write()

    def __load_default(self) -> None:
        """Loads default modules."""

        self.__modules.update(dict(getmembers(object=default_modules, predicate=isfunction)))

    def __load_custom(self) -> None:
        """Loads custom modules and."""

        # Empty dict if no custom path
        if not self.__custom_modules_path:
            return

        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader
        from pathlib import Path

        tmp_modules: dict[str, Callable[..., None]] = dict()

        # Imports all modules from the given path
        for module in Path(self.__custom_modules_path).expanduser().rglob("*.py"):
            # Get filename
            filename = module.name.split(".py")[0]

            # Set module loader
            loader = SourceFileLoader(fullname=filename, path=module.as_posix())

            # Get module spec
            spec = spec_from_loader(loader.name, loader)

            # Check next file if spec is empty
            if spec is None:
                continue  # pragma: no cover # TODO: add test later

            # Get all modules from file
            modules = module_from_spec(spec)

            # Execute module
            loader.exec_module(modules)

            # Add modules to the list
            # Duplicates will be overwritten
            tmp_modules.update(dict(getmembers(object=modules, predicate=isfunction)))

        self.__modules.update(tmp_modules)

    @property
    def get_modules(self) -> dict[str, Callable[..., None]]:
        """Getter for private attr modules."""

        return self.__modules

    @property
    def get_config_data(self) -> ConfigFile:
        """Getter for private attr config data."""

        return self.__config_data

    @property
    def get_custom_path(self) -> Optional[str]:
        """Getter for private attr custom modules path."""

        return self.__custom_modules_path
