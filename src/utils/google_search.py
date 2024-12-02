import os
import sys
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from config import update_config
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

env_path = os.path.join(os.path.expanduser("~"), ".aipat.env")
load_dotenv(env_path)

GOOGLE_CSE_ID=os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_URL=os.getenv("GOOGLE_SEARCH_URL")

if not GOOGLE_CSE_ID or not GOOGLE_API_KEY:
    print("Google API keys are missing! Please check your configuration.")
    env_path = os.path.join(os.path.expanduser("~"), ".aipat.env")
    update_config(env_path)
    sys.exit(1)

searchAPI = GoogleSearchAPIWrapper(google_cse_id=GOOGLE_CSE_ID, google_api_key=GOOGLE_API_KEY)

def get_full_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = " ".join(p.get_text() for p in paragraphs[:11])
        return content
    except requests.RequestException as e:
        pass

def should_search(query):
    keywords = ["search", "find", "lookup", "google", "information about", "details on", "more about"]
    return any(keyword in query.lower() for keyword in keywords)

def google_search(query):
    if not should_search(query):
        return "Search not required for this query."

    results = searchAPI.results(query, num_results=5)
    answer = ""
    for result in results:
        full_content = get_full_content(result['link'])
        result['full_content'] = full_content
        answer += (f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\nFull Content: {result['full_content']}\n\n")

    return answer

search_tool = Tool(
    name="Google Search Snippets, Titles, and Links",
    func=google_search,
    description="Search Google for recent results if the query suggests it."
)
