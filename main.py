from groq import Groq
import os
import csv
import re
from dotenv import load_dotenv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from convertToSpeech import tts

load_dotenv()
api_key = os.getenv("LLAMA_API_KEY")
client = Groq(api_key=api_key)

commentary_counter = 1
past_events = [
    "The game has begun! The players take their positions, the crowd is buzzing with excitement, and Dale is ready with the new ball. Madushka takes his guard—let’s get this match underway!",
    "Dale charges in, steaming towards the crease. He delivers a sharp short ball—Madushka stands tall, meets it with a firm punch off the back foot. No run, but solid defensive play!"
]
system_message = {}
def begin_commentary(info, examples):
    c1 = info["team1"]
    c2 = info["team2"]
    venue = info["venue"]
    toss = info["toss"]
    decision = info["decision"]
    dewFactor = info["dewFactor"]
    weather = info["weather"]
    commentator1Style = info["commentator1Style"]
    commentator2Style = info["commentator2Style"]
    language = info["language"]
    return {
        "role": "system",
        "content": (
            f"Answer in the language {language}, speak in full sentences."
            f"You are two professional cricket commentators covering a live match between {c1} and {c2} at {venue}. "
            f"The toss was won by {toss}, and they decided to {decision}. The weather is {weather} with a dew factor of {dewFactor}. "
            "Your goal is to create an **exciting, realistic, and emotional** live sports broadcast. "
            "Use **cricket terminology** (e.g., cover drive, bouncer, third umpire). "
            "Express **emotion**: excitement for a six, suspense for a review, frustration for a wicket. "
            f"The first commentator should speak {commentator1Style}, and the second commentator should speak {commentator2Style}. "
            "Speak **naturally, like a real live commentary broadcast**."
            "When first commentator speaks, use 'C1' and when second commentator speaks, use 'C2'."
            f"Here are some examples of commentary: {examples}"
            "Avoid duplicate phrases and repetitive content. "
            "Should always have both commentators speaking. Every return message should be in the form of 'C1: commentary. C2: commentary.'"
            "Write complete sentences."
        )}

def generate_commentary(event, info, past_events, elapsed_time):
    global commentary_counter
    commentary_counter += 1
    
    c1 = info["team1"]
    c2 = info["team2"]
    venue = info["venue"]
    toss = info["toss"]
    decision = info["decision"]
    dewFactor = info["dewFactor"]
    weather = info["weather"]
    
    if commentary_counter <= 2:
        user_content = (
            f"Welcome to the live broadcast of the match between {c1} and {c2} at {venue}. "
            f"The toss was won by {toss}, and they decided to {decision}. The weather is {weather} with a dew factor of {dewFactor}. "
            f"Let's start the commentary with {event}."
            f"It should have a word count of {elapsed_time * 2}"
        )
    else:
        previous_events_summary = " ".join(past_events[-5:])
        user_content = f"{event} Previously: {previous_events_summary}"
    chat_completion = client.chat.completions.create(
        messages=[
            system_message,
            {
                "role": "user",
                "content": user_content
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.9,
        max_completion_tokens=150,
        top_p=1,
        stop=None,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def start(team1, team2, venue, toss, decision, dewFactor, weather, commentator1Style, commentator2Style, language):
    global system_message
    csv_content = []
    with open('commentary.csv', 'r', newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for i, row in enumerate(reader):
            if i >= 40:
                break
            csv_content.append(f"{row[3]}: {row[5]}")
    csv_content_str = " | ".join(csv_content)

    info = {
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "toss": toss,
        "decision": decision,
        "dewFactor": dewFactor,
        "weather": weather,
        "commentator1Style": commentator1Style,
        "commentator2Style": commentator2Style,
        "language": language
    }
    system_message = begin_commentary(info, csv_content_str) 
    return info

def extract_content(text):
    matches = re.findall(r'C\d:\s*([^C]+)', text)
    return [match.strip() for match in matches]

start_time = time.time()
class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self):
        self.info = start("England Lions", "Sri Lanka", "Wankhede Stadium", "England Lions", "Bat", "High", "Clear", "Excited", "Calm", "English")
        self.languageConversion = {"English": 0, "Hindi": 1, "Japanese": 2}
        self.real_time = False
        super().__init__()
    def calcTime(self):
        global start_time
        elapsedTime = time.time() - start_time
        start_time = time.time()
        return elapsedTime
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        event = data.get('event')
        elapsed_time = self.calcTime()
        language = self.languageConversion[self.info["language"]]
        
        if not event:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Event is required"}).encode())
            return
        
        commentary = generate_commentary(event, self.info, past_events, elapsed_time)
        split = extract_content(commentary)
        past_events.append(commentary)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        tts([split[0], split[1]], language, elapsed_time, self.real_time)
        self.wfile.write(json.dumps(
            {"message": "Event processed", 
             "language": self.info["language"],
             "Commentator 1": split[0],
             "Commentator 2": split[1],
             "elapsed_time": elapsed_time}).encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()