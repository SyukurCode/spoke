# LIBRARY
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from googletrans import Translator
from gtts import gTTS
import logging
import os
import json, requests
import googletrans
import cron

# LOCAL LIBRARY
import player
import textToSound

#DEFINE TRASLATOR
translator = Translator()

#DEFINE PLAYER
_player = player.VLCPlayer()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
	return jsonify({"message":"ready!"}), 200

@app.route('/languages')
def languages():
	sourcelang = googletrans.LANGUAGES
	return sourcelang

@app.route('/play', methods=["GET"])
def play():
	soundFile = request.args.get('file')
	if soundFile is None or not soundFile:
		logger.debug("missing parameter")
		return jsonify({"Error":"Missing parameter"}), 400

#	local_req = requests.get("http://localhost:3000/audio_list")
#	audio_file_name = local_req.json() 
#	logger.info(f"{audio_file_name}")

	if os.path.exists(soundFile):
		_player.add_to_playlist(soundFile)
		if _player.get_status() == "Playing":
			return jsonify({"message":f"Add to playlist:{soundFile}"}), 200
		return jsonify({"message":"Playing"}), 200

#	if os.path.exists(audio_file_name[soundFile]):
#		_player.add_to_playlist(audio_file_name[soundFile])
#		if _player.get_status() == "Playing":
#			return jsonify({"message":f"Add to playlist:{soundFile}"}), 200
#		return jsonify({"message":"Playing"}), 200

	return jsonify({"message":"file not found"}), 400

@app.route('/audio_list', methods=["GET"])
def list_audio_files():
	audio_extensions = ('.mp3', '.wav', '.flac')  # Add more extensions as needed
	audio_files = []
	for root, dirs, files in os.walk('/app/resources'):
		for file in files:
			if file.lower().endswith(audio_extensions):
				audio_files.append({file:os.path.join(root, file)})

	# rertun audio files in JSON format
	#list_audio = json.dumps(audio_files)
	return jsonify(audio_files), 200

@app.route('/status')
def playerState():
	status = _player.get_status()
	return jsonify({"status":status}), 200

@app.route('/stop')
def playerStop():
	_player.stop()
	return jsonify({"status":"stopped"}), 200

@app.route("/speech")
def speech():
	textForSpeech = request.args.get('text')
	lan = request.args.get('lan')
	#textForSpeech = "Selamat pagi"
	if textForSpeech is None or not textForSpeech:
		logger.debug("missing parameter")
		return jsonify({"Error":"Missing parameter"}), 400

	if lan is None or not lan:
		speechOut = textToSound.text(textForSpeech,"auto")
	else:
		speechOut = textToSound.text(textForSpeech,lan)

	speechOut = textToSound.text(textForSpeech,lan)
	soundSpeech = json.loads(speechOut.speech())
	_player.add_to_playlist(soundSpeech["file"])
	return jsonify({"message":"Spoken","language":soundSpeech["language"]}), 200

@app.route('/t_lan', methods=["GET"])
def speechtolan():
	textForSpeech = request.args.get('text')
	lan = request.args.get('frm_lan')
	to_lan = request.args.get('to_lan')

	if textForSpeech is None or not textForSpeech or to_lan is None or not to_lan:
		logger.debug("missing parameter")
		return jsonify({"Error":"Missing parameter"}), 400

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
	return jsonify({"message":"Spoken","from":from_lang,"to":to_lang}), 200

@app.route("/playlist", methods=["GET"])
def playlist():
	return _player.get_playlist()

@app.errorhandler(404)
def error404_request(error):
    return jsonify({'message':str(error)}), 404


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000, debug=True)

