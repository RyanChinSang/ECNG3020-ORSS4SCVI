# ECNG3020 - [Android] ORSS4SCVI
![image1](https://github.com/RyanChinSang/ECNG3020-ORSS4SCVI/blob/master/BETA/static/logos/logo.png?raw=true)

Object Recognition Sub-System for the Smart Cane for the Visually Impaired.

Real-time object detection and classification\identification, color recognition, operation using voiced input (or manual keyed-input) and audio output.

## Latest release - v1.2a
### What's new?
* Speech to Text service:
    * Configurable Voice Recognition service in "Settings".
    * Increased period to 6 seconds for inputting voiced commands.
    * The Continuous Voice Recognition keyphrase is now "ok assistant" since the old keyword incurred false positives too frequently.
    * Voice Recognition timeout mechanism can now be properly interrupted.
* Color Detection system:
    * Gaussian filtering to the Color Detection algorithm (via OpenCV).
    * Configurable filtering in "Settings".
    * Color Detection algorithm uses OpenCV's "Mat" class to process pixel color.
* Re-vamped About section:
    * New Version Changelog pop-up dialog on pressing the "Version" text in the "About" section.
    * New License pop-up dialog on pressing the "License" text in the "About" section.
    * Layout overhaul - much more graphical; Image(s) and formatted text.
* Other:
    * Full integration of the OpenCV-3.4.1 Android library.
    * Android's "Back" key/button will now always incur a prompt on the main screen to exit the App.
    * Official Git-Hub release for the Android App.
    * Polished Git-READMEs for both branches of this project.
    * Minor code cleanup and reformatting.


![image2](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.2a/ORSS4SCVI_v1.2a-1.png)![image3](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.2a/ORSS4SCVI_v1.2a-2.png)

### Features:
* Real-time Object Identification using [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection).
* Colour Identification based on [RGB to Color Name Reference by Kevin J. Walsh](https://web.njit.edu/~kevin/rgb.pdf).
* Speech Recognition using [DroidSpeech](https://github.com/vikramezhil/DroidSpeech) and [PocketSphinx](https://github.com/cmusphinx/pocketsphinx-android).
* Text-to-Speech using [Android's Text to Speech Synthesizer](https://developer.android.com/reference/android/speech/tts/TextToSpeech.html).
* Image processing using [OpenCV-Android](https://github.com/opencv/opencv/wiki/ChangeLog#version341).

### Coming Soon:
* Optical Character Recognition.

## Introduction
This is the official Git-repository for all code related to the [ECNG3020 Project](http://ecng.sta.uwi.edu/ecng/ecng3020/) titled above for completion to the [BSc. Electrical and Computer Engineering](https://sta.uwi.edu/eng/electrical/) at the [University of the West Indies, St. Augustine](http://sta.uwi.edu/).

The Project Report and other Documentation can be found [here](https://drive.google.com/drive/folders/0B9tE495iG_1PUmFKdUlIcWVoS2c?usp=sharing). (Authorization required)

## Authors
* Developed by **Ryan Chin Sang**.
    * Email: `ryancs1995@gmail.com` or `ryan.chinsang@my.uwi.edu`

* Supervised by [Dr. Akash Pooransingh](https://sta.uwi.edu/eng/electrical/staff/akash_pooransingh.asp).
