import requests
import json
import time
import config

class LeetCodeScraper:
    def __init__(self):
        self.session_id = config.LEETCODE_SESSION
        self.csrf_token = config.LEETCODE_CSRF_TOKEN
        
        if not self.session_id:
            print("Warning: LEETCODE_SESSION is not set. LeetCode scraping will be skipped.")
            
        self.base_url = "https://leetcode.com"
        self.headers = {
            "Cookie": f"LEETCODE_SESSION={self.session_id};",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        if self.csrf_token:
            self.headers["Cookie"] += f"; csrftoken={self.csrf_token}"
            self.headers["X-CSRFToken"] = self.csrf_token
            self.headers["Referer"] = "https://leetcode.com/submissions/"

    def get_accepted_submissions(self):
        """Fetches all accepted submissions using the REST API."""
        if not self.session_id:
            return []
            
        print("Fetching LeetCode submissions...")
        
        offset = 0
        limit = 20
        all_accepted = []
        # Track by (slug, language) to get latest submission per language
        seen_submissions = set()
        
        while True:
            url = f"{self.base_url}/api/submissions/?offset={offset}&limit={limit}"
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code != 200:
                    print(f"LeetCode API Error: {response.status_code}")
                    break
                    
                data = response.json()
                if 'submissions_dump' not in data:
                    break
                    
                submissions = data['submissions_dump']
                if not submissions:
                    break
                    
                for sub in submissions:
                    if sub.get('status_display') == 'Accepted':
                        slug = sub.get('title_slug')
                        lang = sub.get('lang')
                        identifier = f"{slug}-{lang}"
                        if identifier not in seen_submissions:
                            all_accepted.append(sub)
                            seen_submissions.add(identifier)
                            
                if not data.get('has_next'):
                    break
                    
                offset += limit
                time.sleep(2) # Avoid rate limits
                
            except Exception as e:
                print(f"Error fetching LeetCode submissions: {e}")
                break
                
        print(f"Found {len(all_accepted)} unique accepted LeetCode submissions.")
        return all_accepted

    def get_problem_details(self, title_slug):
        """Fetches problem description, tags, and difficulty via GraphQL."""
        url = f"{self.base_url}/graphql/"
        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionFrontendId
            title
            content
            difficulty
            topicTags {
              name
            }
          }
        }
        """
        variables = {"titleSlug": title_slug}
        try:
            response = requests.post(url, json={"query": query, "variables": variables}, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and data['data'].get('question'):
                    return data['data']['question']
        except Exception as e:
            print(f"Error fetching LeetCode details for {title_slug}: {e}")
        return None

    def get_file_extension(self, language):
        """Maps LC language string to file extension."""
        lang_map = {
            'cpp': 'cpp',
            'java': 'java',
            'python': 'py',
            'python3': 'py',
            'c': 'c',
            'csharp': 'cs',
            'javascript': 'js',
            'ruby': 'rb',
            'swift': 'swift',
            'go': 'go',
            'scala': 'scala',
            'kotlin': 'kt',
            'rust': 'rs',
            'php': 'php',
            'typescript': 'ts',
            'racket': 'rkt',
            'erlang': 'erl',
            'elixir': 'ex',
            'dart': 'dart'
        ext = lang_map.get(language.lower())
        if not ext:
            print(f"Warning: Unknown language '{language}'. Saving as .txt")
            ext = 'txt'
        return ext
