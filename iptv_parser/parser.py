from __future__ import annotations

import re
from typing import Dict, Iterable

from .models import ChannelEntry, Playlist


class M3UParser:
    EXTINF_NAME_PATTERN = re.compile(r",(.*)$")
    ATTRIBUTE_PATTERN = re.compile(r'([\w-]+)="([^"]*)"')

    def parse(self, content: str, source_name: str, source_url: str, country: str | None = None) -> Playlist:
        playlist = Playlist(source_name=source_name, source_url=source_url, country=country)
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#EXTINF"):
                extinf = line
                url = lines[i + 1] if i + 1 < len(lines) else ""
                if not url or url.startswith("#"):
                    i += 1
                    continue

                attrs = self._parse_attributes(extinf)
                name = self._parse_channel_name(extinf)
                entry = ChannelEntry(
                    name=name,
                    url=url,
                    tvg_id=attrs.get("tvg-id"),
                    tvg_name=attrs.get("tvg-name"),
                    tvg_logo=attrs.get("tvg-logo"),
                    group_title=attrs.get("group-title"),
                    country=country,
                    raw_extinf=extinf,
                    attributes=attrs,
                )
                playlist.add_channel(entry)
                i += 2
                continue
            i += 1
        return playlist

    def _parse_attributes(self, extinf_line: str) -> Dict[str, str]:
        return {key: value for key, value in self.ATTRIBUTE_PATTERN.findall(extinf_line)}

    def _parse_channel_name(self, extinf_line: str) -> str:
        match = self.EXTINF_NAME_PATTERN.search(extinf_line)
        return match.group(1).strip() if match else "Unknown"

    @staticmethod
    def deduplicate(channels: Iterable[ChannelEntry]) -> list[ChannelEntry]:
        seen = set()
        result = []
        for channel in channels:
            key = (channel.name.casefold(), channel.url)
            if key not in seen:
                seen.add(key)
                result.append(channel)
        return result
