"""
template.py
-----------

Project Scaffold Generator for Lead Scoring Pipeline

This script generates the folder and module structure for a lead scoring ML project.
It creates all required directories and placeholder Python files, 
ready for incremental development of the pipeline components.

Usage:
------
Simply run the script at the project root:

    python template.py

It will create:
- Folders for source code, notebooks, and pipelines
- Project-level files like requirements.txt, pyproject.toml, dvc.yaml, params.yaml
"""


## -------------------------------------------------------------------------------------------------------------------- ##
from pathlib import Path


## -------------------------------------------------------------------------------------------------------------------- ##
## -----------------------------------------------Project Structure---------------------------------------------------- ##
## -------------------------------------------------------------------------------------------------------------------- ##

PROJECT_NAME = "lead_scoring"

folders = [
    "notebooks",
    f"src/{PROJECT_NAME}/core",
    f"src/{PROJECT_NAME}/utils",
    f"src/{PROJECT_NAME}/config",
    f"src/{PROJECT_NAME}/components",
    f"src/{PROJECT_NAME}/transformers",
    f"src/{PROJECT_NAME}/pipeline",
    f"src/{PROJECT_NAME}/runners"
]

placeholder_files = {
    "notebooks": [".gitkeep"],
    f"src/{PROJECT_NAME}": ["__init__.py"],
    f"src/{PROJECT_NAME}/core": ["__init__.py"],
    f"src/{PROJECT_NAME}/utils": ["__init__.py"],
    f"src/{PROJECT_NAME}/config": ["__init__.py"],
    f"src/{PROJECT_NAME}/components": ["__init__.py"],
    f"src/{PROJECT_NAME}/transformers": ["__init__.py"],
    f"src/{PROJECT_NAME}/pipeline": ["__init__.py"],
    f"src/{PROJECT_NAME}/runners": ["__init__.py"],
    "": [
        "requirements.txt",
        "pyproject.toml",
        "params.yaml",
        "dvc.yaml"
        ]
}

for folder in folders:
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    print(f"Created folder: {path}")

for folder, files in placeholder_files.items():
    for filename in files:
        path = Path(folder) / filename if folder else Path(filename)
        if not path.exists():
            path.touch()
            print(f"Created placeholder file: {path}")

print("\nProject scaffold created successfully!")
print("Next steps:")
print("1. Fetch data from source")
print("2. Start notebook experimentation")
print("3. Add modular scripts to src")
print("4. Orchestrate and evaluate entire ML pipeline")
print("5. Document project flow")


## -------------------------------------------------------------------------------------------------------------------- ##