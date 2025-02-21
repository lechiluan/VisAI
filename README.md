# Y4A-Hackathon-2025

## Python Version is 3.10.5

## Installation

**1. Clone Repository & Install Packages**

```sh
git clone "project_url"
pip install virtualenv
```

**2. Setup Virtualenv And Install Requirements**

```sh
# For Windows
virtualenv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

```sh
# Fix Bug When Can Not Active Virtualenv ENV in Windows
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

```sh
# For macOS & Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Create a .env file**

```sh
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

**4. Start Server**

```sh
python main.py
```
