"""Get the latest news articles from YLE API.
"""

import os
import requests
from typing import List, Any

class NewsAPIError(Exception):
    "Custom exception for News API errors"


class News():
    def __init__(self) -> None:
        self.api_id = os.getenv("YLE_API_ID")
        self.api_key = os.getenv("YLE_API_KEY")
        self.domestic_news_page = os.getenv("YLE_DOMESTIC_NEWS_PAGE")
        self.international_news_page = os.getenv("YLE_INTERNATIONAL_NEWS_PAGE")
        self.economy_news_page = os.getenv("YLE_ECONOMY_NEWS_PAGE")

    def get_domestic_news(self) -> List[str]:
        numbers = list(range(int(self.domestic_news_page)+1, int(self.international_news_page)))
        return self._get_news(page=self.domestic_news_page, numbers=numbers)

    def get_international_news(self) -> List[str]:
        numbers = list(range(int(self.international_news_page)+1, int(self.economy_news_page)))
        return self._get_news(page=self.international_news_page, numbers=numbers)

    def _get_news(self, page: str, numbers: List[int]) -> List[str]:
        try:
            url = f"https://external.api.yle.fi/v1/teletext/pages/{page}.json"
            params = {
                "app_id": self.api_id,
                "app_key": self.api_key
            }
            response = requests.get(url, params=params)
            data = response.json()

            return self._parse_data(data, numbers)
        except Exception as e:
            raise NewsAPIError(str(e))
    
    def _parse_data(self, data: Any, numbers: List[int]) -> List[str]:
        articles = []
        used_numbers = []
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
                            if used_numbers == numbers or text[:3] in [str(num) for num in used_numbers]:
                                break
                            if text[:3] in [str(num) for num in numbers]:
                                articles.append(text[4:].strip())
                                used_numbers.append(int(text[:3]))
        return articles

