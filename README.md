# react-native-bundle-extractor

This is a small utility for extracting the React Native JavaScript bundle
file from an Android APK.

## Installation

    pip install -r requirements.txt

## Usage

    python extract.py

This will look for an `app.apk` in the current directory. From the APK file,
the script will try to extract `assets/index.android.bundle`. It will extract
it into a `index.android.bundle` file in the current directory. The bundle
will be "beautified" by `jsbeautify`.
