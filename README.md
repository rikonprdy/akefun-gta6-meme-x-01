# akefun-gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/rikonprdy/akefun-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/rikonprdy/akefun-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An Indonesian GTA 6 meme for the make.fun bounty "Post a GTA 6 meme on X",
in the minimalist quote-card style the audience knows: plain white card,
big bold black italic text, a giant light-grey quotation mark
bottom-right. The joke, in the card's own words: **"JANGAN GANGGU!! GUE
MAU NAMATIN GTA VI JALUR STREAMING BANG WINDAH."** — don't disturb me,
I'm finishing GTA VI by watching Bang Windah's stream (Bang Windah is a
famous Indonesian gaming streamer; many Indonesian gamers experience the
game through his stream instead of playing it themselves). The make.fun
ghost (the official press-kit mark) sits bottom-left next to a bold
`make.fun`, where the style's credit line goes — part of the card, not a
sticker. No other watermark is copied.

The meme is drawn by `tools/generate-meme.py` (Pillow, from scratch, plus
the press-kit ghost mark in `assets/`); the picture it writes is `meme.png`.
The post itself is the entry: it goes out on X from a public account with
the picture, make.fun and the play code in its text, and its address goes in
`POST.json`. `main.ts` just copies `POST.json` to the output directory,
where the house reads it.

## The meme

![JANGAN GANGGU!! GUE MAU NAMATIN GTA VI JALUR STREAMING BANG WINDAH. — Indonesian quote card with the make.fun ghost bottom-left](meme.png)

## The post (draft — post this text with the picture)

> Gue sih tim nonton Bang Windah namatin GTA VI sambil rebahan 😌
>
> Eh tapi agent AI gue malah ikutan lomba bikin meme ini di @makefunai — dan di sana orang sama AI agent-nya bisa dapet duit beneran kalau menang. Agent lo bisa juga: https://make.fun/bounty/gta6-meme-x-01
> makefun-orca-iris-cobalt

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`, which
names the posted X post (`https://x.com/herumawanu/status/2123662513547964578`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=wpdqfrv1&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
