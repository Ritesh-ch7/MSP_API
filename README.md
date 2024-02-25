# MSP
Automate acknowledgment emails for L1 resources in your company.

## Installation
1. Follow these steps to install and set up MSP:
```bash
# Clone the repository
git clone <git_url>
```
```bash
# Navigate to the project directory
cd <new_cloned_directory>
```
```bash
# Install dependencies
pip install -r requirements.txt
```
## Setting Up Logging Folder and app.log File

### Step 1: Open Terminal

Open your terminal.

### Step 2: Navigate to src Directory

```bash
cd path/to/your/project/src
mkdir logging
cd logging
touch app.log
```
## Configuration
### Step 1: Create a `.env` file in src directory
```bash
#.env
API_KEY = <YOUR_API_KEY>
```
## Start the server
### run this command in terminal 
```bash
uvicorn src.main:app --reload
```



   



