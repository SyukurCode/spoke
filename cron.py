from apscheduler.schedulers.background import BackgroundScheduler
import os, glob, logging, time
import zoneinfo

os.environ['TZ'] = 'Asia/Kuala_Lumpur'
zoneinfo.ZoneInfo('Asia/Kuala_Lumpur')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

scheduler = BackgroundScheduler()
scheduler.add_job(run_cleaning, 'interval', minutes=10)
scheduler.start()
