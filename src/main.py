# *-* coding: utf-8 *-*
"""

"""
import os
import argparse
import json
from datetime import datetime
from typing import Final, Iterator, Dict, Optional, Tuple

import requests
from bs4 import BeautifulSoup

HEADERS: Final[Dict[str, str]] = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
    "cache-control": "max-age=0",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
}


def get_urls(filename: str) -> Iterator[str]:
    with open(filename) as f:
        for line in f:
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            yield line


def parse_price_from_soup(soup: BeautifulSoup) -> Tuple[Optional[float], Optional[str]]:
    try:
        price = soup.find("div", class_="col-xs-6")
        currency, price = price.find_all("span")
        currency = currency.encode_contents().decode("UTF-8")
        price = price.encode_contents().decode("UTF-8")
        price = price.replace(",", ".").replace("EUR", "").strip()
        price = float(price)
    except:
        print("Failed to parse price from website!")
        return None, None

    return price, currency


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--isin_file",
        "-i",
        type=str,
        help="Path to file which contains the ISINs to scrape from lyxoretf.de",
        default=os.path.join("res", "ISINLIST"),
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Where to write the results",
        default=os.path.join("out", datetime.now().isoformat()),
    )
    args = parser.parse_args()

    data = []
    for isin in get_urls(args.isin_file):
        isin = isin.strip()
        url = "https://www.justetf.com/de-en/etf-profile.html?isin=%s" % isin
        response = requests.get(url, headers=HEADERS, timeout=30)

        if response.status_code != 200:
            print(
                "Failed to access site '%s' with error: %s", url, response.status_code
            )
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        price, currency = parse_price_from_soup(soup)
        data.append(
            {
                "ISIN": isin,
                "date": datetime.now().isoformat(),
                "price": price,
                "currency": currency,
            }
        )

    print("Writing results to %s" % args.output)
    with open(args.output, "w") as f:
        json.dump(data, f, ensure_ascii=False)
