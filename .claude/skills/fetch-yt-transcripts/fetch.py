#!/usr/bin/env python3
"""Fetch YouTube transcripts into timestamped markdown.

Usage:
    fetch.py <youtube-url> <output-slug> [--out-root <path>]

Writes to <out-root>/<output-slug>/ (relative to cwd — run from project root).
Defaults to sources/transcripts/.
Accepts a single video URL or a playlist URL. No audio or video is downloaded.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

YTDLP = os.path.expanduser("~/.local/bin/yt-dlp")


def fmt_ts(sec: float) -> str:
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def slug(title: str) -> str:
    t = re.sub(r"[^\w\s-]", "", title).strip().lower()
    return re.sub(r"[-\s]+", "-", t)[:80]


def list_playlist(url: str) -> list[tuple[int, str, str]]:
    """Return [(index, video_id, title), ...] in playlist order."""
    result = subprocess.run(
        [YTDLP, "--flat-playlist", "--print", "%(playlist_index)s\t%(id)s\t%(title)s", url],
        capture_output=True, text=True, check=True,
    )
    items = []
    for line in result.stdout.strip().splitlines():
        idx_s, vid, title = line.split("\t", 2)
        idx = int(idx_s) if idx_s and idx_s != "NA" else 1
        items.append((idx, vid, title))
    return items


def write_transcript(out_dir: Path, idx: int, vid: str, title: str, single: bool) -> str | None:
    """Fetch one transcript and write as markdown. Returns filename or None on failure."""
    try:
        snips = list(YouTubeTranscriptApi().fetch(vid))
    except Exception as e:
        print(f"  FAILED {vid} ({title}): {e}", file=sys.stderr)
        return None

    prefix = "" if single else f"{idx:02d}-"
    fname = f"{prefix}{slug(title)}.md"
    path = out_dir / fname
    url = f"https://www.youtube.com/watch?v={vid}"
    duration = snips[-1].start + snips[-1].duration

    with path.open("w") as out:
        out.write(f"# {title}\n\n")
        out.write(f"**Video:** [{url}]({url})\n")
        out.write(f"**Duration:** {fmt_ts(duration)}\n\n")
        out.write("Timestamps link back to the YouTube moment.\n\n---\n\n")

        chunk_start = None
        buf: list[str] = []
        for s in snips:
            if chunk_start is None:
                chunk_start = s.start
            buf.append(s.text.replace("\n", " ").strip())
            if s.start - chunk_start >= 30:
                link = f"{url}&t={int(chunk_start)}s"
                text = " ".join(b for b in buf if b)
                out.write(f"**[{fmt_ts(chunk_start)}]({link})** {text}\n\n")
                chunk_start = None
                buf = []
        if buf:
            link = f"{url}&t={int(chunk_start)}s"
            text = " ".join(b for b in buf if b)
            out.write(f"**[{fmt_ts(chunk_start)}]({link})** {text}\n\n")

    return fname


def write_index(out_dir: Path, slug_name: str, url: str, items: list[tuple[int, str, str, str]]) -> None:
    """items: [(idx, vid, title, filename), ...]"""
    path = out_dir / "README.md"
    with path.open("w") as out:
        out.write(f"# Transcripts — {slug_name}\n\n")
        out.write(f"**Source:** [{url}]({url})\n\n")
        out.write("Each file has clickable timestamps that link back to the YouTube moment. ")
        out.write("Grep for a phrase, jump to the timestamp, watch the animation.\n\n")
        out.write("## Chapters\n\n")
        for idx, _vid, title, fname in items:
            out.write(f"{idx}. [{title}]({fname})\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("slug")
    parser.add_argument("--out-root", default="sources/transcripts")
    args = parser.parse_args()

    url, slug_name = args.url, args.slug
    out_dir = Path.cwd() / args.out_root / slug_name
    out_dir.mkdir(parents=True, exist_ok=True)

    is_playlist = "list=" in url or "/playlist" in url
    items = list_playlist(url) if is_playlist else [(1, _extract_vid(url), _fetch_title(url))]
    single = not is_playlist

    print(f"Fetching {len(items)} transcript(s) into {out_dir}")
    written: list[tuple[int, str, str, str]] = []
    for idx, vid, title in items:
        fname = write_transcript(out_dir, idx, vid, title, single)
        if fname:
            written.append((idx, vid, title, fname))
            print(f"  [{idx:02d}] {fname}")

    if len(written) > 1:
        write_index(out_dir, slug_name, url, written)

    print(f"\nWrote {len(written)}/{len(items)} transcripts to {out_dir}")
    if len(written) < len(items):
        return 1
    return 0


def _extract_vid(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not m:
        raise SystemExit(f"Could not extract video ID from {url}")
    return m.group(1)


def _fetch_title(url: str) -> str:
    r = subprocess.run([YTDLP, "--print", "%(title)s", "--skip-download", url],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


if __name__ == "__main__":
    sys.exit(main())
