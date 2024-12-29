import argparse
import requests

from generator import generate_video, generate_video_script


def fetch_sundai_project_data(project_id):
    """Fetch project data from the Sundai API"""
    url = f"https://www.sundai.club/api/projects/{project_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch project data: {response.status_code}")


def main():
    parser = argparse.ArgumentParser(description="Process project ID")
    parser.add_argument(
        "project_id",
        type=str,
        help="Project ID to process, for example 34dffa61-f90e-4184-a034-7bb5ab4f0981",
    )

    args = parser.parse_args()
    project_id = args.project_id

    print(f"Processing project ID: {project_id}")

    try:
        # Fetch project data
        print(f"Fetching project {project_id} data...")
        project_data = fetch_sundai_project_data(project_id)
        print(f"Fetched project: {project_data.get('title', 'N/A')}")

        # Generate video script
        print("Generating video script...")
        script = generate_video_script(project_data)

        # Print the generated script
        print("Generated video script:")
        print("=" * 50)
        print(script)
        print("=" * 50)

        # Genetate video
        print("\nGenerating video...")
        video_url = generate_video(script)
        print(f"Video URL: {video_url}")

    except Exception as e:
        print(f"Error: {str(e)}")  # Add your project processing logic here


if __name__ == "__main__":
    main()
