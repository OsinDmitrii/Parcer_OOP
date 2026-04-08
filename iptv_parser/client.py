from __future__ import annotations

import re
from typing import List

import requests


class GitHubPlaylistClient:
    """Клиент для получения списка стран и m3u8-файлов из репозитория Free-TV/IPTV."""

    README_RAW_URL = "https://raw.githubusercontent.com/Free-TV/IPTV/master/README.md"
    ALL_PLAYLIST_URL = "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8"
    COUNTRY_PLAYLIST_TEMPLATE = (
        "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_{slug}.m3u8"
    )

    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (compatible; IPTVParserBot/1.0; +https://github.com/Free-TV/IPTV)"
                )
            }
        )

    def fetch_readme(self) -> str:
        response = self.session.get(self.README_RAW_URL, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def get_country_slugs(self) -> List[str]:
        text = self.fetch_readme()
        slugs = re.findall(r"lists/([a-z_]+)\.md", text)
        seen = set()
        unique = []
        for slug in slugs:
            if slug not in seen:
                seen.add(slug)
                unique.append(slug)
        return unique

    @staticmethod
    def slug_to_country_name(slug: str) -> str:
        return slug.replace("_", " ").title()

    def get_country_names(self) -> List[str]:
        return [self.slug_to_country_name(slug) for slug in self.get_country_slugs()]

    def resolve_country_slug(self, country_name: str) -> str:
        normalized = country_name.strip().lower().replace(" ", "_")
        available = self.get_country_slugs()
        if normalized in available:
            return normalized
        raise ValueError(
            f"Страна '{country_name}' не найдена. Используйте метод вывода доступных стран."
        )

    def fetch_playlist_text(self, country: str | None = None) -> tuple[str, str, str]:
        if country:
            slug = self.resolve_country_slug(country)
            url = self.COUNTRY_PLAYLIST_TEMPLATE.format(slug=slug)
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return self.slug_to_country_name(slug), url, response.text

        response = self.session.get(self.ALL_PLAYLIST_URL, timeout=self.timeout)
        response.raise_for_status()
        return "All", self.ALL_PLAYLIST_URL, response.text
