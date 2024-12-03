import json
import requests
import webbrowser
import urllib.parse
from langchain_core.tools import Tool

class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=5):
        """
        Initialize the YouTube search class.
        :param search_terms: Query for searching on YouTube.
        :param max_results: Number of results to fetch.
        """
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        """
        Fetch and parse YouTube search results.
        :return: A list of dictionaries containing video metadata.
        """
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        BASE_URL = "https://www.youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}"

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch YouTube results: {response.status_code}")

        html_content = response.text
        while "ytInitialData" not in html_content:
            html_content = requests.get(url).text

        return self._parse_html(html_content)

    def _parse_html(self, html_content):
        """
        Parse the HTML to extract video metadata from ytInitialData.
        :param html_content: Raw HTML response from YouTube.
        :return: A list of video metadata dictionaries.
        """
        results = []

        try:
            start = html_content.index("ytInitialData") + len("ytInitialData") + 3
            end = html_content.index("};", start) + 1
            json_str = html_content[start:end]
            data = json.loads(json_str)
        except Exception as e:
            raise Exception(f"Error parsing ytInitialData: {e}")

        try:
            for contents in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
                for video in contents["itemSectionRenderer"]["contents"]:
                    if "videoRenderer" in video:
                        video_data = video["videoRenderer"]
                        video_info = {
                            "id": video_data.get("videoId", None),
                            "title": video_data.get("title", {}).get("runs", [{}])[0].get("text", "No Title"),
                            "thumbnails": [thumb["url"] for thumb in video_data.get("thumbnail", {}).get("thumbnails", [])],
                            "long_desc": video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", ""),
                            "channel": video_data.get("longBylineText", {}).get("runs", [{}])[0].get("text", "Unknown Channel"),
                            "duration": video_data.get("lengthText", {}).get("simpleText", "N/A"),
                            "views": video_data.get("viewCountText", {}).get("simpleText", "N/A"),
                            "publish_time": video_data.get("publishedTimeText", {}).get("simpleText", "N/A"),
                            "url": f"https://www.youtube.com/watch?v={video_data.get('videoId', '')}"
                        }
                        results.append(video_info)

                    if len(results) >= self.max_results:
                        return results
        except Exception as e:
            raise Exception(f"Error extracting video data: {e}")

        return results

    def to_dict(self, clear_cache=True):
        """
        Return the search results as a list of dictionaries.
        :param clear_cache: Clear the cached videos after returning the data.
        :return: List of video metadata.
        """
        result = self.videos
        if clear_cache:
            self.videos = []
        return result

    def to_json(self, clear_cache=True):
        """
        Return the search results as a JSON string.
        :param clear_cache: Clear the cached videos after returning the data.
        :return: JSON string of video metadata.
        """
        result = json.dumps({"videos": self.videos}, indent=2)
        if clear_cache:
            self.videos = []
        return result

def youtube_search_with_simplified_playback(query, max_results=5, play_video=False):
    """
    Searches YouTube and optionally plays the first video based on user choice.
    :param query: Search query for YouTube.
    :param max_results: Number of search results to return.
    :param play_video: Boolean indicating whether to play the first video.
    :return: A list of video metadata and optional playback of the first video.
    """
    search = YoutubeSearch(query, max_results=max_results)
    videos = search.to_dict()
    response = ""

    for idx, video in enumerate(videos, start=1):
        response += (
            f"{idx}. {video['title']}\n"
            f"   Channel: {video['channel']}\n"
            f"   Duration: {video['duration']}\n"
            f"   Views: {video['views']}\n"
            f"   Published: {video['publish_time']}\n"
            f"   URL: {video['url']}\n\n"
        )

    if play_video and videos:
        first_video = videos[0]
        webbrowser.open(first_video['url'])
        response += f"\nPlaying the first video: {first_video['title']} (URL: {first_video['url']})\n"

    return response

youtube_tool = Tool(
    name="YouTube Search and Play First Video if Play Video on User Prompt",
    func=lambda query: youtube_search_with_simplified_playback(query=query, max_results=5, play_video=False),
    description="Search YouTube for videos and return the results with link. If play_video is True, play the first video automatically.",
)
