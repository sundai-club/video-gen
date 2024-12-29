import os
import replicate
from replicate.helpers import FileOutput

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def generate_video(script, thumbnail=None):
    """Generate a video using Replicate"""
    # Initialize the Replicate client
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    model = "minimax/video-01" # output['url']
    # model = "minimax/video-01-live" # output['url'], but you need first_frame_image
    # model = "lightricks/ltx-video:c441c271f0cfd578aa0cd14a8488329dd10b796313a9335573a4a63507a976a5" # output[0]
    input = {
        "prompt": script,
        "prompt_optimizer": True,
    }
    if thumbnail:
        input["first_frame_image"] = thumbnail
    output = client.run(model, input=input)
    print(output)
    try:
        print(output.__dict__)
        print(output[0])
        print(output['url'])
    except Exception as e:
        print(e)
    if isinstance(output, list):
        output = output[0]
    if isinstance(output, dict):
        output = output['url']
    if isinstance(output, FileOutput):
        output = output.url
    return output


def generate_video_script(project_data):
    """Generate a video script using OpenAI"""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Prepare the messages
    prompt = open("prompt-extract-project-info-001.txt", "r").read()
    prompt = str(project_data) + "\n" + prompt
    messages = [
        {"role": "user", "content": prompt},
    ]

    # Generate the script using chat completion
    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, temperature=0.7
    )

    # Step 3: Read the second prompt
    second_prompt = open("prompt-video-script-006.txt", "r").read()
    
    second_prompt = response.choices[0].message.content + "\n" + second_prompt

    # Prepend the response from the first API call to the second prompt
    video_script = client.chat.completions.create(
        model="gpt-4o", messages=[
            {"role": "user", "content": second_prompt},
        ], temperature=0.7
    )

    # Return the generated script
    return video_script.choices[0].message.content
