#!/usr/bin/env python

import re
from argparse import ArgumentParser
from collections import Counter
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
from dateutil.parser import parser as time_parser, parserinfo


def counter_str(counter: Counter) -> str:
    return ", ".join([f"{x}: {counter[x]}" for x in counter])


def parse_data(path: Path) -> pd.DataFrame:
    cols = ["timestamp", "user", "message"]
    rows = []
    parser = time_parser(info=parserinfo(dayfirst=True))
    line_regex = re.compile("(.+)\\s(\\d{1,2}:\\d{2}.*?)\\s+-\\s+(.+?):\\s+(.+)")
    last_message = None
    multiline = False
    with open(str(path), "r", encoding="utf-8") as file:
        for line in file:
            match = line_regex.match(line)
            if match:
                if multiline:
                    # print(last_message)
                    # print("-" * 30)
                    rows[-1][2] = last_message
                    multiline = False

                timestamp = parser.parse(f"{match[1]} {match[2]}")

                rows.append([timestamp, match[3], match[4]])
                last_message = match[4]
            else:
                if last_message is not None:
                    if not multiline:
                        multiline = True
                    last_message = f"{last_message}{line}"

    conversation_data = pd.DataFrame(data=rows, columns=cols)
    return conversation_data


def analyze(conversation_data: pd.DataFrame, verbose: bool, timelapse=timedelta(hours=6)):
    last_timestamp: Optional[timedelta] = None
    last_sender = None
    enders = Counter()
    starters = Counter()

    # Alternative to calculate hours
    # timestamps: pd.Series = conversation_data.loc[:, "timestamp"]
    # passed_times: pd.Series = timestamps.iloc[1:].reset_index(drop=True)\
    #     .sub(timestamps.iloc[:-1].reset_index(drop=True))
    # print(passed_times)
    # avg = passed_times.mean()
    # std = passed_times.std()
    # print(avg, std)

    for i, (timestamp, user, _) in conversation_data.iterrows():
        if last_timestamp:
            time_passed = timestamp - last_timestamp
            if time_passed > timelapse:
                enders.update([last_sender])
                starters.update([user])
                if verbose:
                    print(f"{last_sender} send the last message and {user} responded until {time_passed} later")
        else:
            starters.update([user])
        last_timestamp = timestamp
        last_sender = user

    print(f"Who starts the conversation: {counter_str(starters)}")
    print(f"Who finishes the conversation: {counter_str(enders)}")


def main():
    parser = ArgumentParser()
    parser.add_argument("file", help="File of the Whatsapp conversation")
    parser.add_argument("--hours", help="How many hours to consider when a conversation has finished", type=int,
                        default=6)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)

    if not path.exists():
        print("Cannot find file")
        exit(1)

    if path.is_dir():
        print("Cannot use a directory")
        exit(1)

    df = parse_data(path)
    print(f"There are {df.shape[0]} messages in the conversation")

    hours = timedelta(hours=args.hours)

    analyze(df, args.verbose, hours)


if __name__ == '__main__':
    main()
