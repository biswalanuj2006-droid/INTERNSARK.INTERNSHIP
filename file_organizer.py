"""
File Organizer Automation
=========================
Uses:    Python, os, shutil (stdlib only — no pip needed!)
Run:     python file_organizer.py
Action:  Scans a folder you choose and moves files into
         sorted subfolders by type.
"""

import os
import shutil
import time
from pathlib import Path

# ── File type map ──────────────────────────────────────────────────────────────
# Add / remove extensions here to customize the organizer.

FILE_TYPES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".svg", ".webp", ".ico", ".tiff", ".heic", ".raw",
    },
    "PDFs": {
        ".pdf",
    },
    "Videos": {
        ".mp4", ".mov", ".avi", ".mkv", ".wmv",
        ".flv", ".webm", ".m4v", ".3gp",
    },
    "Documents": {
        ".doc", ".docx", ".odt", ".txt", ".rtf",
        ".md", ".pages",
    },
    "Spreadsheets": {
        ".xls", ".xlsx", ".csv", ".ods", ".numbers",
    },
    "Presentations": {
        ".ppt", ".pptx", ".odp", ".key",
    },
    "Audio": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".m4a", ".wma", ".opus",
    },
    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".bz2", ".xz", ".iso",
    },
    "Code": {
        ".py", ".js", ".ts", ".html", ".css", ".java",
        ".c", ".cpp", ".h", ".cs", ".php", ".rb", ".go",
        ".rs", ".swift", ".kt", ".sh", ".bat", ".json",
        ".xml", ".yaml", ".yml", ".toml", ".sql",
    },
    "Executables": {
        ".exe", ".msi", ".dmg", ".deb", ".rpm", ".apk",
    },
}

# Build reverse map: extension → folder name
EXT_MAP: dict[str, str] = {}
for folder, exts in FILE_TYPES.items():
    for ext in exts:
        EXT_MAP[ext] = folder

# ── Helpers ────────────────────────────────────────────────────────────────────

def divider(char="─", width=56):
    print("  " + char * width)

def section(title: str):
    print()
    divider("═")
    print(f"  {title}")
    divider("═")

def get_target_folder(ext: str) -> str:
    """Return the destination folder name for a given file extension."""
    return EXT_MAP.get(ext.lower(), "Others")

def safe_move(src: Path, dest_dir: Path, dry_run: bool) -> tuple[bool, str]:
    """
    Move src into dest_dir.
    If a file with the same name already exists, append a timestamp.
    Returns (success, final_filename).
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        timestamp = int(time.time())
        dest = dest_dir / f"{stem}_{timestamp}{suffix}"

    if not dry_run:
        shutil.move(str(src), str(dest))

    return True, dest.name

# ── Core organizer ─────────────────────────────────────────────────────────────

def organize(target_path: Path, dry_run: bool = False) -> dict:
    """
    Scan target_path and move files into subfolders.
    Returns a summary dict.
    """
    if not target_path.exists():
        print(f"\n  [!] Path does not exist: {target_path}")
        return {}
    if not target_path.is_dir():
        print(f"\n  [!] Not a directory: {target_path}")
        return {}

    # Collect only files (not subdirectories, not this script itself)
    script_name = Path(__file__).name
    files = [
        f for f in target_path.iterdir()
        if f.is_file() and f.name != script_name
    ]

    if not files:
        print("\n  No files found to organize.")
        return {}

    summary: dict[str, list[str]] = {}
    errors: list[str] = []

    mode_label = "[DRY RUN] " if dry_run else ""
    print(f"\n  {mode_label}Scanning {len(files)} file(s) in:\n  {target_path}\n")

    for f in sorted(files):
        ext = f.suffix
        folder_name = get_target_folder(ext)
        dest_dir = target_path / folder_name

        try:
            success, final_name = safe_move(f, dest_dir, dry_run)
            if success:
                symbol = "→" if not dry_run else "~"
                print(f"  {symbol}  {f.name:<40}  {folder_name}/")
                summary.setdefault(folder_name, []).append(final_name)
        except Exception as e:
            errors.append(f"{f.name}: {e}")
            print(f"  [!] Failed to move {f.name}: {e}")

    if errors:
        print(f"\n  [!] {len(errors)} error(s) occurred.")

    return summary

# ── Report printer ─────────────────────────────────────────────────────────────

def print_report(summary: dict, dry_run: bool):
    if not summary:
        return
    section("SUMMARY REPORT")
    mode = " (dry run — no files were moved)" if dry_run else ""
    total = sum(len(v) for v in summary.values())
    print(f"  Total files processed{mode}: {total}\n")

    for folder, files in sorted(summary.items()):
        print(f"  {folder}/  ({len(files)} file(s))")
        for name in files:
            print(f"    • {name}")
    print()

# ── Menu actions ───────────────────────────────────────────────────────────────

def run_organizer(dry_run: bool = False):
    label = "DRY RUN (preview only)" if dry_run else "LIVE RUN (files will be moved)"
    section(f"ORGANIZE FILES — {label}")

    raw = input("  Enter folder path to organize\n  (press Enter for current directory): ").strip()
    target = Path(raw) if raw else Path(".")

    target = target.expanduser().resolve()
    print(f"\n  Target: {target}")

    if not dry_run:
        confirm = input("  Confirm? Files will be moved. (y/n): ").strip().lower()
        if confirm != "y":
            print("  Cancelled.")
            return

    summary = organize(target, dry_run=dry_run)
    print_report(summary, dry_run)

def show_type_map():
    section("SUPPORTED FILE TYPES")
    for folder, exts in FILE_TYPES.items():
        ext_list = "  ".join(sorted(exts))
        print(f"  {folder:<16}: {ext_list}")
    print(f"\n  Any other extension → Others/")

def undo_last():
    section("UNDO / RESTORE FILES")
    print("  Undo moves 'Others' folder files back to the parent.")
    raw = input("  Enter the organized folder path: ").strip()
    target = Path(raw).expanduser().resolve() if raw else Path(".")

    moved = 0
    for sub in target.iterdir():
        if not sub.is_dir():
            continue
        for f in sub.iterdir():
            if f.is_file():
                dest = target / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
                    print(f"  ← {sub.name}/{f.name}")
                    moved += 1

    if moved:
        print(f"\n  Restored {moved} file(s) to {target}")
        # Remove empty subdirectories
        for sub in list(target.iterdir()):
            if sub.is_dir() and not any(sub.iterdir()):
                sub.rmdir()
                print(f"  Removed empty folder: {sub.name}/")
    else:
        print("  Nothing to restore.")

# ── Main menu ──────────────────────────────────────────────────────────────────

MENU = """
  ┌──────────────────────────────────────────────┐
  │          FILE ORGANIZER AUTOMATION           │
  ├──────────────────────────────────────────────┤
  │  1  →  Organize a folder (live)              │
  │  2  →  Preview only (dry run)                │
  │  3  →  Show supported file types             │
  │  4  →  Undo / restore files                  │
  │  0  →  Exit                                  │
  └──────────────────────────────────────────────┘
"""

def main():
    print("\n  Welcome to File Organizer Automation")
    print("  No pip install needed — uses Python stdlib only.")

    actions = {
        "1": lambda: run_organizer(dry_run=False),
        "2": lambda: run_organizer(dry_run=True),
        "3": show_type_map,
        "4": undo_last,
    }

    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! Stay organized. 🗂\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("\n  [!] Invalid option. Enter 0–4.")

        input("\n  Press Enter to return to menu...")

if __name__ == "__main__":
    main()