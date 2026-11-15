# Gita Pathshala – project files

A Bhagavad Gita learning site covering all 701 verses, with explanations in English, Hindi and Gujarati.
Published as a Claude artifact: https://claude.ai/artifact/8EbfFDCmbtmLSoPnEYGnwH

## Folder layout

| Path | What it is |
|---|---|
| `index.html` | The finished single-page site (~780 KB), served by GitHub Pages. |
| `exp/ch1.json … ch18.json` | Verse explanations, one file per chapter, loaded on demand by the page. 701 entries in total. |
| `pipeline/base.html` | Source page before merging new explanations (contains the verse data, lessons, glossary and the live progress table on the About page). |
| `pipeline/original-exp/` | The explanation files as they were before the 210 new ones were added (491 verses). |
| `pipeline/batches/b*.json` | The 210 newly written explanations (Chapters 10–18), in 36 batch files. |
| `pipeline/missing.json` | The 210 verses that were missing. |
| `pipeline/build.py` | Validates every batch and rebuilds `site/`. Run `python3 -I pipeline/build.py`. |
| `audio-samples/` | The background-tune sample pages (v1 and the softer v2). Not yet part of the site. |

## How the page is built

`index.html` embeds two JSON blocks:

- `<script type="application/json" id="VDATA">`: the 701 verses (chapter `c`, verse `v`, Sanskrit, transliteration).
- `<script type="application/json" id="CDATA">`: lessons, story, chapters, glossary, themes, questions and `expKeys` (the list of verses that have an explanation, which drives the progress table).

Explanations load per chapter from `exp/ch{N}.json`. Each entry is keyed `"chapter.verse"` (for example `"2.47"`):

```
{ "w": [ ...IAST word groups... ],
  "en"|"hi"|"gu": {
    "wm": [...],      // word meanings, same length as "w"
    "tr": "...",      // translation
    "simple", "deep", "ctx": "...",
    "ex": [ , ],      // exactly 2 examples
    "apply", "mis": "...",
    "interp": [[school, text], ...],   // 1–4 items
    "rq": "...", "take": "..." } }
```

## Rebuild and republish

1. Add or edit a batch file in `pipeline/batches/` (same schema as above).
2. `python3 -I pipeline/build.py` checks the schema (key order, `wm` length, 2 examples, 1–4 interpretations) and rewrites `index.html` and `exp/`.
3. Commit and push (GitHub Pages redeploys automatically), mapping each as `"exp/chN.json": path`.

Artifact-published pages are self-contained: external hosts are blocked (Google Fonts excepted), so any audio must be synthesised or embedded as a `data:` URI. Browsers also block autoplay, so music must start on the visitor's first tap.

## Background tune (proposal, not yet built in)

`audio-samples/gita-tune-samples-v2.html` is a Web Audio page with seven soft, synthesised sounds (singing bowl, chimes, soft bansuri in Raag Yaman, music box in Raag Bhupali, harp, chant melody, warm hum). Once a tune is chosen, it goes into `index.html` as an inline script with a mute button, a low default volume, a first-tap start and the choice remembered in `localStorage` (wrapped in try/catch).

## Status

- 701 of 701 verses explained (verified by `build.py`).
- Last published version: 24.
