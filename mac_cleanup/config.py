import toml
from pathlib import Path
from inquirer import Checkbox, prompt
from rich.prompt import Prompt

config_path = Path(__file__).parent.resolve().as_posix() + "/modules.toml"


def config_checkbox(
        all_modules: list,
        enabled: list,
) -> list[str]:
    """
    Opens the checkbox list in the terminal to enable modules

    Args:
        all_modules: List w/ all modules
        enabled: List w/ all enabled modules
    Returns:
        List w/ all modules user selected
    """
    questions = Checkbox(
        "modules",
        message="Activated modules",
        choices=all_modules,
        default=enabled,
        carousel=True,
    )
    answers = prompt([questions])
    if not answers:
        raise KeyboardInterrupt
    return answers["modules"]


def set_custom_path(
) -> None:
    """
    Sets path for custom modules in config
    """
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


def get_config(
) -> dict:
    """
    Gets the config or creates it if it doesn't exist

    Returns:
        Config as a dict
    """
    # Creates config if it's not already created
    Path(config_path).touch()

    # Loads config (in case something got wrong there is try -> except)
    try:
        config = toml.load(config_path)
    except toml.TomlDecodeError:
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
    config.update(config)
    with open(config_path, 'w+') as f:
        toml.dump(config, f)


def load_config(
        configuration_needed: bool = False,
) -> None:
    """
    Loads & checks config and launches config_checkbox if needed

    Args:
        configuration_needed: Request configuration
    """
    from mac_cleanup.modules import load_default, load_custom

    requested_configure = configuration_needed

    config = get_config()

    # Joins default and custom modules together
    all_modules = dict()
    all_modules.update(load_default())
    all_modules.update(load_custom(config.get("custom_path")))

    # If config is empty requestes configuration and selects all modules as enabled
    if config == dict() or not config.get("enabled"):
        configuration_needed = True
        enabled = list(all_modules.keys())
    else:
        enabled = config.get("enabled", list())

    if configuration_needed:
        enabled = config_checkbox(
            all_modules=list(all_modules.keys()),
            enabled=enabled,
        )
    else:
        # Checks if enabled modules exists else removes 'em
        [
            enabled.remove(i)
            for i in enabled
            if not all_modules.get(i)
        ]

    # Sets enabled in config
    config.update({"enabled": enabled})
    set_config(config)

    # Loads all enabled modules
    [
        all_modules[module]()
        for module in enabled
        if not requested_configure
    ]


if __name__ == "__main__":
    load_config()
