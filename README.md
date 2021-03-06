adb_android
==========

Enables android adb in your python script.

### Build status & coverage status

[![Build Status](https://travis-ci.org/vmalyi/adb_android.svg?branch=master)](https://travis-ci.org/vmalyi/adb_android)

### Purpose

This python package is a wrapper for standard android adb implementation. It allows you to execute android adb commands in your python script.

### What's supported?

Currently following adb commands are **supported**:
* adb push
* adb pull
* adb shell
* adb devices
* adb install
* adb uninstall
* adb get-serialno

Currently following adb commands are **not supported**:

* adb forward
* adb get-state
* adb wait-for-device
* adb start-server
* adb kill-server
* adb logcat
* adb bugreport
* adb jdwp
* adb help
* adb version
* adb -d
* adb -e
* adb -s

### How to install?

Install with help of pip:
```
pip install adb_android
```
### How to use?
```
from adb_android import adb_android as adb

adb.push('/tmp/file.txt', '/data/media/0')
adb.pull('/data/media/0/file.txt', '/tmp/')

...
```

### How to contribute?

* Implement adb commands which are currently not supported by the module (see above)
* Increase unit test coverage for already supported commands
* Bring your own ideas!
