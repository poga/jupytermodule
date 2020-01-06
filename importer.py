import sys
import types  # Used to instantiate a Module object, unavailable as a builtin
import os.path

# os.path.join is used frequently, so we shorten our invocation
from os.path import join as ospj


class TmpFinder(object):
    """ Class to find and load modules from `/tmp/modules/` """
    def __init__(self):
        self.greeting = 'Hello from TmpFinder'
        self.tmp_prefix = ospj('/tmp', 'modules')

    def find_module(self, fullname, path=None):
        # Adding print statements, so that (1) we know everytime find_module is
        # invoked during the import process and (2) we see what the name and
        # path of the module passed to us look like.
        print(fullname, path)

        # NOTE: For simplicity and brevity, we assume the module we're being
        # given is a top-level file module, not a directory based package or
        # sub-package. We also ignore `path`, doing so will break subpackage
        # imports and relative imports. Adding this functionality is easy
        # enough, but it detracts from the example, so we leave it out.
        location = ospj(self.tmp_prefix, *(fullname.split('.')))

        if os.path.exists(location):
            # We're returning the loader object here, which in this case, just
            # happens to be the same as the finder object
            return self

        # Default return for a function is None of course, so we do nothing
        # special when we don't find the module

    def load_module(self, fullname):
        # Helpful print statement tells us when loader is used

        # If the module already exists in `sys.modules` we *must* use that
        # module, it's a mandatory part of the importer protcol
        if fullname in sys.modules:
            # Do nothing, just return None. This likely breaks the idempotency
            # of import statements, but again, in the interest of being brief,
            # we skip this part.
            return

        location = ospj(self.tmp_prefix, *(fullname.split('.')))

        try:
            # The importer protocol requires the loader create a new module
            # object, set certain attributes on it, then add it to
            # `sys.modules` before executing the code inside the module (which
            # is when the "module" actually gets code inside it)

            m = types.ModuleType(fullname,
                                 'This is the doc string for the module')
            m.__file__ = '<tmp {}>'.format(location)
            m.__name__ = fullname
            m.__loader__ = self
            sys.modules[fullname] = m

            # Attempt to open the file, and exec the code therein within the
            # newly created module's namespace
            with open(location, 'r') as f:
                exec(f) in sys.modules[fullname].__dict__

            # Return our newly create module
            return m

        except Exception as e:
            # If it fails, we need to reset sys.modules to it's old state. This
            # is good practice in general, but also a mandatory part of the
            # spec, likely to keep the import statement idempotent and free of
            # side-effects across imports.

            # Delete the entry we might've created; use LBYL to avoid nested
            # exception handling
            if sys.modules.get(fullname):
                del sys.modules[fullname]
            raise e


sys.meta_path.append(TmpFinder())
