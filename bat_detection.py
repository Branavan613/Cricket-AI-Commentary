from inference_sdk import InferenceHTTPClient
import os
from dotenv import load_dotenv

load_dotenv()

def detect_bat(image):
    CLIENT = InferenceHTTPClient( 
        api_url="https://detect.roboflow.com",
        api_key= os.getenv("ROBOFLOW_API_KEY")
    )
    result = CLIENT.infer(image, model_id="cricket_shot_detection-wpa4x/1")
    print(f'THIS IS THE RESULT: {result["predictions"][0]["class"]}')
    return result["predictions"][0]["class"]