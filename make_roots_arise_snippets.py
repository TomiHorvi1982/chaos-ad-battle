#!/usr/bin/env python3
"""
Sepultura — Roots Bloody Roots + Arise snippet creator
Vytvoří MP3 snippety do složky snippets/ pro použití ve hře.
Použití: python3 make_roots_arise_snippets.py
"""

import os
import subprocess
import sys
from pathlib import Path

SNIPPETS_OUT = Path(__file__).parent / "snippets"
ROOTS_BASE   = Path("/Users/maxbook/Documents/Sepultura/Backing tracks/Roots Bloody Roots")
ARISE_BASE   = Path("/Users/maxbook/Documents/Sepultura/Backing tracks/Arise")
SNIPPETS_OUT.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════
# ROOTS BLOODY ROOTS — definice riffů
# Každý riff: (display_name, start_sec, end_sec)
# ═══════════════════════════════════════════════════════════
ROOTS_SONGS = [
    {
        "folder": "01. Roots Bloody Roots-C major-121bpm-440hz",
        "prefix": "Roots_Bloody_Roots",
        "title":  "Roots Bloody Roots",
        "riffs": [
            ("Main_Riff",    0.0,  12.0),
            ("Verse_Groove", 14.0, 26.0),
        ],
    },
    {
        "folder": "02. Attitude-F major-80bpm-440hz",
        "prefix": "Attitude",
        "title":  "Attitude",
        "riffs": [
            ("Main_Riff",  0.0,  12.0),
            ("Chorus",    24.0,  36.0),
        ],
    },
    {
        "folder": "03. Cut-Throat-Bb major-98bpm-443hz",
        "prefix": "Cut_Throat",
        "title":  "Cut-Throat",
        "riffs": [
            ("Intro_Riff", 0.0,  12.0),
            ("Verse",     18.0,  30.0),
        ],
    },
    {
        "folder": "04. Ratamahatta (Feat. David Silveria & Carlinhos Brown)-Bb minor-113bpm-442hz",
        "prefix": "Ratamahatta",
        "title":  "Ratamahatta",
        "riffs": [
            ("Tribal_Intro", 0.0,  14.0),
            ("Main_Groove",  20.0, 32.0),
        ],
    },
    {
        "folder": "05. Breed Apart-D minor-104bpm-444hz",
        "prefix": "Breed_Apart",
        "title":  "Breed Apart",
        "riffs": [
            ("Main_Riff",   0.0,  12.0),
            ("Heavy_Break", 30.0, 42.0),
        ],
    },
    {
        "folder": "06. Straighthate-D major-78bpm-447hz",
        "prefix": "Straighthate",
        "title":  "Straighthate",
        "riffs": [
            ("Main_Groove", 0.0,  14.0),
            ("Chorus",     28.0,  40.0),
        ],
    },
    {
        "folder": "07. Spit-E minor-181bpm-442hz",
        "prefix": "Spit",
        "title":  "Spit",
        "riffs": [
            ("Fast_Riff",   0.0,  10.0),
            ("Verse_Blast", 12.0, 22.0),
        ],
    },
    {
        "folder": "08. Lookaway (Feat. Jonathan Davis, Mike Patton & DJ Lethal)-B minor-71bpm-440hz",
        "prefix": "Lookaway",
        "title":  "Lookaway",
        "riffs": [
            ("Main_Groove", 4.0,  16.0),
            ("Chorus",     36.0,  48.0),
        ],
    },
    {
        "folder": "09. Dusted-D minor-108bpm-440hz",
        "prefix": "Dusted",
        "title":  "Dusted",
        "riffs": [
            ("Main_Riff",  0.0,  12.0),
            ("Verse",     20.0,  32.0),
        ],
    },
    {
        "folder": "10. Born Stubborn-D major-71bpm-444hz",
        "prefix": "Born_Stubborn",
        "title":  "Born Stubborn",
        "riffs": [
            ("Main_Groove", 4.0,  16.0),
            ("Heavy_Part",  30.0, 42.0),
        ],
    },
    {
        "folder": "11. Jasco-D major-110bpm-447hz",
        "prefix": "Jasco",
        "title":  "Jasco",
        "riffs": [
            ("Tribal_Riff", 0.0,  14.0),
            ("Main_Theme",  20.0, 32.0),
        ],
    },
    {
        "folder": "12. Itsári-Db major-179bpm-440hz",
        "prefix": "Itsari",
        "title":  "Itsári",
        "riffs": [
            ("Fast_Intro",  0.0,  10.0),
            ("Main_Groove", 12.0, 22.0),
        ],
    },
    {
        "folder": "13. Ambush-G major-95bpm-448hz",
        "prefix": "Ambush",
        "title":  "Ambush",
        "riffs": [
            ("Main_Riff",  0.0,  12.0),
            ("Verse",     22.0,  34.0),
        ],
    },
    {
        "folder": "14. Endangered Species-D minor-80bpm-440hz",
        "prefix": "Endangered_Species",
        "title":  "Endangered Species",
        "riffs": [
            ("Main_Groove", 0.0,  14.0),
            ("Heavy_Verse", 24.0, 36.0),
        ],
    },
    {
        "folder": "15. Dictatorshit-Eb minor-99bpm-440hz",
        "prefix": "Dictatorshit",
        "title":  "Dictatorshit",
        "riffs": [
            ("Main_Riff",  0.0,  12.0),
            ("Chorus",    28.0,  40.0),
        ],
    },
]

