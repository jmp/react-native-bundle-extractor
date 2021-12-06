class ExtractorError(RuntimeError):
    pass


class ExecuteError(ExtractorError):
    pass


class ExecutableNotFoundError(ExtractorError):
    pass


class PackageNotFoundError(ExtractorError):
    pass


class FileNotFoundInAPKError(ExtractorError):
    pass


class InvalidArgumentError(ExtractorError):
    pass
