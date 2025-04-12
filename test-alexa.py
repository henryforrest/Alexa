import base64
import requests
import unittest

alexa = "http://localhost:3004/alexa"

class Testing(unittest.TestCase):
  ###########################################################
  ## Test [1]                                              ##
  ###########################################################
  def test1(self):
    f   = open("question.wav","rb")
    wav = f.read()
    f.close()

    speech1 = base64.b64encode(wav).decode("ascii")

    hdrs = {"Content-Type":"application/json"}
    js   = {"speech":speech1}
    rsp  = requests.post(alexa,headers=hdrs,json=js)

    self.assertEqual(rsp.status_code,200)

    speech2 = rsp.json()["speech"]

    wav     = base64.b64decode(speech2)
    f       = open("answer.wav","wb")
    f.write(wav)
    f.close()

    self.assertEqual(rsp.status_code,200)
    # verify speech somehow?
