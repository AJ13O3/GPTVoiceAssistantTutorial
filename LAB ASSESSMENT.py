# Import modules
from openai import OpenAI
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
from playsound import playsound

# Creates an OpenAI client instance 
client = OpenAI() 
# Create a client using the credentials from your .csv file
polly = boto3.client('polly', 
                     region_name="eu-west-1", 
                     
                     aws_access_key_id = "ACCESS_KEY_ID", 
                     aws_secret_access_key = "SECRET_ACCESS_KEY"
                     )

# This is the "memory" of the API which allows it to recall previous conversations
# It is an array of message objects
# Each message object has a role (either "system", "user" or "assistant") and content
# The memory typically starts with a system message "telling" the API what its purpose is and helps set its behaviour
# In a message object where "user" is the role, the content is the query that the user has asked
# In a message object where "assistant" is the role, the content is API's response
apiMemory = [
    {"role": "system", "content": "You are a helpful assistant."},
  ]

def chatGPT():

  # Allows user to enter their query
  query = input(str("Enter a message: ")).lower()

  # Allows the user to exit if needed
  if query == "exit":
    quit()

  else:
    # Adds the user input into the API memory
    apiMemory.append({"role": "user", "content": query})

    # Generates a response based on the last message appended into the memory list
    # The "model" parameter refers to what model we are using, each with different capabilities and price points
    # Refer to https://platform.openai.com/docs/models/overview for information about other models
    # The second parameter "messages" passes the previous messages into the function
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages= apiMemory)

    # Filters out the API's reply from the full response
    reply = response.choices[0].message.content

    # Adds the API's reply into the API memory in order to remember what it has outputted
    apiMemory.append({"role": "assistant", "content": reply})

    # returns the reply for the user
    return reply+"\n"
    
def awsPolly():
  # Requests speech synthesis
  # The synthesize_speech function currently takes parameters
  # The text "Hello world!" is currently a placeholder and will be changed later
  # The OutputFormat is mp3 in order balance space in the hard drice and audio quality
  # The voice is the voice of the AI
  # Various voices can be used refer to the documentation for more information: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
  try:
      response = polly.synthesize_speech(Engine = "neural", Text=chatGPT(), OutputFormat="mp3", VoiceId="Emma" )                                 
  except (BotoCoreError, ClientError) as error:
      # The service returned an error, exit 
      print(error)
      sys.exit(-1)

  # Access the audio stream from the response
  if "AudioStream" in response:
          with closing(response["AudioStream"]) as stream:
            # Saves the output to the desktop as an .mp3 file
            output = os.path.join(os.path.expanduser("~/Desktop"), "reply.mp3")
            try:
              # Open a file for writing the output as a binary stream
                  with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit 
                print(error)
                sys.exit(-1)
  else:
      print("Could not stream audio")
      sys.exit(-1)

  # Play the audio using the playsound module
  playsound(output)

def main():
   awsPolly()

while 1:
    main()