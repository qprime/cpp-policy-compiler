---
description: Fetch YouTube video or playlist transcripts as timestamped markdown. Text only — never downloads audio or video.
argument-hint: <youtube-url> <output-slug>
allowed-tools: Bash(python3 *), Bash(~/.local/venvs/yt-dlp/bin/python *), Bash(~/.local/bin/yt-dlp *), Bash(mkdir *), Bash(ls *), Read, Write, Edit
---

# Fetch YouTube Transcripts

Fetch transcripts from YouTube and write them as timestamped markdown. The output is
a search index — each paragraph is a clickable link back to the video moment.

Arguments: `$ARGUMENTS` — expected as `<youtube-url> <output-slug>`. If the user
invoked `/fetch-yt-transcripts` without both, ask for the missing piece before
running.

## When to use

- User asks to pull transcripts for a video, playlist, course, lecture series, or channel.
- User mentions wanting to "index" or "search" a YouTube resource.
- Source material is video-only and the user wants it queryable from the notes.

## When NOT to use

- User wants to download the video/audio itself → different task, not this command.
- Source has a text version (book, blog, arXiv paper) → store that instead.
- Transcripts are copyrighted or paywalled → ask before proceeding.

## Prerequisites

The script needs `yt-dlp` and `youtube-transcript-api` in a venv. Check for
`~/.local/bin/yt-dlp` first; if it is missing, create it:

```bash
python3 -m venv ~/.local/venvs/yt-dlp
~/.local/venvs/yt-dlp/bin/pip install -q yt-dlp youtube-transcript-api
ln -sf ~/.local/venvs/yt-dlp/bin/yt-dlp ~/.local/bin/yt-dlp
```

## How to run

The bundled script lives at `.claude/skills/fetch-yt-transcripts/fetch.py`. Invoke it
through the venv's Python, from the project root:

```bash
~/.local/venvs/yt-dlp/bin/python .claude/skills/fetch-yt-transcripts/fetch.py \
    <youtube-url> \
    <output-slug>
```

Output lands in `<transcript-root>/<output-slug>/`. The root defaults to
`sources/transcripts/` and is overridden with `--out-root <path>`. The slug becomes
the directory name — pick something short and greppable, e.g.
`3b1b-essence-linalg`, `mit-18.06`, `karpathy-nn-zero-to-hero`.

<!--
TRANSCRIPT ROOT: Project-owned. Default is `sources/transcripts/`.
If this project keeps reference material somewhere else, name that path here and
pass it as `--out-root`. Left unfilled, transcripts land under `sources/` whether
or not that directory means anything in this project.
-->

## Output shape

Each video becomes one markdown file:
- Header with video URL and duration
- Body grouped into ~30-second paragraphs
- Each paragraph prefixed with a timestamp link: `**[2:44](https://youtube.com/watch?v=...&t=164s)** ...`

For playlists, the directory also gets a `README.md` listing all chapters.

## Steps

1. **Confirm scope** — single video or playlist? What slug should the directory use?
   If `$ARGUMENTS` is missing either piece, ask.
2. **Run the fetch script** from project root.
3. **Check the output** — count files, spot-check one transcript, verify timestamps work.
4. **Update the index** — if the project keeps a README over its reference material,
   add a pointer to the new transcript set.
5. **Report** — how many transcripts, total size, any failures.

## Gotchas

- Some videos carry human-submitted transcripts, which are better than auto-generated
  ones. The script takes whatever YouTube returns; it does not choose between them.
- yt-dlp's `--write-auto-sub` path is unreliable without a JS runtime. The script uses
  `youtube-transcript-api` instead, which works directly.
- No video or audio is ever downloaded. If the user asks for those, that's a
  different ask.
- Transcripts are text; they can't replace the visuals. They are an index back to the
  video.
