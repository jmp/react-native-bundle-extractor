import shutil
import subprocess

from .decorators import with_logging


class ExecutableNotFoundError(RuntimeError):
    pass


@with_logging('Checking ADB')
def check_adb():
    if shutil.which('adb') is None:
        raise ExecutableNotFoundError(
            'The "adb" executable was not found in PATH.\n'
            'Make sure you have Android SDK Platform-Tools installed.'
        )


@with_logging('Listing packages')
def get_packages():
    result = subprocess.run(
        'adb shell pm list packages'.split(),
        capture_output=True,
    )
    if result.stderr:
        raise RuntimeError(result.stderr.decode('utf-8'))
    lines = result.stdout.strip().splitlines()
    return [line.decode('utf-8').replace('package:', '') for line in lines]


@with_logging('Finding package path')
def find_package_path(package):
    result = subprocess.run(
        f'adb shell pm path {package}'.split(),
        capture_output=True,
        check=True,
    )
    return result.stdout.decode('utf-8').strip().replace('package:', '')


@with_logging('Pulling from device')
def pull_path(path, out_path):
    result = subprocess.run(
        f'adb pull {path} {out_path}'.split(),
        capture_output=True,
        check=True,
    )
    return result.stdout.decode('utf-8').strip()


@with_logging('Finding package')
def verify_package_exists(package, packages):
    if package not in packages:
        raise RuntimeError(f'Package "{package}" was not found on device!')


def pull_apk(package, out_path):
    packages = get_packages()
    verify_package_exists(package, packages)
    package_path = find_package_path(package)
    pull_path(package_path, out_path)
