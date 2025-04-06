import time
import requests
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO

load_dotenv()
IP_WEBCAM_URL = os.environ.get('IP_WEBCAM_URL')
BACKEND_URL = os.environ.get('BACKEND_URL')

def take_photo():
    try:
        response = requests.get(IP_WEBCAM_URL)
        image = Image.open(BytesIO(response.content))
         
        # Save the image
        filename = "captured_image.jpg"
        image.save(filename)
        print(f"Photo saved as {filename}")

        # Show the image (optional)
        # image.show()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def check_backend_to_take_photo():
    while True:
        try:
            response = requests.get(BACKEND_URL + "/check_if_photo_needed")
            if response.status_code == 200 and response.json().get("take_photo"):
                phtoto_taken = take_photo()
        except requests.RequestException as e:
            print(f"Error connecting to backend: {e}")
        time.sleep(5)  # Ping backend every 5 seconds

def scheduled_task():
    photo_taken = take_photo()

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', minutes=1)
    scheduler.start()

    backend_thread = threading.Thread(target=check_backend_to_take_photo)
    backend_thread.daemon = True
    backend_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        scheduler.shutdown()
