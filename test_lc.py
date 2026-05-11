import sys
sys.path.append('.')
from leetcode_scraper import LeetCodeScraper
lc = LeetCodeScraper()
subs = lc.get_accepted_submissions()
if subs:
    print(subs[0])
