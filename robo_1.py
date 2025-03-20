from inference import InferencePipeline
from inference.core.interfaces.camera.entities import VideoFrame
import cv2
import supervision as sv
from processor import process
from bat_detection import detect_bat
import os
from dotenv import load_dotenv
import requests

server_url = "<Input your server URL here>"
load_dotenv()

# Create a bounding box annotator and label annotator
label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoxAnnotator()
type_of_shot = []
last_bat = None
def my_custom_sink(predictions, video_frame):
    global out, frame_width, frame_height, last_bat
    
    # Convert predictions to detections format
    detections = sv.Detections.from_inference(predictions)
    
    # Create labels with additional information
    data = {}
    labels = []
    count = 0
    print(video_frame.frame_id)
    

    for detection, confidence in zip(detections.xyxy, detections.confidence):
        x_min, y_min, x_max, y_max = detection
        center_x = (x_max + x_min) / 2
        center_y = (y_max + y_min) / 2
        
        # Format label with location and confidence
        class_name = predictions["predictions"][count]["class"]
        label = f"{class_name}: ({center_x:.1f}, {center_y:.1f}) Conf: {confidence:.2f}"
        labels.append(label)
        if class_name not in data.keys():
            data[class_name] = []
        data[class_name].append({"position" : [x_min, x_max, y_min, y_max], "confidence" : confidence})
        
        # Print detailed information
        
        print(f"Detection - {label}")
        count += 1
    bat = process(data, frame_height, frame_width)
    print(f"In Box: {bat}")
    
    if bat:  # Adjust frame number as needed
        screenshot_path = f"./tests/tests_f/v3/frame_{video_frame.frame_id}.jpg"
        cv2.imwrite(screenshot_path, video_frame.image)
        print(f"Saved screenshot at frame {video_frame.frame_id}")
        type_of_shot.append(detect_bat(screenshot_path))
        os.remove(screenshot_path)
        event_data = {
            "event": bat
        }
        response = requests.post(server_url, json=event_data)
        # Print the response from the server
        if response.status_code == 200:
            print("Response from server:")
            print(response.json())
        else:
            print(f"Failed to send event. Status code: {response.status_code}")
            print(response.text)
        
    # Annotate frame
    image = label_annotator.annotate(
        scene=video_frame.image.copy(), 
        detections=detections, 
        labels=labels
    )   
    image = box_annotator.annotate(image, detections=detections)
    
    # Resize and write frame
    image_resized = cv2.resize(image, (frame_width, frame_height))
    out.write(image_resized)
    
    # Display
    cv2.imshow("Predictions", image_resized)
    cv2.waitKey(1)

def read_video(video_path):
    # Open a video writer to save output
    video_output_path = f"./tests/tests_f/v3/output.mp4"
    frame_width = 1280  # Set appropriate width
    frame_height = 720  # Set appropriate height
    fps = 30  # Set appropriate FPS
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (frame_width, frame_height))


    pipeline = InferencePipeline.init(
        model_id="cricket_animation/1",
        api_key=os.getenv("ROBOFLOW_API_KEY"),
        video_reference=video_path,
        on_prediction=my_custom_sink,
        confidence=0.2
    )

    pipeline.start()
    pipeline.join()
    
    # Release the video writer
    out.release()
    cv2.destroyAllWindows()