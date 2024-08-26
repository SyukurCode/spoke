import vlc
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VLCPlayer:
	def __init__(self):
		self._thread = None
		self.player = vlc.MediaPlayer()
		logger.debug("player set")

	def stop(self):
		self.player.stop()

	def get_status(self):
		state = self.player.get_state()
		states = {
				vlc.State.NothingSpecial: "NothingSpecial",
				vlc.State.Opening: "Opening",
				vlc.State.Buffering: "Buffering",
				vlc.State.Playing: "Playing",
				vlc.State.Paused: "Paused",
				vlc.State.Stopped: "Stopped",
				vlc.State.Ended: "Ended",
				vlc.State.Error: "Error"
			}
		return states.get(state, "Unknown")

	def play(self,audio_file):
		media = vlc.Media(audio_file)
		self.player.set_media(media)
		self.player.play()
		# Allow some time for VLC to start
		time.sleep(1)
		# Get the duration of the audio in milliseconds
		duration = self.player.get_length()
		# Convert milliseconds to seconds and wait for the duration of the audio file
		time.sleep(duration / 1000.0)
		self.stop()


