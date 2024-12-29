import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_video(script):
    """Generate a video using Replicate"""
    # Initialize the Replicate client
    # client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    return None


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
            Include sections for visuals and narration."""
        },
        {
            "role": "user",
            "content": f"""Project Details:
            Title: {project_data.get("title", "")}
            Preview: {project_data.get("preview", "")}
            Description: {project_data.get("description", "")}
            Tech Tags: {', '.join([tag.get("name") for tag in project_data.get("techTags", [])])}
            Domain Tags: {', '.join([tag.get("name") for tag in project_data.get("domainTags", [])])}
            
            Please create a video script that showcases this project effectively."""
        }
    ]

    # Generate the script using chat completion
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    # Return the generated script
    return response.choices[0].message.content
