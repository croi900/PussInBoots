import speech_recognition as sr
import pyttsx3
import spacy
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from openai import OpenAI
from textblob import Word
client = OpenAI(api_key="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")

nouns=[]

allowed_words = ["laptop", "mouse", "bottle", "wine glass", "cup", "remote", "toothbrush", "handbag",
                    "suitcase", "tie", "keyboard", "cell phone", "pizza", "sofa", "chair", "fork", "scissors", "book","banana","apple"]

id_name_map = {"0" : "Kitchen", "2" : "Living Room"}
def SpeakText(command):
	    # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()
def queue():
    # spacy subj
    nlp = spacy.load('en_core_web_sm')

    # Initialize the recognizer
    r = sr.Recognizer()


# Function to convert text to
# speech
    
    with sr.Microphone(device_index=1) as source2:
        r.adjust_for_ambient_noise(source2, duration=2)
        print("Adjusted for noise ! ! ! Nyaa~ owo ><")
        while (1):
            try:
            
                audio2 = r.listen(source2,phrase_time_limit=10)
                
            # Using google to recognize audiowi
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()


                print("Did you say ", MyText)


                doc= nlp(MyText)
                
                for chunk in doc.noun_chunks:
                    if  True:
                        sing=Word(chunk.root.text).singularize()
                        if sing in allowed_words:
                            nouns.append(sing)
                print(nouns)
                

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred")


thread1 = Thread(target=queue)
thread1.start()
def match(jon):
    rooms=json.loads(jon)
    v = []
    for rid in rooms:
        for itm in rooms[rid]:
            v.append([itm, rid])

    detection = {}
    for target in nouns:
        detection[target] = set()
        for item in v:
            if item[0] == target:
                detection[target].add((item[1],rooms[item[1]].count(target)))             

    print(detection)
    return detection        
def get_gpt_text(detection):    
    prompt = "Form a sentence where you explain to a blind person that there are "
    for target in detection:    
        if len(detection[target]) == 0:
            prompt += f"There are no {target}."
            nouns.remove(target)
        else:
            for tup in detection[target]:
                if target in nouns:
                    nouns.remove(target)
                else:
                    print("not in nouns", target)
                prompt += f" {tup[1]} {target} in the {id_name_map[tup[0]]}, "
        
    #print(prompt)
    if prompt == "Form a sentence where you explain to a blind person that there are ":
        return None
    
    if prompt:
        print(prompt)
        return prompt + ". You are obligated to say that all objects you mention are situated on a table! Also note that if there are no objects of a kind, don't mention that they are on a table, just say you can't find any."

    return prompt

class RequestHandler(BaseHTTPRequestHandler):
    # GET method handler
    def do_GET(self):
        if '/response' in self.path:
            
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            # Access the parameter values
            text = query_params.get('text', [''])[0]

            # Do something with the parameters
            # ...
            print(nouns)
            prompt = get_gpt_text(match(text))
            if prompt:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{prompt}"}
                    ]
                    )
                print(response.choices[0].message.content)

                SpeakText(response.choices[0].message.content)
            # Send a response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Success!")
        else:
            # If the path is not recognized, return a 404 error
            self.send_error(404, 'Not Found')

host = '0.0.0.0'
port = 8080
# Create an HTTP server instance
httpd = HTTPServer((host, port), RequestHandler)
# Start the server
print(f'Starting server on {host}:{port}')
httpd.serve_forever()
thread1.join()
