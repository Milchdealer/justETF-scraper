# lyxoretf-scraper
Scrapes prices from lyxoretf. Just for my personal usage.

# Installation
Make sure you use a virtual env or similiar.
```sh
pip install -r requirements.txt
```

# Usage
```
>>> python3 src/main.py -h
usage: main.py [-h] [--isin_file ISIN_FILE] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --isin_file ISIN_FILE, -i ISIN_FILE
                        Path to file which contains the ISINs to scrape from lyxoretf.de
  --output OUTPUT, -o OUTPUT
                        Where to write the results
```

# Docker
You can also just run it via docker.

```sh
# Build
docker build -t lyxoretf-scraper .

# Run
docker run --rm -v `pwd`:/usr/src/app/out -t lyxoretf-scraper
```
