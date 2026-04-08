from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class ChannelEntry:
    name: str
    url: str
    tvg_id: Optional[str] = None
    tvg_name: Optional[str] = None
    tvg_logo: Optional[str] = None
    group_title: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    raw_extinf: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_readable_text(self) -> str:
        lines = [
            f"Канал: {self.name}",
            f"Страна: {self.country or 'Не указана'}",
            f"Группа: {self.group_title or 'Не указана'}",
            f"tvg-id: {self.tvg_id or '—'}",
            f"tvg-name: {self.tvg_name or '—'}",
            f"Логотип: {self.tvg_logo or '—'}",
            f"Язык: {self.language or 'Не указан'}",
            f"URL: {self.url}",
        ]
        return "\n".join(lines)

    def to_m3u_block(self) -> str:
        return f"{self.raw_extinf or ''}\n{self.url}".strip()


@dataclass(slots=True)
class Playlist:
    source_name: str
    source_url: str
    country: Optional[str] = None
    channels: List[ChannelEntry] = field(default_factory=list)

    def add_channel(self, channel: ChannelEntry) -> None:
        self.channels.append(channel)

    def groups(self) -> List[str]:
        return sorted({c.group_title for c in self.channels if c.group_title})

    def channel_names(self) -> List[str]:
        return [c.name for c in self.channels]
