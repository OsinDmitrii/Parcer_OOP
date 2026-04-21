from __future__ import annotations

import argparse
import json

from iptv_parser import IPTVManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ООП-проект для парсинга Free-TV/IPTV и сохранения данных в TXT."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("countries", help="Вывести все доступные страны")

    countries_save = subparsers.add_parser("countries-save", help="Сохранить список стран в TXT")
    countries_save.add_argument("--filename", default="countries.txt")

    export_country = subparsers.add_parser(
        "export-country",
        help="Сохранить каналы страны в M3U-структуре (#EXTM3U + #EXTINF/URL)",
    )
    export_country.add_argument("country")
    export_country.add_argument("--filename", default=None)

    export_country_blocks = subparsers.add_parser(
        "export-country-blocks",
        help="Алиас export-country: сохранить каналы страны в M3U-структуре",
    )
    export_country_blocks.add_argument("country")
    export_country_blocks.add_argument("--filename", default=None)

    subparsers.add_parser(
        "export-all-countries",
        help="Сохранить каналы всех стран в M3U-структуре (*_channels.txt)",
    )

    groups = subparsers.add_parser("groups", help="Показать группы каналов по стране")
    groups.add_argument("country")

    search = subparsers.add_parser("search", help="Поиск каналов по стране")
    search.add_argument("country")
    search.add_argument("query")

    stats = subparsers.add_parser("stats", help="Показать статистику по стране")
    stats.add_argument("country")

    parser.add_argument("--output-dir", default="output")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    manager = IPTVManager(output_dir=args.output_dir)

    if args.command == "countries":
        for country in manager.list_countries():
            print(country)
        return

    if args.command == "countries-save":
        path = manager.save_countries_to_txt(filename=args.filename)
        print(f"Сохранено: {path}")
        return

    if args.command == "export-country":
        path = manager.save_country_playlist_to_txt(args.country, filename=args.filename)
        print(f"Сохранено: {path}")
        return

    if args.command == "export-country-blocks":
        path = manager.save_country_as_m3u_blocks_txt(args.country, filename=args.filename)
        print(f"Сохранено: {path}")
        return

    if args.command == "export-all-countries":
        paths = manager.save_all_countries_playlists_to_txt()
        for path in paths:
            print(f"Сохранено: {path}")
        return

    if args.command == "groups":
        for group in manager.get_groups(args.country):
            print(group)
        return

    if args.command == "search":
        results = manager.search_channels(args.country, args.query)
        if not results:
            print("Ничего не найдено")
            return
        for item in results:
            print(item.to_readable_text())
            print("-" * 80)
        return

    if args.command == "stats":
        print(json.dumps(manager.get_stats(args.country), ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
