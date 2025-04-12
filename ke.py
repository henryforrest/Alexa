import os
import requests
from flask import Flask, request

KEY2 = os.environ["KEY2"]
PATH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key="+KEY2

app = Flask(__name__)

@app.route("/ke",methods=["POST"])
def endpoint():
  js = request.get_json()
  question = js.get("text")
  if question != None:
    hdrs = {"Content-Type":"application/json"}
    js   = {"contents":[{"parts":[{"text":question}]}]}
    rsp  = requests.post(PATH,headers=hdrs,json=js)
    if rsp.status_code == 200:
      answer = rsp.json()["candidates"][0]["content"]["parts"][0]["text"]
      return {"text":answer}, 200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

if __name__ == "__main__":
  app.run(host="localhost",port=3003)
