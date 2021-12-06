import shutil
import subprocess

from .decorators import log
from .exceptions import ExecutableNotFoundError, ExecuteError, NoSuchPackageError

PACKAGE_PREFIX = "package:"


def execute(command):
    result = subprocess.run(command.split(), capture_output=True)
    if result.stderr:
        raise ExecuteError(result.stderr.decode("utf-8"))
    return result.stdout.decode("utf-8").strip()


@log("Checking ADB")
def check_adb():
    if shutil.which("adb") is None:
        raise ExecutableNotFoundError(
            'The "adb" executable was not found in PATH.\n'
            "Make sure you have Android SDK Platform-Tools installed."
        )


@log("Listing packages")
def get_packages():
    result = execute("adb shell pm list packages")
    return [line.replace(PACKAGE_PREFIX, "") for line in result.splitlines()]


@log("Finding package path")
def find_package_path(package):
    result = execute(f"adb shell pm path {package}")
    return result.replace(PACKAGE_PREFIX, "")


@log("Pulling from device")
def pull_path(path, out_path):
    return execute(f"adb pull {path} {out_path}")


@log("Finding package")
def verify_package_exists(package, packages):
    if package not in packages:
        raise NoSuchPackageError(f'Package "{package}" was not found!')
