# ECNG3020 - ORSS4SCVI
![image1](https://github.com/RyanChinSang/ECNG3020-ORSS4SCVI/blob/master/BETA/static/logos/logo.png?raw=true)

Object Recognition Sub-System for the Smart Cane for the Visually Impaired.

Real-time object detection and classification\identification, color recognition, operation using voiced input (or manual keyed-input) and audio output.

## Latest release - v0.3a
### What's new?
//[ADD LINK]
Most of the developmental effort has been transferred to this prototype's implementation on the Android platform. You can see it [here]().

For full reference, see [VERSION.txt](https://github.com/RyanChinSang/ECNG3020-ORSS4SCVI/blob/master/VERSION.txt).
* Much more interactive; automated (spoken) messages:
    * Welcome and Goodbye messages.
    * Has "help" function to say all controls to the user.
    * Can say all controls to user for both Online and Offline mode, when in that mode.
* Improved colour identification:
    * Larger colour library.
    * Improved colour matching algorithm.
    * Can output both specific color, and quantized (simplified) colors.
* Improved program overall structure - better cohesion.
    * Improved the structure of Controls and how they are handled.
    * Improved the structure of the colors library.
    * Improved how Text to Speech is setup.
    * Improved how all variables are handled.
* Many minor bug fixes.


![image2](https://github.com/RyanChinSang/ECNG3020-ORSS4SCVI/blob/master/History/Screenshots/ORSS4SCVI_v0.3a.png?raw=True)

An application prototype built using [Python 3.6.3 64-bit](https://www.python.org/downloads/release/python-363/).

### Features:
* Real-time Object Identification using [Google TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection).
* Colour Identification based on [RGB to Color Name Reference by Kevin J. Walsh](https://web.njit.edu/~kevin/rgb.pdf).
* Speech Recognition using [Google Cloud Speech API](https://cloud.google.com/speech/) through [SpeechRecognition](https://github.com/Uberi/speech_recognition).
* Text-to-Speech using [pyttsx3](https://github.com/nateshmbhat/pyttsx3).
* Image processing using [OpenCV-Python](https://pypi.python.org/pypi/opencv-python) and [matplotlib](https://github.com/matplotlib/matplotlib).

### Coming Soon:
* Optical Character Recognition.

## Introduction
This is the official Git-repository for all code related to the [ECNG3020 Project](http://ecng.sta.uwi.edu/ecng/ecng3020/) titled above for completion to the [BSc. Electrical and Computer Engineering](https://sta.uwi.edu/eng/electrical/) at the [University of the West Indies, St. Augustine](http://sta.uwi.edu/).

The Project Report and other Documentation can be found [here](https://drive.google.com/drive/folders/0B9tE495iG_1PUmFKdUlIcWVoS2c?usp=sharing). (Authorization required)

## Authors
* Developed by **Ryan Chin Sang**.
    * Email: `ryancs1995@gmail.com` or `ryan.chinsang@my.uwi.edu`

* Supervised by [Dr. Akash Pooransingh](https://sta.uwi.edu/eng/electrical/staff/akash_pooransingh.asp).
