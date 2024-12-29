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
    # model = "minimax/video-01" # output['url']
    model = "lightricks/ltx-video:c441c271f0cfd578aa0cd14a8488329dd10b796313a9335573a4a63507a976a5" # output[0]
    output = client.run(model, input={"prompt": script, "prompt_optimizer": True})
    print(output)
    print(output[0])
    return output[0]


def generate_video_script(project_data):
    """Generate a video script using OpenAI"""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Prepare the messages
    messages = [
        {
            "role": "system",
            "content": """You are a professional video script writer. Create an engaging video script based on the project details provided.
            The script should be creative, informative, and suitable for a 2-3 seconds video.
            Include sections for visuals and narration.""",
        },
        {
            "role": "user",
            "content": f"""Project Details:
            Title: {project_data.get("title", "")}
            Preview: {project_data.get("preview", "")}
            Description: {project_data.get("description", "")}
            Tech Tags: {project_data.get("techTags", [])}
            Domain Tags: {project_data.get("domainTags", [])}
            
            Please create a video script that showcases this project effectively.""",
        },
    ]

    # Generate the script using chat completion
    response = client.chat.completions.create(
        model="gpt-4", messages=messages, temperature=0.7
    )

    # Return the generated script
    return response.choices[0].message.content
