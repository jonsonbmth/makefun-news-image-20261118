# makefun-news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/jonsonbmth/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/jonsonbmth/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page — "THE WORLD TODAY" — summing up the world news of Wednesday 18 November 2026 in a single 1024×1024 image: the U.S. sinking five Iranian tankers in the Gulf, Xi opening APEC in Shenzhen as Trump and Putin arrive, Category 5 Cyclone Xavier battering the Northern Cook Islands, plus 33 more verified stories from six continents, a numbered world map, and a sources footer.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the finished front page, `entry.png`, to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). It verifies the image is exactly 1024×1024, under the 1 MiB limit, and byte-identical to the committed file. Two runs produce byte-identical output.

To rebuild the page from its photo assets, run `python3 build_page.py` (needs Pillow; it composes the masthead, heroes, cards, dotted world map and lists from `assets/` and writes `entry.png`).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
