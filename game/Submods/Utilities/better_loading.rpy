init -990 python in mas_submod_utils:
    bl_submod = Submod(
        author="multimokia",
        name="Better Loading",
        version="1.0.0",
        description=(
            "Modifies the internal renpy loader to load the same on UNIX systems as it does on Windows\n"
            "It also converts backslashes to forward slashes in filepaths automatically."
        )
    )

init -989 python in bl_utils:
    import store

    #Register the updater if needed
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod=store.mas_submod_utils.bl_submod,
            user_name="multimokia",
            repository_name="MAS-Util-Better-Loading",
            tag_formatter=tagparser,
            update_dir="",
            attachment_id=None,
        )

init -999 python in bl_utils:
    def tagparser(tag):
        """
        Tag formatter for GH tags

        IN:
            tag - raw tag to parse to clean
        """
        return tag[tag.index('_') + 1:]

python early:
    def bl_load(name, tl=True):
        """
        Base loader function
        """
        #Clear out the backslash here
        name = name.replace('\\', '/')

        name = renpy.re.sub(r'/+', '/', name)

        for p in renpy.loader.get_prefixes():
            rv = renpy.loader.load_core(p + name)
            if rv is not None:
                return rv

        raise IOError("Couldn't find file '%s'." % name)

    def bl_transfn(name):
        """
        Tries to translate the name to a file that exists in one of the
        searched directories.
        """
        #Clear out the backslash here
        name = name.replace('\\', '/')

        name = renpy.loader.lower_map.get(name.lower(), name)

        if isinstance(name, str):
            name = name.decode("utf-8")

        for d in renpy.config.searchpath:
            fn = os.path.join(renpy.config.basedir, d, name)

            renpy.loader.add_auto(fn)

            if os.path.exists(fn):
                return fn

        raise Exception("Couldn't find file '%s'." % name)

    def bl_loadable(name):
        """
        Checks if a file is loadable

        IN:
            name - name of the file to check

        OUT:
            boolean:
                True if loadable
                False otherwise
        """
        for p in renpy.loader.get_prefixes():
            if renpy.loader.loadable_core(p + name):
                return True
        return False

    renpy.loader.load = bl_load
    renpy.loader.transfn = bl_transfn
    renpy.loader.loadable = bl_loadable
