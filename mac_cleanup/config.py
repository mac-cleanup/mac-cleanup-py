from typing import List, Dict  # Generics are fun
from pathlib import Path
from .utils import function

config_path = Path(__file__).parent.resolve().as_posix() + "/modules.toml"


def get_config(
) -> dict:
    """
    Gets the config or creates it if it doesn't exist

    Returns:
        Config as a dict
    """
    from toml import load, TomlDecodeError

    # Creates config if it's not already created
    Path(config_path).touch(exist_ok=True)

    # Loads config (in case something got wrong there is try -> except)
    try:
        config = load(config_path)
    except TomlDecodeError:
        config = dict()
    return config


def set_config(
        config: dict,
) -> None:
    """
    Updates and writes config

    Args:
        config: Config as a dict to be written
    """
    from toml import dump

    with open(config_path, "w+") as f:
        dump(config, f)


def config_checkbox(
        all_modules: list,
        enabled: list,
) -> List[str]:
    """
    Opens the checkbox list in the terminal to enable modules

    Args:
        all_modules: List w/ all modules
        enabled: List w/ all enabled modules
    Returns:
        List w/ all modules user selected
    """
    from inquirer import Checkbox, prompt
    from .console import print_panel, console

    # Prints the legend
    print_panel(
        text="[success]Enable: [yellow][warning]<space>[/warning] | [warning]<--[/warning] | [warning]-->[/warning]"
             "\t[success]Confirm: [warning]<enter>[/warning]",
        title="[info]Controls"
    )

    questions = Checkbox(
        "modules",
        message="Active modules",
        choices=all_modules,
        default=enabled,
        carousel=True,
    )
    answers: Dict[str, List[str]] = prompt([questions], raise_keyboard_interrupt=True)

    # Clear console after checkbox
    console.clear()
    if not answers:
        raise ValueError("Got empty answers from Checkbox")
    return answers["modules"]


def set_custom_path(
) -> None:
    """
    Sets path for custom modules in config
    """
    from rich.prompt import Prompt

    # Ask for user input
    custom_path = Prompt.ask(
        "Enter path to custom modules",
        default="~/Documents/mac-cleanup/",
        show_default=True,
    )

    # Creates directory if it doesn't exist
    Path(custom_path).expanduser().mkdir(exist_ok=True)

    # Changes custom_path in config
    config = get_config()
    config.update({"custom_path": Path(custom_path).expanduser().as_posix()})
    set_config(config)


def load_config(
        configuration_needed: bool = False,
) -> None:
    """
    Loads & checks config and launches config_checkbox if needed

    Args:
        configuration_needed: Request configuration
    """
    from .modules import load_default, load_custom

    config = get_config()

    # Joins default and custom modules together and sort 'em
    all_modules: Dict[str, function] = dict(  # type: ignore
        load_custom(config.get("custom_path")),
        **load_default(),
    )
    all_modules_keys = list(all_modules.keys())

    # If config is empty requestes configuration and selects all modules as enabled
    if config.get("enabled", 0) == 0 or not isinstance(config["enabled"], list):
        from .console import console

        console.print("[danger]Modules not configured, opening configuration screen...[/danger]")
        enabled = config_checkbox(
            all_modules=all_modules_keys,
            enabled=all_modules_keys,
        )
        configuration_needed = False
    else:
        enabled = config["enabled"]

    if configuration_needed:
        from .console import console

        enabled = config_checkbox(
            all_modules=all_modules_keys,
            enabled=enabled,
        )
        config.update({"enabled": enabled})
        set_config(config)
        console.print("Config saved, exiting...")
        exit(0)
    else:
        # Checks if enabled modules exists else removes 'em
        for i in enabled:
            if i not in all_modules:
                enabled.remove(i)

    # Sets enabled in config
    config.update({"enabled": enabled})
    set_config(config)

    # Loads all enabled modules
    [
        all_modules[module]()  # type: ignore
        for module in enabled
    ]


if __name__ == "__main__":
    load_config()
