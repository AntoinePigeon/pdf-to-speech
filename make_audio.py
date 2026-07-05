import boto3

# 1. Connect to Polly
polly = boto3.client("polly")

# 2. The text we want spoken.
text = "Hello Antoine. Your text to speech project is officially working."

# 3. Ask Polly to turn that text into audio.
response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",   # we want an MP3
    VoiceId="Joanna",     # which voice reads it
    Engine="neural"       # neural = the higher-quality voice engine
)

# 4. The audio arrives as a stream. Pull the raw bytes out of it.
audio_bytes = response["AudioStream"].read()

# 5. Write those bytes to a file.
with open("output.mp3", "wb") as file:
    file.write(audio_bytes)

print("Done! Saved output.mp3")