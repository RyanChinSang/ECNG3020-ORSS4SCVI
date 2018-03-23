# ECNG3020 - [Android] ORSS4SCVI
![image1](https://github.com/RyanChinSang/ECNG3020-ORSS4SCVI/blob/master/BETA/static/logos/logo.png?raw=true)

Object Recognition Sub-System for the Smart Cane for the Visually Impaired.

Real-time object detection and classification\identification, color recognition, operation using voiced input (or manual keyed-input) and audio output.

## Latest release - v1.3a
### What's new?
* Settings:
    * Username to accommodate a more personalized experience when using the App. This is used most notably for the new TTS welcome message feature (see below).
    * Black-screen operation which attempts to put the app into a lower power consumption state by minimizing the use of the screen of the device. This is activated through touching the screen for 3 seconds, and deactivated by touching the screen once after.
    * Reset To reset all settings to their pre-configured default values and initiate the new Initial Setup Wizard (see below).
    * Settings' backend is now completely revised to facilitate expansion and conformation with the new Initial Setup Wizard (see below).
    * Settings' structure now has dedicated categorization for the different modules of the App.

* (NEW) Initial Setup Wizard:
    * On every new startup, or on App reset (through settings), the Initial Setup Wizard will automatically invoke to assist in configuring the App and facilitate a means for the user to better understand the App's features.
    * Settings displayed on the Setup Wizard are coherent with the settings available in the App's Settings menu with their default values set.
    * Option to Skip the Setup at any phase, except on the last. If skipped, not all changes to the Settings would be saved.

* Object Detection system:
    * Object detection will always monitor (every ~5 seconds) for a "crowded" condition (where there are 5 or more people detected in the Field of Vision) and will play a double beep-tone if the condition is true.
    * New algorithm! Object Detection function will now report (to the user) the object that is closest to the centre of the Field of Vision, instead of just the highest confidence detected object.
    * Delay period between drawing the object's bounding box and having the data ready to process is now smaller (simpler interface).

* Speech to Text service:
    * The App is now capable of outputting specific information when the user says the keyword "specific" in the command, independent of the Settings.
    * Assistant will now invoke an "I do not understand" message when the user's command does not match the known commands.
    * STT commands now use their own functions independent from the on-screen buttons.

* Text to Speech service:
    * A beep-tone will now play when the user calls the TTS service with an empty string.
    * Welcome message will always play at the main activity when the App starts as a unique instance (on Restart or Reset).
    * Upon changing any Settings, the TTS service will invoke and describe the change(s) made, along with a pop-up notification (Toast).
    * TTS now implements a check for the App's TTS settings on-demand; centralizes away from requiring other activities to perform the check.

* Other:
    * Clicking the App's Icon in the "About" section will now take the user to the GitHub webpage for the Android project.
    * Intentional delay time for exiting the App increased to 600ms to ensure all that services can properly close.
    * Formatted the GNU Licence text for the pop-up dialog - it is now much more readable.
    * Volume can now be toggled using the Volume Up/Down physical buttons on the device, instead of going into GTFODAPI's debug mode.
    * Exiting and TTS services now operates without error.
    * Bug with App returning to Settings instead of the main activity. It will now always return to the correct activity.
    * More code cleanup, reformatting and renaming. Variable names are now consistent.

### Main
![image2](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-1.png)![image3](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-2.png)

### Main Menu
![image4](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-3.png)![image4](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-4.png)![image4](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-5.png)

### Initial Setup Wizard
![image7](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-6.png)![image8](https://raw.githubusercontent.com/RyanChinSang/ECNG3020-ORSS4SCVI/master/History/AndroidScreenshots/v1.3a/ORSS4SCVI_v1.3a-7.png)


### Features:
* Real-time Object Identification using [Google's TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection).
* Colour Identification based on [RGB to Color Name Reference by Kevin J. Walsh](https://web.njit.edu/~kevin/rgb.pdf).
* Speech Recognition using [DroidSpeech](https://github.com/vikramezhil/DroidSpeech) and [PocketSphinx](https://github.com/cmusphinx/pocketsphinx-android).
* Text-to-Speech using [Android's Text to Speech Synthesizer](https://developer.android.com/reference/android/speech/tts/TextToSpeech.html).
* Image processing using [OpenCV-Android](https://github.com/opencv/opencv/wiki/ChangeLog#version341).

### Coming Soon:
* Optical Character Recognition.
* Instance Segmentation.

## Introduction
This is the official Git-repository for all code related to the [ECNG3020 Project](http://ecng.sta.uwi.edu/ecng/ecng3020/) titled above for completion to the [BSc. Electrical and Computer Engineering](https://sta.uwi.edu/eng/electrical/) at the [University of the West Indies, St. Augustine](http://sta.uwi.edu/).

The Project Report and other Documentation can be found [here](https://drive.google.com/drive/folders/0B9tE495iG_1PUmFKdUlIcWVoS2c?usp=sharing). (Authorization required)

## Authors
* Developed by **Ryan Chin Sang**.
    * Email: `ryancs1995@gmail.com` or `ryan.chinsang@my.uwi.edu`

* Supervised by [Dr. Akash Pooransingh](https://sta.uwi.edu/eng/electrical/staff/akash_pooransingh.asp).
