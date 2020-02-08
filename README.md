# react-native-bundle-extractor

This is a small utility for extracting the [React Native][1] JavaScript bundle
file from an Android APK. It can fetch the bundle either from an APK file
on the disk, or from an Android package installed on a connected device
(including Android virtual devices), without requiring deep knowledge of
the Android Debug Bridge (ADB).

Since React Native JavaScript bundles are typically minified, the tool
also runs it through [jsbeautifier][2] to get a more human-readable output.

The purpose of this tool is to give you a better idea of what your release
code will look like. It may convince you to obfuscate your JavaScript bundles. 

## Installation

    pip install -r requirements.txt

## Usage

To extract the bundle from an APK:

    python extract.py foo.apk

To extract the bundle from connected device using `adb`:

    python extract.py com.package.someapp

To customize the bundle filename, you can pass an additional parameter:

    python extract.py com.package.someapp --bundle index.android.bundle

## Run tests

    pytest

[1]: https://facebook.github.io/react-native/
[2]: https://pypi.org/project/jsbeautifier/
