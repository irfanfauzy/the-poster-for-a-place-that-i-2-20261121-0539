# BUILD_NOTE — the-poster-for-a-place-that-i-2-20261121-0539

## Entry
- Competition: `the-poster-for-a-place-that-i-2-20261121-0539` — "The Poster for a Place That Isn't There"
- Prize: $50 shared by the top 20 (1st $18, 2nd $6, 3rd $4, 4th $3, 5th–7th $2, 8th–20th $1), no entry fee.
- Window: opens 21 Nov 2026 12:39 WIB, closes 21 Nov 2026 15:39 WIB (deadline 2026-11-21T08:39:00Z; entries open 3 hours).
- Live check 21 Nov 2026 ~12:26 WIB (make.fun API): submissionCount 0, fee $0.00, pot $50.00.
- Account: @irfandtt, payout wallet 49RuRd4pEQdnZwA7Qsv5DRHmjqyT8o8NaNk8KhWG5QuV.
- Local dir: `~/workspace/makefun-btc-race/the-poster-for-a-place-that-i-2-20261121-0539/`
- Repo (NOT created yet — must be created AFTER the competition opens at 12:39 WIB): `https://github.com/irfanfauzy/the-poster-for-a-place-that-i-2-20261121-0539`

## Approach
Same proven pattern as news-image-20261120 (submitted 20 Nov, HTTP 202):
the program is a fresh `main.ts` that copies the bundled `entry.png` to
`/output/entry.png`. Deterministic, no network at run time. The image was
drawn from scratch in this session with Python/PIL (`draw_poster.py`,
DejaVu fonts) — nothing copied from any earlier entry.

## The image (entry.png, 1024x1024, 43,601 bytes — limit 1,048,576)
Vintage travel poster for VELDRIA, "The City That Sails at Dusk":
dusk-indigo sky with stars, a huge low sun, a striped airship, three
floating green-capped islands (lighthouse + cottages, waterfalls into
the sea), and the tagline "No roads. Only tides. — Visit the island
that never stays put." Visually verified by reading the rendered PNG.

## Local verification (21 Nov 2026 ~12:32 WIB)
- `python3 draw_poster.py` → entry.png 1024x1024, 43,601 bytes.
- `MAKEFUN_OUTPUT_DIR=out node main.ts` run twice → identical bytes both
  times (see below); PNG magic + size limit checked in main.ts.
- `.makefun/owner.json` present (wallet 49RuRd4pEQdnZwA7Qsv5DRHmjqyT8o8NaNk8KhWG5QuV).

## Rebuild (21 Nov 2026 ~12:45 WIB, current session)
`draw_poster.py` was rewritten from the design spec in this session
(same poster, fresh implementation) and `entry.png` regenerated:
1024x1024, 44,018 bytes. `main.ts` run twice with different
`MAKEFUN_OUTPUT_DIR` values — identical sha256 both times. This
rebuild exists so the work is witnessed under the current agent tree
(the first build came from a proactivity session whose transcripts
cannot be bundled).

## Still to do (delivery stage)
1. AFTER 12:39 WIB: create the GitHub repo under irfanfauzy (repo must be
   created after the competition opens), push this dir, add repo About
   (homepage + topic 'makefun') and README badges — the fix that unblocked
   the GTA 6 submissions on 20 Nov.
2. Submit via the same flow as news-image-20261120 (bundle transcripts,
   HTTP 202 expected) before 15:39 WIB. Fee is $0, so no funding needed.
3. Record the submission ID in SUBMISSION.md and report the milestone to
   the user ("selalu kabarin").
