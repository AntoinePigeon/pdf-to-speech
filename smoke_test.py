import boto3

polly = boto3.client("polly")

voices = polly.describe_voices()

print("Connection works! Example voice:", voices["Voices"][0]["Name"])