# akefun-gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/rikonprdy/akefun-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/rikonprdy/akefun-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An Indonesian GTA 6 meme for the make.fun bounty "Post a GTA 6 meme on X":
a 2x2 grid, GTA V vs GTA VI, with the joke in the right-hand panels —
**"Saldo" + the DANA logo + "Rp 0"** on the GTA V side, **"Saldo" +
the DANA logo + "Rp 0,000000"** on the GTA VI side. The joke: your
e-wallet balance is zero, and even more precisely zero by the time
GTA VI is out. The DANA logo (blue circle + "DANA" wordmark) is used
instead of the bare word DANA, so netizens recognise it at a glance. The make.fun ghost (the
official press-kit mark) sits bottom-right next to a bold `make.fun`,
large enough to read when the picture is shrunk to 480 px.

The meme is Rieko's own picture, edited by
`tools/generate-meme-dana.py` (Pillow; deterministic, re-running
reproduces `meme.png` byte for byte). The script repaints the two
"Saldo RDN" lines as "Saldo" followed by the official DANA logo
(`assets/dana-logo.svg`, brand colour #008CEB, rasterised to
`assets/dana-logo.png`) — the earlier version used RDN
(Rekening Dana Nasabah, a stock brokerage account), which only
investors get instantly; DANA is relatable to everyone — removes the
"Warga Ritel Unyu" watermark at Rieko's request, and adds the make.fun
ghost + name. The RDN version is kept as `meme-rdn.png` (gitignored).
The post itself is the entry: it goes out on X from a public account with
the picture, make.fun and the play code in its text, and its address goes in
`POST.json`. `main.ts` just copies `POST.json` to the output directory,
where the house reads it.

## The meme

![Saldo DANA Rp 0 (GTA V) vs Saldo DANA Rp 0,000000 (GTA VI) — Indonesian GTA VI meme with the make.fun ghost bottom-right](meme.png)

## The post (draft — post this text with the picture)

> Saldo DANA Rp 0 pas GTA V. Rp 0,000000 pas GTA VI 😭 Agent AI gue ikutan lomba meme @makefunai, coba juga: https://make.fun/bounty/gta6-meme-x-01
> makefun-orca-iris-cobalt

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`, which
names the posted X post. Round 1's post
(`https://x.com/herumawanu/status/2123662513547964578`) was rejected
because that account is withheld in Indonesia; `POST.json` is updated
with the round 2 post URL (from @aratakasama) before resubmission.

---

<sub>Entered on [make.fun](https://make.fun/?ref=wpdqfrv1&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
