from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator
from gtts import gTTS
from datetime import datetime
import logging, json, cron, os
import googletrans

# LOCAL LIBRARY
import player
import textToSound

#DEFINE TRASLATOR
translator = Translator()

#DEFINE PLAYER
_player = player.VLCPlayer()
_primary_player = player.VLCPlayer()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Spoke Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Test"])
def index():
    return {"Author": "Syukur","Status":"Ready!","Version":"1.0.0","DateTime": datetime.now()}

@app.get("/languages")
def languages():
	sourcelang = googletrans.LANGUAGES
	return sourcelang

@app.get("/play")
def play(soundFile: str,priority: bool = False):
    if soundFile is None or not soundFile:
        logger.debug("missing parameter")
        raise HTTPException(status_code=400, detail="Missing parameter")

    if os.path.exists(soundFile):
        if priority is None or not priority:
            _player.add_to_playlist(soundFile)
        else:
            if _player.get_status() == "Playing":
                _player.pause()
            _primary_player.add_to_playlist(soundFile)
            if _player.get_status() == "Paused":
                _player.play()

        if _player.get_status() == "Playing":
            return {"message":f"Add to playlist:{soundFile}"}
        return {"message":"Playing"}
    
    raise HTTPException(status_code=400, detail="file not found")

@app.get('/audio_list')
def get_audio_files():
	audio_extensions = ('.mp3', '.wav', '.flac')  # Add more extensions as needed
	audio_files = []
	for root, dirs, files in os.walk('/app/resources'):
		for file in files:
			if file.lower().endswith(audio_extensions):
				audio_files.append({file:os.path.join(root, file)})

	# rertun audio files in JSON format
	#list_audio = json.dumps(audio_files)
	return audio_files

@app.get('/status')
def player_State():
	status = _player.get_status()
	return {"status":status}

@app.get('/stop')
def player_stop():
	_player.stop()
	return {"status":"stopped"}

@app.get("/speech")
def speech(textForSpeech: str, lan: str, priority: bool = False):
	#textForSpeech = "Selamat pagi"
	if textForSpeech is None or not textForSpeech:
		logger.debug("missing parameter")
		raise HTTPException(status_code=400, detail="Missing parameter")

	if lan is None or not lan:
		speechOut = textToSound.text(textForSpeech,"auto")
	else:
		speechOut = textToSound.text(textForSpeech,lan)

	speechOut = textToSound.text(textForSpeech,lan)
	soundSpeech = json.loads(speechOut.speech())

	if priority is None or not priority:
		_player.add_to_playlist(soundSpeech["file"])
	else:
		if _player.get_status() == "Playing":
			_player.pause()
		_primary_player.add_to_playlist(soundSpeech["file"])
		if _player.get_status() == "Paused":
			_player.play()

	return {"message":"Spoken","language":soundSpeech["language"]}

@app.get('/t_lan')
def speechtolan(textForSpeech: str, lan: str, to_lan: str):
	if textForSpeech is None or not textForSpeech or to_lan is None or not to_lan:
		logger.debug("missing parameter")
		raise HTTPException(status_code=400, detail="Missing parameter")

	if lan is None or not lan:
		speechOut = textToSound.text(textForSpeech,"auto")
	else:
		speechOut = textToSound.text(textForSpeech,lan)

	speechOut = textToSound.text(textForSpeech,lan)
	soundSpeech = json.loads(speechOut.speechToLan(to_lan))
	_player.add_to_playlist(soundSpeech["file"])
	sourcelang = googletrans.LANGUAGES
	from_lang = sourcelang[soundSpeech["language"]]
	to_lang = sourcelang[soundSpeech["to_lan"]]
	return {"message":"Spoken","from":from_lang,"to":to_lang}

@app.get("/playlist")
def playlist():
	data = json.loads(_player.get_playlist())
	return data