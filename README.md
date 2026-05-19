# LeetCode Auto-Sync Tool

A Python script that automatically fetches your accepted LeetCode submissions and synchronizes them to a GitHub repository, complete with dynamic profile badges and performance statistics!

## Features
- **Zero-Friction Sync:** Automatically creates and organizes folders for your problems.
- **Multi-Language Support:** Syncs all unique accepted languages (Python, C++, Java, etc) per problem.
- **Runtime & Memory Stats:** Automatically extracts and injects your execution time and memory usage into each problem's README.
- **Profile Badges:** Dynamically generates a Master README with your LeetCode stats card.

## Setup Instructions

1. **Install Python Requirements:**
   Make sure you have Python installed, then install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Rename `.env.example` to `.env` and fill in your details:
   - `GITHUB_PAT`: Your GitHub Personal Access Token (requires `repo` permissions).
   - `GITHUB_REPO`: The name of the repository to sync to (e.g., `cp-solutions`). The script will automatically create it if it doesn't exist!
   - `LEETCODE_SESSION`: Your LeetCode `LEETCODE_SESSION` cookie.
   - `LEETCODE_CSRF_TOKEN`: Your LeetCode `csrftoken` cookie.
   - `LEETCODE_USERNAME`: Your LeetCode username (used to generate your dynamic profile badge).

3. **Run the Script:**
   ```bash
   python main.py
   ```

## Note on Codeforces
Codeforces synchronization is best handled using the [cf-pusher](https://github.com/SarJ2004/cf-pusher) Chrome Extension, as Codeforces' strict Cloudflare Turnstile blocks automated Python scripts from reading submission source code.
