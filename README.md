# Y4A-Hackathon-2025
<img width="1917" height="908" alt="image" src="https://github.com/user-attachments/assets/cca23db5-9c51-4b80-902c-fef78d5dd346" />
<img width="1909" height="909" alt="image" src="https://github.com/user-attachments/assets/aec2a7d5-dbe2-42e0-b474-bc45150c3f63" />

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

**3. Start Server**

```sh
streamlit run main.py
```

**4. Enter OpenAI API Key**

After the app opens, enter your OpenAI API key in the sidebar before using VisAI.
