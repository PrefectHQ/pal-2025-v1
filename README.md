# Prefect Accelerated Learning (PAL) Labs

Welcome to the repository for the **Prefect Accelerated Learning (PAL)** program — a six-part series designed to help you quickly gain confidence with Prefect through a mix of guided lessons and interactive examples.

Each module in this repository corresponds to a video in the PAL series and contains code samples that reinforce key concepts such as:

- Writing and deploying flows
- Observing and managing state
- Using caching, artifacts, and notifications
- Creating work pool-based deployments
- Designing scalable workflow patterns
- Building advanced automation and concurrency controls

> 🎓 This repository also open-sources the **Prefect Associate Certification Course** content (created by @discdiver), making it freely available for the community to explore, learn from, and build upon.

📺 **Watch the full video series on YouTube:**  
[Prefect Accelerated Learning (PAL) Playlist](https://youtube.com/playlist?list=PLZfWmQS5hVzFBrwj2k4WGxelQtKrNyAwo&feature=shared)

---

## Prereq Checklist

### Accounts Required
- Prefect Cloud account  
- GitHub account

### Editor
Please install a code editor prior to the start of instruction — [Visual Studio Code (VS Code)](https://code.visualstudio.com/) is a good option. 
Any code editor you are comfortable with is fine.

### Set Up Your Environment

We strongly recommend using a virtual environment to isolate your project dependencies. You can use any of the following tools:

- **`uv`** – A modern Python package manager with fast environment creation  
  [Set up a `uv` environment →](https://docs.astral.sh/uv/getting-started/installation/)

- **`venv`** – Python’s built-in virtual environment tool  
  [Official `venv` docs →](https://docs.python.org/3/library/venv.html)  
  [Real Python guide →](https://realpython.com/python-virtual-environments-a-primer/)

- **`conda`** – A popular environment and package manager, especially in data science workflows  
  [Manage environments with `conda` →](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

Make sure you have **Python 3.9 or newer** installed in your environment.

### Install Prefect
In the terminal with your virtual environment activated, run:

```bash
pip install -U prefect
# or, if using uv:
uv pip install -U prefect
````

To verify the installation, run:

```bash
prefect version
```

If you don’t see any results, Prefect is not installed in your active environment. You may need to activate your virtual environment.

If you have any issues installing Prefect, refer to the [installation guide](https://docs.prefect.io/v3/get-started/install).

### Test Prefect Setup

1. Create a file named `flowtest.py` with the following contents:

   ```python
   import httpx
   from prefect import flow

   @flow
   def test_flow():
       res = httpx.get("https://example.com")
       print(res)

   if __name__ == "__main__":
       test_flow()
   ```

2. Run the script:

   ```bash
   python flowtest.py
   ```

   You should see:

   ```
   <Response [200 OK]>
   ```

### (Optional) Install Docker

Install [Docker](https://www.docker.com/products/docker-desktop/) on your machine. Docker is used for one of the modules. If you don’t have Docker installed, that’s okay, you’ll have other options for running workflows.

