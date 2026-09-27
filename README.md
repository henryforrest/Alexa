# Alexa-style voice assistant

A small experiment in chaining cloud APIs. You post a short WAV recording of a
question and get back a WAV recording of the answer: Azure transcribes the audio,
Google's Gemini answers the text, and Azure reads the answer aloud. I wrote it to get
comfortable with REST APIs, so it is deliberately minimal: four small Flask services.

## How it works

`alexa.py` is the orchestrator. It receives the audio, calls the three stage
services over HTTP in turn, and feeds each stage's JSON response into the next.

1. Speech to text (`stt.py`, port 3001). Accepts `{"speech": <base64 WAV>}`, decodes
   it and posts the raw bytes to the Azure Speech REST endpoint
   (`uksouth.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1`,
   `language=en-US`) with `Content-Type: audio/wav;samplerate=16000`. Returns `{"text": <DisplayText>}`.
2. Answer (`ke.py`, port 3003). Accepts `{"text": <question>}` and posts
   `{"contents": [{"parts": [{"text": <question>}]}]}` to Gemini's `generateContent`
   endpoint for `gemini-1.5-flash`. Returns the first candidate's text as `{"text": <answer>}`.
3. Text to speech (`tts.py`, port 3002). Accepts `{"text": <answer>}`, wraps it in SSML
   with the `en-US-JennyNeural` voice and posts it to Azure's `cognitiveservices/v1`
   endpoint, asking for `riff-16khz-16bit-mono-pcm`. Returns `{"speech": <base64 WAV>}`.

`POST /alexa` on port 3004 takes `{"speech": <base64 WAV>}` and returns the final
`{"speech": ...}` with a 200, or an empty 500 if any stage fails. Each service
answers 400 if its input field is missing and 500 if the upstream call fails.

## Project layout

- `alexa.py` - orchestrator; chains the three services over HTTP.
- `stt.py` - speech to text via the Azure Speech REST API.
- `ke.py` - "knowledge entity": answers the transcribed question with Gemini.
- `tts.py` - text to speech via Azure Speech, returning a WAV.
- `test-alexa.py` - end-to-end test: sends `question.wav`, saves `answer.wav`.

## Running

Python 3 with `flask` and `requests` (`pip install flask requests`). Two environment
variables are read at start-up:

- `KEY` - an Azure Speech resource key. The region is hard-coded to `uksouth`, and
  the same key is used by `stt.py` and `tts.py`.
- `KEY2` - a Google AI Studio API key for the Gemini API, used by `ke.py`.

With both exported, start the three stage services and then the orchestrator, each
in its own terminal: `python stt.py`, `python tts.py`, `python ke.py`, `python alexa.py`.
To try it end to end, record a question as `question.wav` (16 kHz, 16-bit mono PCM, as
the Azure request declares) in this directory and run `python -m unittest test-alexa.py`.
The test posts the file to `/alexa`, checks for a 200 and writes the reply to `answer.wav`.
It has no `__main__` block, so it must be run through `unittest` rather than directly.

## Notes

- Single turn: each request is independent and nothing is remembered between
  questions. There is no wake word or microphone capture; audio travels as base64 in JSON.
- The language, voice, region and Gemini model name are hard-coded. Google retires
  model versions over time, so `gemini-1.5-flash` may need updating.
- Error handling is minimal (any failure becomes an empty 500), the test only checks
  the status code, and the services have no authentication: localhost only.
