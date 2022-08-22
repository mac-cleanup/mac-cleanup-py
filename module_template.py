from mac_cleanup import *
# Do not import any functions at the top level

# Get an instance of Collector
t = Collector()


# Module's name in configuration screen == function name
def module_example_1():
    # Import anything you need from utils here
    from mac_cleanup.utils import check_exists, cmd

    if check_exists("~/example/path"):
        # .msg() is necessary in the start of module, adds new collection in execute_list
        # IF WASN'T CALLED - commands will be added in last module
        t.msg("Message you want to see in progress bar")

        # .collect() w/o arguments will delete path
        t.collect("~/example/path")

        # cmd() will execute the command and return the stdout & stderr
        if cmd("echo 1") == "1":
            # .collect() w/ command=True will execute command and return stdout & stderr
            t.collect("whoami",
                      command=True)

        # .collect() w/ dry=True will be counted in dry run but won't be deleted
        t.collect("~/example/dry_run/file.webm",
                  dry=True)


# You can create lots of modules in one file
def module_example_2():
    pass
