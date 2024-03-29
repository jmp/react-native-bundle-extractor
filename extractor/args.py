import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Extract React Native JavaScript bundle from an APK.",
    )
    parser.add_argument(
        "source",
        metavar="APK_OR_PACKAGE",
        help="a path to an APK file or an Android package name",
    )
    parser.add_argument(
        "--bundle",
        metavar="FILENAME",
        help="name of the JavaScript bundle file inside the APK",
        default="index.android.bundle",
    )
    parser.add_argument(
        "--out",
        metavar="FILENAME",
        help="path where the bundle should be extracted",
        default="index.android.bundle",
    )
    return parser.parse_args(args)
