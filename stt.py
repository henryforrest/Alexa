import base64
import os 
import requests
from flask import Flask, request

KEY = os.environ["KEY"]
REG = "uksouth"
URI = "https://" + REG + ".stt.speech.microsoft.com/" \
        "speech/recognition/conversation/cognitiveservices/v1?" \
        "language=en-US"

app = Flask(__name__)

@app.route("/stt",methods=["POST"])
def endpoint():
  js = request.get_json()
  t = js.get("speech")
  if t != None:
    u = base64.b64decode(t)
    v = work(u) 
    if v != None:
      return {"text":v},200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

def work(speech):
  hdrs = {
    "Content-Type":"audio/wav;samplerate=16000",
    "Ocp-Apim-Subscription-Key":KEY,
  }
  rsp = requests.post(URI,headers=hdrs,data=speech)
  if rsp.status_code == 200:
    return rsp.json()["DisplayText"]
  else:
    return None

if __name__ == "__main__":
  app.run(host="localhost",port=3001)
