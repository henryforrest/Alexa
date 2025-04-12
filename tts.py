import base64
import os 
import requests
from flask import Flask, request

KEY = os.environ["KEY"]
REG = "uksouth"
URI = "https://" + REG + ".tts.speech.microsoft.com/" \
        "cognitiveservices/v1"

app = Flask(__name__)

@app.route("/tts",methods=["POST"])
def endpoint():
  js = request.get_json()
  t = js.get("text")
  if t != None:
    u = work(t) 
    if u != None:
      v = base64.b64encode(u).decode("ascii")
      return {"speech":v},200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

def ssml(text):
  return "<?xml version='1.0'?>" \
         "<speak version='1.0' xml:lang='en-US'>" \
         "  <voice xml:lang='en-US' name='en-US-JennyNeural'>" \
         + text + \
         "  </voice>" \
         "</speak>"

def work(text):
  hdrs = {
    "Content-Type":"application/ssml+xml",
    "X-Microsoft-OutputFormat":"riff-16khz-16bit-mono-pcm",
    "Ocp-Apim-Subscription-Key":KEY,
  }
  rsp = requests.post(URI,headers=hdrs,data=ssml(text))
  if rsp.status_code == 200:
    return rsp.content
  else:
    return None

if __name__ == "__main__":
  app.run(host="localhost",port=3002)
