import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GITHUB_PAT = os.getenv('GITHUB_PAT')
GITHUB_REPO = os.getenv('GITHUB_REPO')

LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
LEETCODE_CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
LEETCODE_USERNAME = os.getenv('LEETCODE_USERNAME')

def validate_config():
    missing = []
    if not GITHUB_PAT or not GITHUB_REPO:
        print("Error: GITHUB_PAT and GITHUB_REPO must be set in .env")
        return False
        
    if not LEETCODE_SESSION:
        print("Warning: LEETCODE_SESSION not set. LeetCode sync will be skipped.")
        
    return True
