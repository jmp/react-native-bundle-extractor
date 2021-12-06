class ExecuteError(RuntimeError):
    pass


class ExecutableNotFoundError(RuntimeError):
    pass


class NoSuchPackageError(RuntimeError):
    pass


class BundleNotFoundError(RuntimeError):
    pass
