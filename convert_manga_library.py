import argparse
from pathlib import Path
from typing import Dict
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Converts a library exported from tachiyomi to a more compact format")
    parser.add_argument("-s", "--source", help="Directory which contains the library", required=True)
    parser.add_argument(
        "-o", "--output", help="Output directory, the script will skip already converted chapters", required=True
    )
    parser.add_argument(
        "-c", "--config-file", help="Config file with name equivalences for the different series", required=False
    )

    args = parser.parse_args()

    tachi_dir = Path(args.source)

    if not tachi_dir.exists() or tachi_dir.is_file():
        print(f"The directory {tachi_dir} does not exists or is not a directory")
        exit(1)

    output_dir = Path(args.output)

    if output_dir.is_file():
        print(f"The output directory {output_dir} does not exists or is not a directory")
        exit(1)

    if not output_dir.exists():
        output_dir.mkdir()

    name_map = {} if args.config_file is None else create_name_equivs(Path(args.config_file))

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
                    chapter_out,
                    chapter,
                    "single",
                ]
                print(" ".join(command))
                subprocess.run(command)


def create_name_equivs(file: Path) -> Dict[str, str]:
    name_map: Dict[str, str] = {}
    rep = ""

    if not file.exists() or file.is_dir():
        print("Config file does not exists or is not valid, using no name equivalencies")
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
