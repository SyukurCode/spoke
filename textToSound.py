from googletrans import Translator
from gtts import gTTS
from datetime import datetime
import json
import logging
import googletrans

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

translator = Translator()

class text:
	_language = None
	_text = None
	def __init__(self,textSpeech,language='auto'):
		self._language = language
		self._text = textSpeech

	def speech(self):
		if self._language == 'auto' or self._language is None or not self._language:
			lang_detect = self.detectLanguage(self._text)
			lang_set = lang_detect
		else:
			lang_set = self._language

		logger.info("lang:{}".format(lang_set))
		speechAudio = gTTS(self._text, lang=lang_set, slow=False)
		filename = f"./tmp/{datetime.now().timestamp()}.mp3"
		speechAudio.save(filename)

		output = {
			  "file": filename,
			  "language": lang_set
			 }

		return json.dumps(output)

	def speechToLan(self,lang):
		self._text = self.translating(self._text,lang)
		if self._language == 'auto' or self._language is None or not self._language:
			lang_detect = self.detectLanguage(self._text)
			lang_set = lang_detect
		else:
			lang_set = self._language

		speechAudio = gTTS(self._text, lang=lang, slow=False)
		filename = f"./tmp/{datetime.now().timestamp()}.mp3"
		speechAudio.save(filename)

		output = {
                          "file": filename,
                          "language": lang_set,
			  "to_lan":lang
                         }

		return json.dumps(output)

	def translating(self,text,lang='ms'):
		translations = translator.translate(text, dest=lang)
		return translations.text

	def detectLanguage(self,text):
		lans = translator.detect(text).lang
		for lan in lans:
		#GET SINGLE LANGUAGE
			if len(lan) == 2:
				return lan
			else:
				return lans
