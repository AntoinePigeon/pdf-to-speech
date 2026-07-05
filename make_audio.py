import boto3

polly = boto3.client("polly")

text = "Hello Antoine. Your text to speech project is officially working."

response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",
    VoiceId="Joanna",
    Engine="neural"
)

audio_bytes = response["AudioStream"].read()

with open("output.mp3", "wb") as file:
    file.write(audio_bytes)

print("Done! Saved output.mp3")