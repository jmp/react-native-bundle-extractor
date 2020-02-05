# react-native-bundle-extractor

This is a small utility for extracting the React Native JavaScript bundle
file from an Android APK.

## Installation

    pip install -r requirements.txt

## Usage

To extract the bundle from an APK:

    python extract.py foo.apk

To extract the bundle from connected device using `adb`:

    python extract.py com.package.someapp

To customize the bundle filename, you can pass an additional parameter:

    python extract.py com.package.someapp index.android.bundle
