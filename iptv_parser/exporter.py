from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models import ChannelEntry, Playlist


class TXTExporter:
    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_countries(
        self, countries: list[str], filename: str = "countries.txt"
    ) -> Path:
        path = self.output_dir / filename
        path.write_text("\n".join(countries), encoding="utf-8")
        return path

    def export_playlist_readable(
        self, playlist: Playlist, filename: str | None = None
    ) -> Path:
        safe_name = (playlist.country or playlist.source_name).lower().replace(" ", "_")
        path = self.output_dir / (filename or f"{safe_name}_channels.txt")

        chunks = [
            f"Источник: {playlist.source_url}",
            f"Плейлист: {playlist.source_name}",
            f"Страна: {playlist.country or 'Все'}",
            f"Количество каналов: {len(playlist.channels)}",
            "=" * 80,
        ]
        for channel in playlist.channels:
            chunks.append(channel.to_readable_text())
            chunks.append("-" * 80)

        path.write_text("\n".join(chunks), encoding="utf-8")
        return path

    def export_m3u_blocks(
        self, channels: Iterable[ChannelEntry], filename: str
    ) -> Path:
        path = self.output_dir / filename
        blocks = []
        for channel in channels:
            blocks.append(channel.to_m3u_block())
            blocks.append("")
        path.write_text("\n".join(blocks).strip() + "\n", encoding="utf-8")
        return path

    def export_check_results(
        self, results: list[ChannelCheckResult], filename: str = "channel_check.txt"
    ) -> Path:
        path = self.output_dir / filename
        lines = []
        for result in results:
            status = "WORKING" if result.is_working else "NOT WORKING"
            lines.extend(
                [
                    f"Канал: {result.channel.name}",
                    f"URL: {result.channel.url}",
                    f"Статус: {status}",
                    f"HTTP: {result.status_code if result.status_code is not None else '—'}",
                    f"Ошибка: {result.error or '—'}",
                    f"Итоговый URL: {result.final_url or '—'}",
                    "-" * 80,
                ]
            )
        path.write_text("\n".join(lines), encoding="utf-8")
        return path
