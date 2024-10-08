# LIBRARY
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from googletrans import Translator
from gtts import gTTS
import logging
import os
import json
import threading

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

@app.route('/play', methods=["GET"])
def play():
	soundFile = request.args.get('file')
	if soundFile is None or not soundFile:
		logger.debug("missing parameter")
		return jsonify({"Error":"Missing parameter"}), 400
	#soundFile = "/opt/AlexaPi/src/resources/ok.mp3"
	if os.path.exists(soundFile):
		if _player.get_status() == "Playing":
			return jsonify({"message":"Player in use"}), 400
		task = threading.Thread(target=_player.play,args=(soundFile,))
		task.start()
		_player.play(soundFile)
		return jsonify({"message":"Playing"}), 200

	return jsonify({"message":"file not found"}), 400

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
	_player.play(soundSpeech["file"])
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
	_player.play(soundSpeech["file"])
	return jsonify({"message":"Spoken","from":soundSpeech["language"],"to":soundSpeech["to_lan"]}), 200

@app.errorhandler(404)
def error404_request(error):
    return jsonify({'message':str(error)}), 404


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000, debug=True)
