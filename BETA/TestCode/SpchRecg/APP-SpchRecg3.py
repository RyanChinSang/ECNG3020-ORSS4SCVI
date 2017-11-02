import os
import pocketsphinx as ps

modeldir = "C:/Python36-64/Lib/site-packages/pocketsphinx/model/"
datadir = "C:/Python36-64/Lib/site-packages/pocketsphinx/data/"

# Create a decoder with certain model
config = ps.Decoder.default_config()
config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
config.set_string('-lm', os.path.join(modeldir, 'en-us.lm.bin'))
config.set_string('-dict', os.path.join(modeldir, 'cmudict-en-us.dict'))
# config.set_string('-kws', 'command.list')

# Open file to read the data
# stream = open(os.path.join(datadir, "goforward.raw"), "rb")

# Alternatively you can read from microphone
import pyaudio
#
#
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# Process audio chunk by chunk. On keyword detected perform action and restart search
decoder = ps.Decoder(config)
# decoder = Decoder()
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break
    if decoder.hyp() is not None:
        print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
        print("Detected keyword, restarting search")
        decoder.end_utt()
        decoder.start_utt()
