import requests
from flask import Flask, request

stt = "http://localhost:3001/stt"
tts = "http://localhost:3002/tts"
ke  = "http://localhost:3003/ke"

app = Flask(__name__)

@app.route("/alexa",methods=["POST"])
def endpoint():
  t = request.get_json()
  u = work(t) 
  if u != None:
    return u,200 # OK
  else:
    return "",500 # Internal Server Error

def work(x):
  return apply(tts,apply(ke,apply(stt,x)))

def apply(f,x):
  if x != None:
    hdrs = {"Content-Type":"application/json"}
    rsp = requests.post(f,headers=hdrs,json=x)
    if rsp.status_code == 200:
      return rsp.json()
    else:
      return None
  else:
    return None

if __name__ == "__main__":
  app.run(host="localhost",port=3004)
