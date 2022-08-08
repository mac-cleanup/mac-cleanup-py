import toml
from pathlib import Path
from inquirer import Checkbox, prompt

config_name = "modules.toml"


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

    # Creates config if it's not already created
    Path(config_name).touch()

    # Loads config (in case something got wrong there is try -> except)
    try:
        config = toml.load(config_name)
    except toml.TomlDecodeError:
        config = dict()

    # Joins default and custom modules together
    all_modules = dict()
    all_modules.update(load_default())
    all_modules.update(load_custom(config.get("custom_path")))

    # If config is empty requestes configuration and selects all modules as enabled
    if config == dict():
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

    # Updates and write config
    config.update({"enabled": enabled})
    with open(config_name, 'w+') as f:
        toml.dump(config, f)

    # Loads all enabled modules
    [
        all_modules[module]()
        for module in enabled
        if not requested_configure
    ]


if __name__ == "__main__":
    load_config()
