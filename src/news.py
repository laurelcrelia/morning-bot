"""Get the latest news articles from YLE API.
"""
import os
import requests

class NewsAPIError(Exception):
    "Custom exception for News API errors"


def get_news(page, numbers):
    try:
        url = f"https://external.api.yle.fi/v1/teletext/pages/{page}.json"
        params = {
            "app_id": os.getenv("YLE_API_ID"),
            "app_key": os.getenv("YLE_API_KEY")
        }
        response = requests.get(url, params=params)
        data = response.json()

        used_numbers = []

        articles = []
        lines = []
        subpages = data.get("teletext", {}).get("page", {}).get("subpage", [])
        for subpage in subpages:
            content = subpage.get("content", [])
            for item in content:
                line= item.get("line", [])
                lines.append(line)
                for line in lines:
                    for entry in line:
                        if int(entry.get("number")) > 4: 
                            text = entry.get("Text", "").strip()
                            if used_numbers == numbers:
                                break
                            if text[:3] in [str(num) for num in numbers]:
                                articles.append(text[4:].strip())
                                used_numbers.append(int(text[:3]))
        return articles
    except Exception as e:
        raise NewsAPIError(str(e))

def get_domestic_news():
    return get_news(page=102, numbers=[103, 104, 105, 106, 107, 108, 109])

def get_international_news():
    return get_news(page=130, numbers=[131, 132, 133, 134, 135, 136, 137, 138, 139, 140])

