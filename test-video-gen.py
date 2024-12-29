import os
import replicate 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_video_generation():
    # Test prompt for video generation
    prompt = open('prompt-video-script-003.txt', 'r').read()

    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    model, key = "minimax/video-01", "url" # output['url']
    output = client.run(model, input={"prompt": prompt, "prompt_optimizer": True})
    print(output)
    print(output['url'])
    return output[key]

if __name__ == "__main__":
    test_video_generation()