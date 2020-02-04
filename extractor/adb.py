import subprocess
import sys


def list_packages():
    result = subprocess.run(
        'adb shell pm list packages'.split(),
        capture_output=True,
    )
    if result.stderr:
        raise RuntimeError(result.stderr.decode('utf-8'))
    print(f'packages: {result.stderr}')
    lines = result.stdout.strip().splitlines()
    return [line.decode('utf-8').replace('package:', '') for line in lines]


def get_package_path(package):
    result = subprocess.run(
        f'adb shell pm path {package}'.split(),
        capture_output=True,
        check=True,
    )
    return result.stdout.decode('utf-8').strip().replace('package:', '')


def pull_path(path, out_path):
    result = subprocess.run(
        f'adb pull {path} {out_path}'.split(),
        capture_output=True,
        check=True,
    )
    return result.stdout.decode('utf-8').strip()


def pull_apk(package, out_path):
    print(f'Looking for package...', end='')
    try:
        if package not in list_packages():
            print(' FAIL')
            print(f'Package "{package}" was not found on device!')
            sys.exit(1)
    except RuntimeError as e:
        print(' FAIL')
        print(f'Could not get package list: {e}')
        sys.exit(1)
    print(' OK')

    print(f'Getting package path...', end='')
    package_path = get_package_path(package)
    print(' OK')

    print(f'Pulling APK...', end='')
    pull_path(package_path, out_path)
    print(' OK')
