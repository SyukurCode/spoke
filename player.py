import vlc
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VLCPlayer:
	def __init__(self):
		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()
		self.playlist = []
		self.current_index = 0
		logger.debug("player set")

	def play_media(self, media_path):
		media = self.instance.media_new(media_path)
		self.player.set_media(media)
		self.player.play()
		logger.debug(f"Playing:{media}")
		# Wait until the media is done playing
		self.wait_until_playing()
		self.wait_until_finished()

	def wait_until_playing(self):
		while self.player.get_state() not in (vlc.State.Playing, vlc.State.Error):
			time.sleep(0.1)

	def wait_until_finished(self):
		while self.player.get_state() == vlc.State.Playing:
			time.sleep(0.1)

        	# Move to the next item in the playlist if available
		self.next_media()

	def add_to_playlist(self, media_path):
		status = self.get_status()
		if not status == "Playing":  # Start playback if this is the first item
			self.playlist = []
			self.current_index = 0
			thread = threading.Thread(target=self.play_media, args=(media_path,))
			thread.start()

		self.playlist.append(media_path)
		logger.info(f"Playlist:[{self.playlist}]")

	def next_media(self):
		self.current_index += 1
		if self.current_index < len(self.playlist):
			self.play_media(self.playlist[self.current_index])


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