# ═══════════════════════════════════════════════════════════
# ARISE — definice riffů
# Stemy: _Bicí_mixed.mp3 (drums), _Rytmická kytara2_mixed.mp3 (rhythm)
# ═══════════════════════════════════════════════════════════
ARISE_SONGS = [
    {
        "name":   "Arise",
        "prefix": "Arise",
        "title":  "Arise",
        "riffs": [
            ("Main_Riff",    0.0,  12.0),
            ("Heavy_Verse",  18.0, 30.0),
        ],
    },
    {
        "name":   "Dead Embyonic Cells",
        "prefix": "Dead_Embryonic_Cells",
        "title":  "Dead Embryonic Cells",
        "riffs": [
            ("Intro_Blast",  0.0,  10.0),
            ("Main_Groove",  14.0, 26.0),
        ],
    },
    {
        "name":   "Desperate Cry",
        "prefix": "Desperate_Cry",
        "title":  "Desperate Cry",
        "riffs": [
            ("Main_Riff",    0.0,  14.0),
            ("Chorus",       28.0, 40.0),
        ],
    },
    {
        "name":   "Murder",
        "prefix": "Murder",
        "title":  "Murder",
        "riffs": [
            ("Fast_Riff",    0.0,  10.0),
            ("Heavy_Break",  14.0, 26.0),
        ],
    },
    {
        "name":   "Infected Voice",
        "prefix": "Infected_Voice",
        "title":  "Infected Voice",
        "riffs": [
            ("Main_Groove",  0.0,  12.0),
            ("Verse",        20.0, 32.0),
        ],
    },
    {
        "name":   "Subtraction",
        "prefix": "Subtraction",
        "title":  "Subtraction",
        "riffs": [
            ("Main_Riff",    0.0,  12.0),
            ("Chorus",       22.0, 34.0),
        ],
    },
    {
        "name":   "Obscure",
        "prefix": "Obscure",
        "title":  "Obscure",
        "riffs": [
            ("Main_Riff",    0.0,  12.0),
            ("Heavy_Verse",  18.0, 30.0),
        ],
    },
    {
        "name":   "Hunger",
        "prefix": "Hunger",
        "title":  "Hunger",
        "riffs": [
            ("Main_Groove",  0.0,  14.0),
            ("Chorus",       28.0, 40.0),
        ],
    },
    {
        "name":   "Under Siege [Regnum Irae]",
        "prefix": "Under_Siege",
        "title":  "Under Siege",
        "riffs": [
            ("Main_Riff",    0.0,  12.0),
            ("Heavy_Break",  20.0, 32.0),
        ],
    },
    {
        "name":   "C.I.U [Criminals In Uniform]",
        "prefix": "CIU",
        "title":  "C.I.U.",
        "riffs": [
            ("Intro_Groove", 0.0,  12.0),
            ("Main_Riff",    18.0, 30.0),
        ],
    },
    {
        "name":   "Orgasmatron",
        "prefix": "Orgasmatron",
        "title":  "Orgasmatron",
        "riffs": [
            ("Main_Riff",    0.0,  14.0),
            ("Heavy_Verse",  20.0, 32.0),
        ],
    },
]


def ffmpeg_cut(input_file, output_file, start, end):
    """Cut audio with ffmpeg, export as 192kbps MP3."""
    duration = end - start
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-t",  str(duration),
        "-i",  str(input_file),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-af",  "afade=t=in:st=0:d=0.1,afade=t=out:st=" + str(max(0, duration - 0.3)) + ":d=0.3",
        str(output_file),
        "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   ⚠️  ffmpeg error: {result.stderr[:200]}")
        return False
    return True


