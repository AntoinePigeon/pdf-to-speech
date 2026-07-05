import boto3

# A "client" is a configured connection object for one AWS service.
# boto3 automatically reads your keys from ~/.aws/credentials
# and your region from ~/.aws/config. No secrets in this file.
polly = boto3.client("polly")

# describe_voices() is a harmless, free, read-only call.
# It's the perfect first test because it can't cost anything.
voices = polly.describe_voices()

# The response is a dictionary. We dig into it and print one voice name.
print("Connection works! Example voice:", voices["Voices"][0]["Name"])