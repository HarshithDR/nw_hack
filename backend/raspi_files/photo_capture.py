import requests
from PIL import Image
from io import BytesIO

# Replace with your phone's IP from the IP Webcam app
IP_WEBCAM_URL = "http://10.103.251.223:8080/shot.jpg"

def capture_photo():
    try:
        response = requests.get(IP_WEBCAM_URL)
        image = Image.open(BytesIO(response.content))
         
        # Save the image
        filename = "captured_image.jpg"
        image.save(filename)
        print(f"Photo saved as {filename}")

        # Show the image (optional)
        # image.show()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the capture function
    capture_photo()