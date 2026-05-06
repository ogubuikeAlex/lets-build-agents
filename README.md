To install uv, use the standalone installer for your operating system to ensure it's available globally and can manage your Python versions for you. [1, 2] 
## 1. Installation
pip install uv [3, 4, 5] 

------------------------------
## 2. Basic Commands
uv has two ways to operate: the Project API (modern, recommended) and the pip-compatibility API (familiar pip syntax). [6, 7] 
## Managing Projects (Modern Workflow)
These commands automatically manage your virtual environment and pyproject.toml file. [6] 

* Start a new project: uv init my-project (Creates a folder with basic files like pyproject.toml).
* Add a package: uv add requests (Installs it and adds it to your project files).
* Remove a package: uv remove requests.
* Run a script: uv run main.py (Runs the script inside the project's isolated environment).
* Sync environment: uv sync (Ensures your local environment matches your lockfile). 

## Using the pip Style (Legacy Compatibility) [13] 
If you just want a faster version of pip for one-off tasks:

* Install a package: uv pip install requests.
* Install from file: uv pip install -r requirements.txt.
* List installed packages: uv pip list. [6, 8, 12, 14, 15] 

------------------------------
## 3. Creating a requirements.txt
In the uv ecosystem, you typically use a uv.lock file for reproducibility, but you can export to a standard text file if needed: [16] 

* Generate requirements.txt from project:
uv export --format requirements.txt --output-file requirements.txt

* Convert a pyproject.toml to requirements.txt (pip-style):
uv pip compile pyproject.toml -o requirements.txt

* The "old way" (like pip freeze):
uv pip freeze > requirements.txt. [8, 15, 17, 18] 

Pro Tip: If you have an existing requirements.txt and want to migrate to uv, run uv add -r requirements.txt. This will import those dependencies into a new uv-managed project automatically. 

# Models I Can USe For Free
- Gemini 1.5 Flash: Optimized for speed and high-volume tasks (Free: 15 RPM, 1 million TPM, 1,500 RPD).
- Gemini 1.5 Pro: Best for complex reasoning and multimodal tasks (Free: 2 RPM, 32,000 TPM, 50 RPD).- Gemini 1.0 Pro: A stable, versatile older model (Free: 15 RPM, 32,000 TPM, 1,500 RPD).
- Gemini 1.5 Flash-8B: A highly efficient, smaller model for lighter workloads