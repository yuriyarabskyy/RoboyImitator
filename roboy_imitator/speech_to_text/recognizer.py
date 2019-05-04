from roboy_imitator.common import CONFIGS

import azure.cognitiveservices.speech as speechsdk
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 3200


class SpeechToText:

    def __init__(self, key=CONFIGS["stt_key"], region=CONFIGS["service_region"]):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    def recognize(self, mic_source=None):
        # setup the audio stream
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        if mic_source is None:
            audio = pyaudio.PyAudio()
            # Claim the microphone
            mic_source = audio.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        # Connect callbacks to the events fired by the speech recognizer
        #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

        speech_recognizer.start_continuous_recognition()

        try:
            while True:
                frames = mic_source.read(CHUNK)
                if not frames:
                    break
                stream.write(frames)
        except KeyboardInterrupt:
            pass
        finally:
            mic_source.stop_stream()
            speech_recognizer.stop_continuous_recognition()
            stream.close()
            mic_source.close()


if __name__ == "__main__":
    speech_to_text = SpeechToText(CONFIGS["stt_key"], CONFIGS["service_region"])
    speech_to_text.recognize()
