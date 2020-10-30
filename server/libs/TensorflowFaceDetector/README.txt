This directory contains open source implementation of a tensorflow Mobilenet
SSD face detector.

The original source as download from the git repo is in:
    ./src_repo
The git repo is here:
    https://github.com/yeephycho/tensorflow-face-detection

The following changes were made:
 - create TensoflowFaceDetector class (from the example files) and put in its
 own file, so it can be called from our code.
 - Some paths may have been changed so this could be called as sub-module.
