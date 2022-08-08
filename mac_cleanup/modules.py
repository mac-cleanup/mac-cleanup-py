def load_default() -> None:
    import mac_cleanup.default_modules as default_modules
    from inspect import getmembers, isfunction

    all_default = getmembers(default_modules, isfunction)

    for module, function in all_default:
        if True:
            function()
