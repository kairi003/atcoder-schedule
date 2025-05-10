import argparse
import json
import warnings
import zoneinfo
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description="Get upcoming AtCoder contests.")
    parser.description = "CLI tool to get the schedule of AtCoder contests"
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default="ja",
        choices=["ja", "en"],
        help="Language for the contest page",
    )
    parser.add_argument(
        "-z",
        "--timezone",
        type=str,
        default="Asia/Tokyo",
        help="Timezone for the contest start time",
    )
    args = parser.parse_args()

    URL = f"https://atcoder.jp/contests/?lang={args.lang}"
    soup = BeautifulSoup(requests.get(URL).text, "lxml")
    table = soup.select_one("#contest-table-upcoming tbody")
    for tr in table.find_all("tr"):
        try:
            dt = datetime.fromisoformat(tr.select_one("td:nth-of-type(1) time").text)
            tz = zoneinfo.ZoneInfo(args.timezone)
            data = {
                "start_time": dt.astimezone(tz).isoformat(),
                "timestamp": int(dt.timestamp()),
                "name": tr.select_one("td:nth-of-type(2) a").text,
                "url": tr.select_one("td:nth-of-type(2) a")["href"],
                "duration": tr.select_one("td:nth-of-type(3)").text,
                "rated_range": tr.select_one("td:nth-of-type(4)").text,
            }
            print(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            warnings.warn(f"Error parsing row: {e}", stacklevel=2)
            continue


if __name__ == "__main__":
    main()