def combine_drums_roots(song_dir, song_folder_name):
    """Combine Roots drum stems (kick+snare+cymbals+hats+toms) into one track."""
    stems_to_mix = ["kick", "snare", "cymbals", "hat", "toms", "other_kit"]
    prefix = song_folder_name.split("/")[-1].split("-")[0].strip()

    inputs = []
    for stem in stems_to_mix:
        # find matching file
        matches = list(song_dir.glob(f"*-{stem}-*.wav")) + list(song_dir.glob(f"*-{stem}.wav"))
        if matches:
            inputs.append(str(matches[0]))

    if not inputs:
        return None

    if len(inputs) == 1:
        return inputs[0]

    # Mix with ffmpeg amix
    tmp_out = SNIPPETS_OUT / f"_tmp_drums_{prefix}.wav"
    filter_str = f"[{''.join(f'[{i}]' for i in range(len(inputs)))}]amix=inputs={len(inputs)}:normalize=0[out]"
    cmd = ["ffmpeg", "-y"]
    for inp in inputs:
        cmd += ["-i", inp]
    cmd += ["-filter_complex", filter_str, "-map", "[out]", str(tmp_out), "-loglevel", "error"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and tmp_out.exists():
        return str(tmp_out)
    return inputs[0]  # fallback to kick only


def find_roots_stem(song_dir, stem_type):
    """Find rhythm or drums stem in Roots song folder."""
    if stem_type == "rhythm":
        matches = list(song_dir.glob("*-rhythm-*.wav")) + list(song_dir.glob("*-rhythm.wav"))
        return str(matches[0]) if matches else None
    elif stem_type == "drums":
        return combine_drums_roots(song_dir, song_dir.name)
    return None


def find_arise_stem(song_name, stem_type):
    """Find stem file for Arise songs."""
    if stem_type == "rhythm":
        patterns = [
            f"{song_name}_Rytmická kytara2_mixed.mp3",
            f"{song_name}_Rytmická kytara_mixed.mp3",
        ]
    else:  # drums
        patterns = [f"{song_name}_Bicí_mixed.mp3"]

    for p in patterns:
        fp = ARISE_BASE / p
        if fp.exists():
            return str(fp)
    return None


def process_roots():
    print("\n🎸 ROOTS BLOODY ROOTS")
    print("=" * 50)
    created = 0
    skipped = 0

    for song in ROOTS_SONGS:
        song_dir = ROOTS_BASE / song["folder"]
        if not song_dir.exists():
            print(f"⚠️  Složka nenalezena: {song['folder']}")
            continue

        print(f"\n  📀 {song['title']}")

        for riff_name, start, end in song["riffs"]:
            for stem_type in ["rhythm", "drums"]:
                out_name = f"{song['prefix']}_{riff_name}_{stem_type}.mp3"
                out_path = SNIPPETS_OUT / out_name

                if out_path.exists():
                    print(f"     ↩️  {out_name} (přeskočeno)")
                    skipped += 1
                    continue

                stem_file = find_roots_stem(song_dir, stem_type)
                if not stem_file:
                    print(f"     ❌ Stem '{stem_type}' nenalezen")
                    continue

                ok = ffmpeg_cut(stem_file, out_path, start, end)
                if ok:
                    size_kb = out_path.stat().st_size // 1024
                    print(f"     ✅ {out_name} ({size_kb} KB)")
                    created += 1
                else:
                    print(f"     ❌ Chyba při vytváření {out_name}")

        # Cleanup tmp drums mix
        for tmp in SNIPPETS_OUT.glob("_tmp_drums_*.wav"):
            tmp.unlink()

    return created, skipped


def process_arise():
    print("\n\n⚡ ARISE")
    print("=" * 50)
    created = 0
    skipped = 0

    for song in ARISE_SONGS:
        print(f"\n  📀 {song['title']}")

        for riff_name, start, end in song["riffs"]:
            for stem_type in ["rhythm", "drums"]:
                out_name = f"{song['prefix']}_{riff_name}_{stem_type}.mp3"
                out_path = SNIPPETS_OUT / out_name

                if out_path.exists():
                    print(f"     ↩️  {out_name} (přeskočeno)")
                    skipped += 1
                    continue

                arise_key = "Bicí" if stem_type == "drums" else "Rytmická kytara2"
                stem_file = find_arise_stem(song["name"], stem_type)
                if not stem_file:
                    print(f"     ❌ Stem '{arise_key}' nenalezen pro {song['name']}")
                    continue

                ok = ffmpeg_cut(stem_file, out_path, start, end)
                if ok:
                    size_kb = out_path.stat().st_size // 1024
                    print(f"     ✅ {out_name} ({size_kb} KB)")
                    created += 1
                else:
                    print(f"     ❌ Chyba při vytváření {out_name}")

    return created, skipped


if __name__ == "__main__":
    print("⚡ SEPULTURA SNIPPET CREATOR")
    print("Výstup:", SNIPPETS_OUT)

    r_created, r_skipped = process_roots()
    a_created, a_skipped = process_arise()

    total = r_created + a_created
    print(f"\n\n✅ HOTOVO — vytvořeno {total} snippetů")
    print(f"   Roots: {r_created} nových, {r_skipped} přeskočených")
    print(f"   Arise: {a_created} nových, {a_skipped} přeskočených")
    print(f"\n📁 Snippety jsou v: {SNIPPETS_OUT}")
    print("💡 Nahraj je na server přes: https://chaos-ad-battle-production.up.railway.app/admin?pass=chaos1993")
