# AI video generation experiments for Sundai hacks

More info at https://www.sundai.club/projects/0d3fb71a-2aca-4dd0-b385-349e276583bb

## Installation

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your OpenAI API key and Replicate API token to the .env file.

OpenAI is used to generate the video script (textual description).  
Replicate is used to generate the video (mp4 and also animated gif).

## Usages

```
python main.py --help
python main.py --dump-all-projects  # saved all projects to output/all_projects.csv
python main.py --project-id 34dffa61-f90e-4184-a034-7bb5ab4f0981 --no-video  # generates only the script
python main.py --project-id 34dffa61-f90e-4184-a034-7bb5ab4f0981  # generated both script and video
```

Project ID can be found in the URL of the project page, for example `34dffa61-f90e-4184-a034-7bb5ab4f0981` at https://www.sundai.club/projects/34dffa61-f90e-4184-a034-7bb5ab4f0981.