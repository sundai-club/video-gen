import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_project_data(project_id):
    """Fetch project data from the Sundai API"""
    url = f"https://www.sundai.club/api/projects/{project_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch project data: {response.status_code}")

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

def main():
    # Project ID from the URL
    project_id = "34dffa61-f90e-4184-a034-7bb5ab4f0981"
    
    try:
        # Fetch project data
        print("Fetching project data...")
        project_data = fetch_project_data(project_id)
        
        # Generate video script
        print("\nGenerating video script...")
        script = generate_video_script(project_data)
        
        # Print the generated script
        print("\nGenerated Video Script:")
        print("=" * 50)
        print(script)
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()