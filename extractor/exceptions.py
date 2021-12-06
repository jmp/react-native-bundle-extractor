class ExtractorError(RuntimeError):
    pass


class ExecuteError(ExtractorError):
    pass


class ExecutableNotFoundError(ExtractorError):
    pass


class PackageNotFoundError(ExtractorError):
    pass


class BundleNotFoundError(ExtractorError):
    pass
