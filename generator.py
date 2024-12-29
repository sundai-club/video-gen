import os
import replicate

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def generate_video(script):
    """Generate a video using Replicate"""
    # Initialize the Replicate client
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    # model, key = "minimax/video-01", "url" # output['url']
    # model, key = "minimax/video-01-live", "url" # output['url'], but you need first_frame_image
    model, key = "lightricks/ltx-video:c441c271f0cfd578aa0cd14a8488329dd10b796313a9335573a4a63507a976a5", 0  # output[0]
    output = client.run(model, input={"prompt": script, "prompt_optimizer": True})
    print(output)
    return output[key]


def generate_video_script(project_data):
    """Generate a video script using OpenAI"""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Prepare the messages
    prompt = open("prompt-video-script.txt", "r").read()
    prompt = prompt.format(**project_data)
    messages = [
        {"role": "user", "content": prompt},
    ]

    # Generate the script using chat completion
    response = client.chat.completions.create(
        model="gpt-4", messages=messages, temperature=0.7
    )

    # Return the generated script
    return response.choices[0].message.content
