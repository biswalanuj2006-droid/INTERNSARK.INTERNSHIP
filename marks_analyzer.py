"""
Student Marks Analyzer
======================
Uses:    Python, pandas, csv
Run:     python marks_analyzer.py
Data:    students.csv  (must be in the same folder)
"""

import pandas as pd
import os
import sys

CSV_FILE = "students.csv"
SUBJECTS = ["Math", "Science", "English", "History", "Computer"]

# ── Grade helper ───────────────────────────────────────────────────────────────

def get_grade(avg: float) -> str:
    if avg >= 90: return "A+"
    if avg >= 80: return "A"
    if avg >= 70: return "B"
    if avg >= 60: return "C"
    if avg >= 50: return "D"
    return "F"

def get_remark(avg: float) -> str:
    if avg >= 90: return "Outstanding"
    if avg >= 80: return "Excellent"
    if avg >= 70: return "Good"
    if avg >= 60: return "Average"
    if avg >= 50: return "Below Average"
    return "Needs Improvement"

# ── Load data ──────────────────────────────────────────────────────────────────

def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        print(f"\n  [!] '{CSV_FILE}' not found in the current folder.")
        print("  Make sure students.csv is in the same directory.")
        sys.exit(1)
    try:
        df = pd.read_csv(CSV_FILE)
        df["Average"] = df[SUBJECTS].mean(axis=1).round(2)
        df["Grade"]   = df["Average"].apply(get_grade)
        df["Remark"]  = df["Average"].apply(get_remark)
        df["Rank"]    = df["Average"].rank(ascending=False, method="min").astype(int)
        return df
    except Exception as e:
        print(f"\n  [!] Error reading CSV: {e}")
        sys.exit(1)

# ── Display functions ──────────────────────────────────────────────────────────

def divider(char="─", width=58):
    print("  " + char * width)

def section(title: str):
    print()
    divider("═")
    print(f"  {title}")
    divider("═")

def show_summary(df: pd.DataFrame):
    section("CLASS SUMMARY")
    total     = len(df)
    class_avg = df["Average"].mean()
    highest   = df["Average"].max()
    lowest    = df["Average"].min()
    passcount = (df["Average"] >= 50).sum()

    print(f"  {'Total students':<25}: {total}")
    print(f"  {'Class average':<25}: {class_avg:.2f}")
    print(f"  {'Highest average':<25}: {highest:.2f}")
    print(f"  {'Lowest average':<25}: {lowest:.2f}")
    print(f"  {'Pass rate':<25}: {passcount}/{total} ({passcount/total*100:.1f}%)")

def show_topper(df: pd.DataFrame):
    section("TOP SCORER")
    row = df.loc[df["Average"].idxmax()]
    print(f"  Name    : {row['Name']}")
    print(f"  Average : {row['Average']} ({row['Grade']} — {row['Remark']})")
    for sub in SUBJECTS:
        print(f"  {sub:<10}: {row[sub]}")

def show_lowest(df: pd.DataFrame):
    section("LOWEST SCORER")
    row = df.loc[df["Average"].idxmin()]
    print(f"  Name    : {row['Name']}")
    print(f"  Average : {row['Average']} ({row['Grade']} — {row['Remark']})")
    for sub in SUBJECTS:
        print(f"  {sub:<10}: {row[sub]}")

def show_all_sorted(df: pd.DataFrame):
    section("ALL STUDENTS — SORTED BY AVERAGE (HIGH → LOW)")
    sorted_df = df.sort_values("Average", ascending=False).reset_index(drop=True)
    header = f"  {'Rank':<5} {'Name':<20} {'Avg':<8} {'Grade':<6} Remark"
    print(header)
    divider()
    for _, row in sorted_df.iterrows():
        print(f"  {row['Rank']:<5} {row['Name']:<20} {row['Average']:<8} {row['Grade']:<6} {row['Remark']}")

def show_subject_analysis(df: pd.DataFrame):
    section("SUBJECT-WISE ANALYSIS")
    header = f"  {'Subject':<12} {'Avg':>6}  {'Max':>5}  {'Min':>5}  {'Topper'}"
    print(header)
    divider()
    for sub in SUBJECTS:
        avg    = df[sub].mean()
        top_i  = df[sub].idxmax()
        topper = df.loc[top_i, "Name"]
        print(f"  {sub:<12} {avg:>6.2f}  {df[sub].max():>5}  {df[sub].min():>5}  {topper}")

def search_student(df: pd.DataFrame):
    section("SEARCH STUDENT")
    name = input("  Enter student name: ").strip()
    matches = df[df["Name"].str.lower() == name.lower()]
    if matches.empty:
        print(f"  [!] No student found with name '{name}'.")
        return
    row = matches.iloc[0]
    print(f"\n  Name    : {row['Name']}")
    print(f"  Rank    : {row['Rank']} out of {len(df)}")
    print(f"  Average : {row['Average']} ({row['Grade']} — {row['Remark']})")
    print()
    for sub in SUBJECTS:
        bar_len = int(row[sub] / 5)
        bar     = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {sub:<10}: {bar}  {row[sub]}")

def show_grade_distribution(df: pd.DataFrame):
    section("GRADE DISTRIBUTION")
    grade_order = ["A+", "A", "B", "C", "D", "F"]
    for grade in grade_order:
        count   = (df["Grade"] == grade).sum()
        bar     = "█" * count
        print(f"  {grade:<4}: {bar:<15} {count} student(s)")

def export_report(df: pd.DataFrame):
    section("EXPORT REPORT")
    filename = "marks_report.csv"
    out = df.sort_values("Average", ascending=False)
    out.to_csv(filename, index=False)
    print(f"  Report saved as '{filename}' in the current folder.")

# ── Main menu ──────────────────────────────────────────────────────────────────

MENU = """
  ┌──────────────────────────────────────────┐
  │         STUDENT MARKS ANALYZER           │
  ├──────────────────────────────────────────┤
  │  1  →  Class summary                     │
  │  2  →  Top scorer                        │
  │  3  →  Lowest scorer                     │
  │  4  →  All students (sorted)             │
  │  5  →  Subject-wise analysis             │
  │  6  →  Search a student                  │
  │  7  →  Grade distribution                │
  │  8  →  Export report to CSV              │
  │  0  →  Exit                              │
  └──────────────────────────────────────────┘
"""

def main():
    df = load_data()
    print(f"\n  Data loaded: {len(df)} students, {len(SUBJECTS)} subjects.")

    actions = {
        "1": lambda: show_summary(df),
        "2": lambda: show_topper(df),
        "3": lambda: show_lowest(df),
        "4": lambda: show_all_sorted(df),
        "5": lambda: show_subject_analysis(df),
        "6": lambda: search_student(df),
        "7": lambda: show_grade_distribution(df),
        "8": lambda: export_report(df),
    }

    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! Keep analyzing. 📊\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("\n  [!] Invalid option. Enter 0–8.")

        input("\n  Press Enter to return to menu...")

if __name__ == "__main__":
    main()