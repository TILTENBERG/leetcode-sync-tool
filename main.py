import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
from github_client import GitHubClient
from leetcode_scraper import LeetCodeScraper
import config
from collections import defaultdict

def generate_master_readme(github_client, lc_metadata):
    readme_content = "# Competitive Programming Solutions\n\n"
    readme_content += "Collection of LeetCode questions to ace the coding interview! - Synced Automatically\n\n"
    
    readme_content += "## Profile Stats\n"
    readme_content += "![LeetCode Stats](https://leetcard.jacoblin.cool/ebaal?theme=dark&font=baloo)\n"
    readme_content += "\n"
    
    if lc_metadata:
        readme_content += "## LeetCode\n\n"
        
        # Group by tags
        lc_by_tag = defaultdict(list)
        for slug, meta in lc_metadata.items():
            for tag in meta['tags']:
                lc_by_tag[tag].append(meta)
                
        # Sort tags and list problems
        for tag in sorted(lc_by_tag.keys()):
            readme_content += f"### {tag}\n"
            # Sort problems by ID numerically if possible
            problems = sorted(lc_by_tag[tag], key=lambda x: int(x['id']) if x['id'].isdigit() else 999999)
            for meta in problems:
                readme_content += f"- [{meta['id']} - {meta['title']}](LeetCode/{meta['slug']}/)\n"
            readme_content += "\n"
            
    github_client.commit_file("README.md", readme_content, "Update master README.md", overwrite=True)

def sync_leetcode(github_client, lc_scraper, existing_files, lc_metadata):
    if not config.LEETCODE_SESSION:
        return
        
    submissions = lc_scraper.get_accepted_submissions()
    for sub in submissions:
        title_slug = sub['title_slug']
        language = sub['lang']
        ext = lc_scraper.get_file_extension(language)
        
        file_path = f"LeetCode/{title_slug}/solution.{ext}"
        readme_path = f"LeetCode/{title_slug}/README.md"
        
        needs_code = file_path not in existing_files
        needs_readme = readme_path not in existing_files
        
        print(f"Checking LeetCode: {title_slug} ({language})")
        details = lc_scraper.get_problem_details(title_slug)
        if details:
            tags = [t['name'] for t in details.get('topicTags', [])]
            if not tags:
                tags = ["Uncategorized"]
                
            lc_metadata[title_slug] = {
                'id': details.get('questionFrontendId', '0'),
                'title': details.get('title', title_slug),
                'slug': title_slug,
                'tags': tags
            }
            
            if needs_readme:
                print(f"Scraping LC statement: {readme_path}")
                runtime = sub.get('runtime', 'N/A')
                memory = sub.get('memory', 'N/A')
                
                readme_content = f"## {details.get('questionFrontendId', '')}. {details.get('title', '')}\n\n"
                readme_content += f"**Difficulty:** {details.get('difficulty', '')}  \n"
                readme_content += f"**Tags:** {', '.join(tags)}\n"
                readme_content += f"**Runtime:** {runtime}  \n"
                readme_content += f"**Memory:** {memory}  \n\n"
                readme_content += details.get('content', '')
                
                github_client.commit_file(readme_path, readme_content, f"Add LeetCode README: {title_slug}")
                existing_files.add(readme_path)
                
        if needs_code:
            print(f"Scraping LC code: {file_path}")
            code = sub.get('code')
            if code:
                github_client.commit_file(file_path, code, f"Add LeetCode solution: {title_slug} ({language})")
                existing_files.add(file_path)
                
        time.sleep(2)

def main():
    if not config.validate_config():
        return

    print("Initializing GitHub Client...")
    try:
        github_client = GitHubClient()
    except Exception as e:
        print(f"Failed to initialize GitHub Client: {e}")
        return

    print("Fetching existing files from repository...")
    existing_files = github_client.get_existing_files()
    print(f"Found {len(existing_files)} existing files in the repo.")

    lc_metadata = {}

    if config.LEETCODE_SESSION:
        lc_scraper = LeetCodeScraper()
        sync_leetcode(github_client, lc_scraper, existing_files, lc_metadata)
    else:
        print("Skipping LeetCode sync (session not provided).")

    print("Generating Master README.md...")
    generate_master_readme(github_client, lc_metadata)

    print("Sync complete!")

if __name__ == "__main__":
    main()
