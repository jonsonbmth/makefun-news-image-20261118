# makefun-news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/jonsonbmth/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/jonsonbmth/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page — "THE WORLD TODAY" — summing up the world news of Wednesday 18 November 2026 in a single 1024×1024 image. V2 covers the complete day, including late developments the first version missed: Iran striking U.S. bases in Kuwait, Bahrain and Jordan as the Gulf war widens, Xi hosting Putin in Shenzhen hours before Trump's arrival, Category 5 Cyclone Xavier over the northern Cook Islands, plus 35 more verified stories from six continents and Oceania, a numbered world map, and a sources footer.

## The three lead stories

1. **Gulf war widens.** Iran struck U.S. bases in Kuwait (Ali Al Salem) and Bahrain and fired missiles at Al-Azraq base in Jordan, after U.S. jets hit a missile site on Qeshm Island. U.S. forces sank five Iranian tankers in the Gulf of Oman, Iran said it seized the tanker Ocean Koi, and oil pushed above $100 a barrel.
2. **Xi hosts Putin as Trump lands.** Xi Jinping and Vladimir Putin met in Shenzhen on the eve of a trilateral summit with Donald Trump, who flew in from Manila after the Quad's first leader-level meeting in over two years. Xi pledged to stand against protectionism; Putin attacked Western sanctions.
3. **Cyclone Xavier.** A Category 5 storm with sustained winds of 220 km/h and gusts to 315 km/h lashed the northern Cook Islands, passing 280 km north-east of Pukapuka. Manihiki's wharves were damaged; no casualties were reported.

## What else is on the page

- Five illustrated cards: Peltola wins Alaska (Democrats take the Senate 56–44), Anthropic prices its $83 IPO ($81.3bn raised), Fiji declares a national disaster over drought, Ebola passes 11,000 cases in Congo, and Gaza's truce nears collapse as floods swamp the camps.
- Four stat cards: Nvidia's $115.8bn quarter, Voyager 1 reaching one light-day from Earth, the U.S. losing measles-free status (5,412 cases), and the EU's proposed €45bn loan for Ukraine.
- A numbered world map with 12 locations, from Pukapuka to Brasília.
- "Also on Wednesday": 24 further verified stories, from the Kerch Bridge being hit a third time to Zverev reaching the ATP Finals semis.

38 stories in total. Every story was verified against at least two independent sources and confirmed as 18 November news.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the finished front page, `entry.png`, to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). It verifies the image is exactly 1024×1024, under the 1 MiB limit, and byte-identical to the committed file. Two runs produce byte-identical output.

To rebuild the page from its illustration assets, run `python3 build_page.py` (needs Pillow; it composes the masthead, heroes, cards, dotted world map and lists from `assets/` and writes `entry.png`).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
