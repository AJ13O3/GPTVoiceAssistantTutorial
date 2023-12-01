"""Getting Started Example for Python 2.7+/3.3+"""
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from playsound import playsound
from tempfile import gettempdir

# Create a client using the credentials from your .csv file
polly = boto3.client('polly', region_name="eu-west-1", aws_access_key_id = "AKIA3NOC5FNUWUIFNSZJ", aws_secret_access_key = "xTZgnDjEwVnypw+IJh7PRp8C0+oWLL9f9XNyDbra")

# Requests speech synthesis
# The synthesize_speech function currently takes parameters
# The text "Hello world!" is currently a placeholder and will be changed later on
# The OutputFormat is mp3 in order balance space in the hard drice and audio quality
# The voice is the voice of the AI
# Various voices can be used refer to the documentation for more information: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
try:
    response = polly.synthesize_speech(Text="Hello world!", OutputFormat="mp3", VoiceId="Joanna")
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
        with closing(response["AudioStream"]) as polly_stream:
           output = os.path.join(os.path.expanduser("~/Desktop"), "reply.mp3")
           try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                   file.write(polly_stream.read())
           except IOError as error:
              # Could not write to file, exit gracefully
              print(error)
              sys.exit(-1)
else:
    print("Could not stream audio")
    sys.exit(-1)

# Play the audio using the playsound module
playsound(output)