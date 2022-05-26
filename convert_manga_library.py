import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Converts a library exported from tachiyomi to a more compact format")
    parser.add_argument("-s", "--source", help="Directory which contains the library")
    parser.add_argument("-o", "--output", help="Output directory, the script will skip already converted chapters")

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

    for source in tachi_dir.iterdir():
        if source.is_file():
            continue

        for manga in source.iterdir():

            if manga.is_file():
                continue

            manga_out = output_dir / manga.name

            for chapter in manga.iterdir():

                chapter_out = (manga_out / chapter.name).with_suffix(".cbz")

                if chapter_out.exists():
                    continue

                command = ["comic-enc", "encode", "--compress-webp", "-o", f'"{chapter_out}"', f'"{chapter}"', "single"]
                print(f"Running command {' '.join(command)}")


if __name__ == "__main__":
    main()
