"""Custom module template example."""

from mac_cleanup import *

# Do not import any functions at the top level

# Get an instance of Collector
clc = Collector()


# Module's name in configuration screen == function name
def module_example_1():
    # Import anything you need from utils here
    from mac_cleanup.utils import check_exists, cmd

    # check_exists - checks if specified path exists
    if check_exists("~/example/path"):
        # Open context manager of Collector
        with clc as unit:
            # message() - sets message to be displayed in the progress bar
            unit.message("Message you want to see in progress bar")

            # add() - adds desired module to modules list
            unit.add(
                # Path - used for deleting paths
                Path("~/example/path")
                # with_prompt - calls for user prompt to approve "risky" action
                # You can specify question in prompt with optional attr "message_"
                .with_prompt()
            )

            unit.add(
                Path("~/example/dry_run/file.webm")
                # dry_run_only - specified path will be counted in dry run, but won't be deleted
                .dry_run_only()
            )

            # cmd() - executes specified command and return stdout only
            # stderr can be returned with attr "ignore_errors" set to False
            if cmd("echo 1") == "1":
                unit.add(
                    # Command - used for executing any command with :func:`mac_cleanup.utils.cmd`
                    Command("whoami").with_prompt("You will see your username. Proceed?")
                    # with_errors - adds stderr to return of command execution
                    .with_errors()
                )


# You can create lots of modules in one file
def module_example_2():
    pass
