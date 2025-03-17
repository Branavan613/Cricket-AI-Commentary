from groq import Groq
import time
client = Groq(api_key="")
import pyttsx3
import csv
engine = pyttsx3.init()

commentary_counter = 0
past_events = []

def begin_commentary(info):
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
            "Answer in the language {language}"
            "Keep under 40 words"
            f"You are two professional cricket commentators covering a live match between {c1} and {c2} at {venue}. "
            f"The toss was won by {toss}, and they decided to {decision}. The weather is {weather} with a dew factor of {dewFactor}. "
            "Your goal is to create an **exciting, realistic, and emotional** live sports broadcast. "
            "Use **cricket terminology** (e.g., cover drive, bouncer, third umpire). "
            "Express **emotion**: excitement for a six, suspense for a review, frustration for a wicket. "
            f"The first commentator should speak {commentator1Style}, and the second commentator should speak {commentator2Style}. "
            "Speak **naturally, like a real live commentary broadcast**."
            "When first commentator speaks, use 'C1' and when second commentator speaks, use 'C2'."
            "After using 'C1' or 'C2', express the emotion in the next sentence based on the event, for example excitement for a six, in this format: 'C2: event'. "
        )}
def generate_commentary(event, info, past_events):
    global commentary_counter
    commentary_counter += 1
    
    c1 = info["team1"]
    c2 = info["team2"]
    venue = info["venue"]
    toss = info["toss"]
    decision = info["decision"]
    dewFactor = info["dewFactor"]
    weather = info["weather"]
    

    # Adjust the content based on the number of commentary events
    if commentary_counter <= 3:
        user_content = (
            f"Welcome to the live broadcast of the match between {c1} and {c2} at {venue}. "
            f"The toss was won by {toss}, and they decided to {decision}. The weather is {weather} with a dew factor of {dewFactor}. "
            f"Let's start the commentary with {event}."
        )
    else:
        previous_events_summary = " ".join(past_events[-5:])
        user_content = f"Keep it under 30 words. {event} Previously: {previous_events_summary}"

    chat_completion = client.chat.completions.create(
        messages=[
            system_message,
            {
                "role": "user",
                "content": user_content
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=150,
        top_p=1,
        stop=None,
        stream=False,
    )
    return chat_completion.choices[0].message.content
# Print the completion returned by the LLM.
info = {
    "team1": "India",
    "team2": "Australia",
    "venue": "Wankhede Stadium",
    "toss": "India",
    "decision": "bat",
    "dewFactor": "low",
    "weather": "clear",
    "commentator1Style": "excited",
    "commentator2Style": "calm",
    "language": "Hebrew"
}
events = [
    "Rohit Sharma faces the first ball of the match.",
    "Rohit Sharma hits a beautiful cover drive for four runs.",
    "Shikhar Dhawan takes a quick single, good running between the wickets.",
    "Mitchell Starc bowls a bouncer, Rohit Sharma ducks under it.",
    "Rohit Sharma hits a huge six over mid-wicket, the crowd goes wild!",
    "An appeal for LBW against Shikhar Dhawan, the umpire is unmoved.",
    "Steve Smith takes a brilliant catch at slip, Shikhar Dhawan is out!",
#     "Virat Kohli plays a well-timed pull shot for another boundary.",
#     "Pat Cummins bowls a tight over, just two runs off it.",
#     "A direct hit from Glenn Maxwell, but Virat Kohli is safe.",
#     "Virat Kohli plays a lovely on-drive for four runs, exquisite timing.",
#     "A misfield at point by David Warner, they take an extra run.",
#     "Josh Hazlewood bowls a slower ball, Rohit Sharma is deceived, dot ball.",
#     "Virat Kohli hits a powerful straight drive for six, what a shot!",
#     "Mitchell Starc bowls a quick bouncer, Virat Kohli is beaten.",
#     "Rohit Sharma plays a well-placed cut shot for four runs.",
#     "Pat Cummins bowls a yorker, Rohit Sharma digs it out.",
#     "A brilliant piece of fielding by Steve Smith, saves a certain boundary.",
#     "Virat Kohli lofts a shot over extra cover for six.",
#     "Rohit Sharma plays a leg glance for a single, good rotation of strike."
 ]
system_message = begin_commentary(info) 

def split_commentary(text):
    parts = text.split(" ", 1)
    return parts  


for event in events:
    commentary = generate_commentary(event, info, past_events)
    spilts = split_commentary(commentary)
    print(commentary)
    if (spilts[0] == "C1"):
        print("C1")
        #engine.setProperty('rate', 190)
        #engine.setProperty("voice", engine.getProperty('voices')[1].id)    
    else: 
        print("C2")
        #engine.setProperty('rate', 210)
        #engine.setProperty("voice", engine.getProperty('voices')[0].id)    
    #engine.say(spilts[1])
    #engine.runAndWait()
    past_events.append(commentary)
print(past_events)