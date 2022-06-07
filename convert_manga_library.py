#!/usr/bin/env python

import argparse
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List
import requests
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description="Converts a library exported from tachiyomi to a more compact format"
    )
    parser.add_argument(
        "-s", "--source", help="Directory which contains the library", required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory, the script will skip already converted chapters",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--config-file",
        help="Config file with name equivalences for the different series",
        required=False,
    )

    parser.add_argument(
        "-n", "--notify", help="Use ntfy to send a notification", action="store_true"
    )

    args = parser.parse_args()

    tachi_dir = Path(args.source)

    if not tachi_dir.exists() or tachi_dir.is_file():
        print(f"The directory {tachi_dir} does not exists or is not a directory")
        exit(1)

    output_dir = Path(args.output)

    if output_dir.is_file():
        print(
            f"The output directory {output_dir} does not exists or is not a directory"
        )
        exit(1)

    if not output_dir.exists():
        output_dir.mkdir()

    name_map = (
        {} if args.config_file is None else create_name_equivs(Path(args.config_file))
    )

    processed = 0
    processed_list = []
    for source in tachi_dir.iterdir():
        if source.is_file():
            continue

        for manga in source.iterdir():

            if manga.is_file():
                continue

            manga_name = name_map[manga.name] if manga.name in name_map else manga.name

            manga_out = output_dir / manga_name
            if not manga_out.exists():
                manga_out.mkdir()

            for chapter in manga.iterdir():
                chapter_out = manga_out / f"{chapter.name}.cbz"

                if chapter_out.exists():
                    continue

                command = [
                    "comic-enc",
                    "encode",
                    "--compress-webp",
                    "-o",
                    str(chapter_out),
                    str(chapter),
                    "single",
                ]
                print(" ".join(command))
                completed = subprocess.run(command)
                if completed.returncode == 0:
                    processed += 1
                    processed_list.append(f"{manga_name} | {chapter.name}")
                else:
                    chapter_out.with_suffix(".comic-enc-partial").unlink(True)

    if args.notify:
        send_notification(processed, processed_list)


def send_notification(processed_number: int, processed_list: List[str]):
    ntfy_path = Path.home() / ".config" / "ntfy.ini"
    if not ntfy_path.exists():
        print("There is not a ntfy config, skipping sending notifications")
        return

    conf = ConfigParser()
    conf.read(ntfy_path)
    try:
        section = conf["manga_notif"]

        headers = {
            "Title": f"Processed {processed_number} new chapters",
            "Tags": "heavy_check_mark",
        }
        r = requests.post(
            f"{section['server']}/{section['channel']}",
            data="\n".join(processed_list).encode("utf-8"),
            headers=headers,
            auth=(section["user"], section["pass"]),
        )
    except KeyError:
        print("Missing config, skipping notif")


def create_name_equivs(file: Path) -> Dict[str, str]:
    name_map: Dict[str, str] = {}
    rep = ""

    if not file.exists() or file.is_dir():
        print(
            "Config file does not exists or is not valid, using no name equivalencies"
        )
        return name_map

    for line in file.read_text().splitlines():
        if line == "":
            rep = ""
            continue
        if rep == "":
            rep = line
            name_map.update({rep: rep})
            continue

        name_map.update({line: rep})
    return name_map


if __name__ == "__main__":
    main()
