from fastapi import FastAPI, HTTPException, Request
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

logging.basicConfig(level=logging.INFO,filename='/app/log/logs.log',filemode='a',datefmt='%d-%m-%Y %H:%M:%S',format='%(asctime)s %(module)s %(levelname)s: %(message)s')
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
def index(request: Request):
	logger.info(f"Request from {request.client.host}")
	return {"Author": "Syukur","Status":"Ready!","Version":"1.0.0","DateTime": datetime.now()}

@app.get("/languages")
def languages(request: Request):
	sourcelang = googletrans.LANGUAGES
	logger.info(f"Request from {request.client.host}")
	return sourcelang

@app.get("/play")
def play( request: Request ,file: str, priority: bool = False):
	logger.info(f"Request from {request.client.host}")
	if file is None or not file:
		logger.debug("missing parameter")
		raise HTTPException(status_code=400, detail="Missing parameter")

	if os.path.exists(file):
		if priority is None or not priority:
			_player.add_to_playlist(file)
		else:
			if _player.get_status() == "Playing":
				_player.pause()
			_primary_player.add_to_playlist(file)
			if _player.get_status() == "Paused":
				_player.play()
				
		if _player.get_status() == "Playing":
			return {"message":f"Add to playlist:{file}"}
		return {"message":"Playing"}
    
	raise HTTPException(status_code=400, detail="file not found")

@app.get('/audio_list')
def get_audio_files(request: Request):
	audio_extensions = ('.mp3', '.wav', '.flac')  # Add more extensions as needed
	audio_files = []
	for root, dirs, files in os.walk('/app/resources'):
		for file in files:
			if file.lower().endswith(audio_extensions):
				audio_files.append({file:os.path.join(root, file)})

	# rertun audio files in JSON format
	#list_audio = json.dumps(audio_files)
	logger.info(f"Request from {request.client.host}")
	return audio_files

@app.get('/status')
def player_State(request: Request):
	status = _player.get_status()
	time = _player.get_time()
	length = _player.get_length()
	file_req = json.loads(_player.get_playlist())
	if len(file_req["playlist"]) == 0:
		file = "No file"
	else:
		file = file_req["playlist"][_player.current_index]
	
	primary_status = _primary_player.get_status()
	primary_time = _primary_player.get_time()
	primary_length = _primary_player.get_length()
	primary_file_req = json.loads(_primary_player.get_playlist())
	if len(primary_file_req["playlist"]) == 0:
		primary_file = "No file"
	else:
		primary_file = primary_file_req["playlist"][_primary_player.current_index]

	logger.info(f"Request from {request.client.host}")
	return {"Player":{"status":status,"time": time,"length": length,"file":file},
		  "Primary_player":{"status": primary_status,"time": primary_time,"length": primary_length,"file":primary_file}}

@app.get('/stop')
def player_stop(request: Request,isPrimary: bool = False):
	if not isPrimary or isPrimary is None:
		_player.stop()
		return {"status":"stopped"}
	_primary_player.stop()
	logger.info(f"Request from {request.client.host}")
	return {"status":"stopped"}

@app.get("/speech")
def speech(request: Request, text: str, lan: str = "ms", priority: bool = False):
	#text = "Selamat pagi"
	if text is None or not text:
		logger.debug("missing parameter")
		raise HTTPException(status_code=400, detail="Missing parameter")

	if lan is None or not lan:
		speechOut = textToSound.text(text,"auto")
	else:
		speechOut = textToSound.text(text,lan)

	speechOut = textToSound.text(text,lan)
	soundSpeech = json.loads(speechOut.speech())

	if priority is None or not priority:
		_player.add_to_playlist(soundSpeech["file"])
	else:
		if _player.get_status() == "Playing":
			_player.pause()
		_primary_player.add_to_playlist(soundSpeech["file"])
		if _player.get_status() == "Paused":
			_player.play()
 
	logger.info(f"Request from {request.client.host}")
	return {"message":"Spoken","language":soundSpeech["language"]}

@app.get('/t_lan')
def speechtolan(request: Request, text: str, lan: str, to_lan: str):
	if text is None or not text or to_lan is None or not to_lan:
		logger.debug("missing parameter")
		raise HTTPException(status_code=400, detail="Missing parameter")

	if lan is None or not lan:
		speechOut = textToSound.text(text,"auto")
	else:
		speechOut = textToSound.text(text,lan)

	speechOut = textToSound.text(text,lan)
	soundSpeech = json.loads(speechOut.speechToLan(to_lan))
	_player.add_to_playlist(soundSpeech["file"])
	sourcelang = googletrans.LANGUAGES
	from_lang = sourcelang[soundSpeech["language"]]
	to_lang = sourcelang[soundSpeech["to_lan"]]
	logger.info(f"Request from {request.client.host}")
	return {"message":"Spoken","from":from_lang,"to":to_lang}

@app.get("/playlist")
def playlist(request: Request, isPrimary: bool = False):
	if isPrimary is None or not isPrimary:
		data = json.loads(_player.get_playlist())
	else:
		data = json.loads(_primary_player.get_playlist())
	logger.info(f"Request from {request.client.host}")
	return data