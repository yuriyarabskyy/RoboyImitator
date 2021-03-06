from roboy_imitator.common import CONFIGS, VOICES, EMOTIONS
from xml.etree import ElementTree

import os
import requests
import time
import logging


class TextToSpeech:

    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self, text_string, voice):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        voice_name = 'Microsoft Server Speech Text to Speech Voice ' + voice
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'de-DE')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'de-DE')
        # change Jessa to guy for male voice
        voice.set('name', voice_name)
        voice.text = text_string
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        logging.debug(f"Status code: {response.status_code}")
        file_name = 'test.wav'  # placeholder
        file_path = os.path.abspath(file_name)

        if response.status_code == 200:
            with open(file_path, 'wb') as audio:
                audio.write(response.content)
                file_path = os.path.realpath(audio.name)
                logging.debug("Your TTS is ready for playback.")
        else:
            logging.warning("Something went wrong. Check your subscription key and headers.")

        return file_path


def tts_test(subscription_key, teststring, emotion="neutral"):
    voice = VOICES[EMOTIONS.get(emotion, "Zira")]
    app = TextToSpeech(subscription_key)
    app.get_token()
    file_path = app.save_audio(text_string=teststring, voice=voice)
    return file_path


if __name__ == "__main__":
    print(tts_test(CONFIGS["tts_key"], "This is a long sentence. I can't show emotions.", emotion="happines"))
