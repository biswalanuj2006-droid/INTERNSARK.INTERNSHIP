# Crypto Price Tracker

A simple Python CLI tool to monitor real-time Bitcoin and Ethereum prices using the CoinGecko API.

## What it does
* Gets current prices, 24h price changes, and market caps for BTC and ETH.
* Let's you view individual coins or compare both at the same time.
* Includes a live tracker mode that auto-refreshes the terminal on a custom timer (min 10s to avoid rate limits).




# File Organizer

A minimal Python script that automatically sorts messy directories by moving files into categorized subfolders based on file extensions.

## Supported Groups
* **Images:** jpg, png, gif, webp, etc.
* **Documents & Spreadsheets:** pdf, docx, txt, md, xlsx, csv
* **Media:** mp4, avi, mp3, wav
* **Archives:** zip, rar, tar
* **Code:** py, js, html, css, json
* *Everything else gets tossed into an "Others" folder.*



# Student Marks Analyzer

A python utility script that uses the Pandas library to load student grade data from a CSV file, calculate statistics, and display or export performance reports.

## What it does
* Calculates individual student averages, grade markers, and class rankings.
* Provides high-level class stats (pass rates, averages, top and bottom performers).
* Breaks down performance metrics by subject (subject averages, subject toppers).
* Includes a built-in lookup feature to search for individual student profiles.
* Exports computed grading and ranking tables directly back to a separate CSV file.

## Prerequisites
You will need Python 3.10+ and the Pandas data library installed on your system.

Install pandas:
pip install pandas

## How to use it
1. Make sure you have a `students.csv` file located in the exact same directory as the script. 
2. The CSV sheet should contain at least the following headers: `Name`, `Math`, `Science`, `English`, `History`, `Computer`.

