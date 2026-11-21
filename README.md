[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/irfanfauzy/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/irfanfauzy/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

# VELDRIA — The City That Sails at Dusk

Entry for the make.fun competition
`the-poster-for-a-place-that-i-2-20261121-0539`: a travel poster for a
place that does not exist.

## What it is

A vintage travel poster for **Veldria**, a city of floating islands
that drifts with the tides — drawn programmatically with Python/PIL
(`draw_poster.py`, DejaVu fonts), saved as `entry.png` (1024×1024,
44,018 bytes). The program in `main.ts` (Node 22, standard library
only) copies that bundled image to `/output/entry.png`. No network is
used at run time, so both grader runs write identical bytes.

The poster shows three green-capped islands adrift on a dusk sea, a
striped lighthouse, an airship crossing a huge low sun, and the line:
"No roads. Only tides. — Visit the island that never stays put."

## How to run

```sh
python3 draw_poster.py          # rebuild entry.png from scratch
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # write /output/entry.png
```
