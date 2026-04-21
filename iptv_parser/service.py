from __future__ import annotations

from pathlib import Path

from .client import GitHubPlaylistClient
from .exporter import TXTExporter
from .models import ChannelEntry, Playlist
from .parser import M3UParser


class IPTVManager:
    def __init__(self, output_dir: str = "output") -> None:
        self.client = GitHubPlaylistClient()
        self.parser = M3UParser()
        self.exporter = TXTExporter(output_dir=output_dir)

    def list_countries(self) -> list[str]:
        return self.client.get_country_names()

    def save_countries_to_txt(self, filename: str = "countries.txt") -> Path:
        countries = self.list_countries()
        return self.exporter.export_countries(countries, filename=filename)

    def load_playlist(self, country: str | None = None) -> Playlist:
        source_name, url, content = self.client.fetch_playlist_text(country=country)
        return self.parser.parse(content, source_name=source_name, source_url=url, country=country)

    def save_country_playlist_to_txt(self, country: str, filename: str | None = None) -> Path:
        playlist = self.load_playlist(country)
        safe_name = country.lower().replace(" ", "_")
        return self.exporter.export_m3u_blocks(
            playlist.channels,
            filename=filename or f"{safe_name}_channels.txt",
        )

    def save_country_as_m3u_blocks_txt(self, country: str, filename: str | None = None) -> Path:
        return self.save_country_playlist_to_txt(country=country, filename=filename)

    def save_all_countries_playlists_to_txt(self) -> list[Path]:
        paths: list[Path] = []
        for country in self.list_countries():
            paths.append(self.save_country_playlist_to_txt(country))
        return paths

    def search_channels(self, country: str, query: str) -> list[ChannelEntry]:
        playlist = self.load_playlist(country)
        query_cf = query.casefold()
        return [
            channel
            for channel in playlist.channels
            if query_cf in channel.name.casefold()
            or query_cf in (channel.group_title or "").casefold()
        ]

    def get_groups(self, country: str) -> list[str]:
        playlist = self.load_playlist(country)
        return playlist.groups()

    def get_stats(self, country: str) -> dict:
        playlist = self.load_playlist(country)
        groups = {}
        for channel in playlist.channels:
            group = channel.group_title or "Без группы"
            groups[group] = groups.get(group, 0) + 1
        return {
            "country": country,
            "total_channels": len(playlist.channels),
            "unique_groups": len(groups),
            "groups": dict(sorted(groups.items(), key=lambda item: item[0].casefold())),
        }
