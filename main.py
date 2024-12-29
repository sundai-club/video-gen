import argparse
import requests
import time
import csv
import sys
import os

from generator import generate_video, generate_video_script


def parse_project(project_data):
    return {
        "id": project_data["id"],
        "title": project_data["title"],
        "preview": project_data["preview"],
        "description": project_data["description"],
        "techTags": ', '.join([tag["name"] for tag in project_data["techTags"]]),
        "domainTags": ', '.join([tag["name"] for tag in project_data["domainTags"]]),
    }

def fetch_sundai_project_data(project_id):
    """Fetch project data from the Sundai API"""
    url = f"https://www.sundai.club/api/projects/{project_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return parse_project(response.json())
    else:
        raise Exception(f"Failed to fetch project data: {response.status_code}")


def all_projects():
    """Fetch all projects from the Sundai API"""
    url = "https://www.sundai.club/api/projects"
    response = requests.get(url)
    if response.status_code == 200:
        return [
            parse_project(project) for project in response.json()
        ]
    else:
        raise Exception(f"Failed to fetch projects: {response.status_code}")


def main():
    os.makedirs("output", exist_ok=True)

    parser = argparse.ArgumentParser(description="Process project ID")
    parser.add_argument(
        "--project-id",
        type=str,
        nargs='?',
        help="Project ID to process, for example 34dffa61-f90e-4184-a034-7bb5ab4f0981",
    )
    parser.add_argument(
        "--dump-all-projects",
        action="store_true",
        help="Export all projects to CSV file",
    )
    parser.add_argument(
        "--no-video",
        action="store_true",
        help="Skip video generation and only create the script",
    )

    args = parser.parse_args()

    if args.dump_all_projects:
        try:
            print("Fetching all projects...")
            projects = all_projects()
            csv_file = "output/all_projects.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'title', 'preview', 'description', 'techTags', 'domainTags'])
                for project in projects:
                    writer.writerow([
                        project['id'],
                        project['title'],
                        project['preview'],
                        project['description'],
                        project['techTags'],
                        project['domainTags']
                    ])
            print(f"Successfully exported {len(projects)} projects to {csv_file}")
            sys.exit(0)
        except Exception as e:
            print(f"Error exporting projects: {str(e)}")
            sys.exit(1)

    if not args.project_id:
        parser.error("project_id is required when not using --dump-all-projects")

    project_id = args.project_id

    print(f"Processing project ID: {project_id}")

    try:
        # Fetch project data
        print(f"Fetching project {project_id} data...")
        project_data = fetch_sundai_project_data(project_id)
        print(f"Fetched project: {project_data.get('title', 'N/A')}")

        timestamp = int(time.time())

        # Generate video script
        print("Generating video script...")
        script = generate_video_script(project_data)

        # Save script to local file
        print("Saving video script to local file...")
        script_filename = f"output/{project_data.get('id')}-{project_data.get('title')}-{timestamp}.txt"
        with open(script_filename, 'w') as f:
            f.write(script)
        print(f"Saved script to {script_filename}")

        # Print the generated script
        print("Generated video script:")
        print("=" * 50)
        print(script)
        print("=" * 50)

        if not args.no_video:
            # Generate video
            print("\nGenerating video...")
            video_url = generate_video(script)
            
            print(f"Video URL: {video_url}")
            # Download video
            print("\nDownloading video...")
            video_filename = f"output/{project_data.get('id')}-{project_data.get('title')}-{timestamp}.mp4"
            video_response = requests.get(video_url, stream=True)
            with open(video_filename, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded video to {video_filename}")
        else:
            print("\nSkipping video generation as --no-video flag was provided")

    except Exception as e:
        print(f"Error: {str(e)}")  # Add your project processing logic here


if __name__ == "__main__":
    main()
