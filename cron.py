from apscheduler.schedulers.background import BackgroundScheduler
import os, glob, logging, time
import zoneinfo, player, requests

os.environ['TZ'] = 'Asia/Kuala_Lumpur'
zoneinfo.ZoneInfo('Asia/Kuala_Lumpur')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cleaner_scheduler = BackgroundScheduler()
player_scheduler = BackgroundScheduler()

class cron_job:
	def __init__(self):
		pass

	def execute_cleaning(self):
		logger.info("Cleaning Scheduler execute...")
		cleaner_scheduler.add_job(run_cleaning, 'interval', minutes=10)
		cleaner_scheduler.start()

	def execute_monitor(self):
		if not player_scheduler.get_jobs():
			logger.info("Monitoring Scheduler execute...")
			player_scheduler.add_job(player_monitor, 'interval', minutes=1)
			player_scheduler.start()
		
def player_monitor():
		response = requests.get("http://localhost:3000/status")
		if(response.status_code == 200):
			data = response.json()
			if data["Primary_player"]["status"] == "Ended":
				if data["Player"]["status"] == "Paused":
					req = requests.get("http://localhost:3000/continue")
					logger.info("Player continue")
					if player_scheduler.get_jobs() :
						player_scheduler.shutdown()
						logger.info("Scheduler stoped")
			
		else:
			if player_scheduler.get_jobs() :
				player_scheduler.shutdown()
				logger.info("Scheduler stoped")
				

def run_cleaning():
	folder_path = "./tmp"  # Specify the folder path
	mp3_files = glob.glob(os.path.join(folder_path, "*.mp3"))
	for file in mp3_files:
		try:
			if isOld(file):
				os.remove(file)
				logger.info(f"Deleted: {file}")
		except Exception as e:
			logger.info(f"Error deleting {file}: {e}")

def isOld(file):
	current_time = time.time()
	file_age = current_time - os.path.getmtime(file)

	# Check if the file is older than 1 hour (3600 seconds)
	if file_age > 1800:
		return True
	return False


