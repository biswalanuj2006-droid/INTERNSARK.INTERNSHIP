"""
Crypto Price Tracker
====================
Uses: Python, requests, JSON
API:  CoinGecko (free, no key needed)
Run:  python crypto_tracker.py
"""

import requests
import time
import os

API_URL = "https://api.coingecko.com/api/v3/simple/price"

COINS = {
    "1": ("bitcoin",  "Bitcoin",  "BTC", "₿"),
    "2": ("ethereum", "Ethereum", "ETH", "Ξ"),
}

# ── API call ───────────────────────────────────────────────────────────────────

def get_price(coin_id: str) -> dict | None:
    """Fetch price, 24h change, and market cap for a coin."""
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_change": "true",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if coin_id not in data:
            print(f"  [!] No data found for '{coin_id}'.")
            return None
        return data[coin_id]
    except requests.exceptions.ConnectionError:
        print("  [!] Network error — check your internet connection.")
    except requests.exceptions.Timeout:
        print("  [!] Request timed out. Try again.")
    except requests.exceptions.HTTPError as e:
        print(f"  [!] HTTP error: {e}")
    except Exception as e:
        print(f"  [!] Unexpected error: {e}")
    return None

# ── Display helpers ────────────────────────────────────────────────────────────

def fmt_price(usd: float) -> str:
    return f"${usd:,.2f}"

def fmt_marketcap(usd: float) -> str:
    if usd >= 1_000_000_000_000:
        return f"${usd / 1_000_000_000_000:.2f}T"
    if usd >= 1_000_000_000:
        return f"${usd / 1_000_000_000:.2f}B"
    return f"${usd:,.0f}"

def fmt_change(pct: float) -> str:
    arrow = "📈" if pct >= 0 else "📉"
    sign  = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}% {arrow}"

def display_coin(coin_id: str, name: str, symbol: str, icon: str):
    """Print a formatted card for one coin."""
    data = get_price(coin_id)
    if data is None:
        return

    price  = data.get("usd", 0)
    change = data.get("usd_24h_change", 0)
    mcap   = data.get("usd_market_cap", 0)

    print()
    print("  ╔══════════════════════════════════════╗")
    print(f"  {icon}  {name} ({symbol})")
    print("  ├──────────────────────────────────────┤")
    print(f"  {'Price':<14}: {fmt_price(price)}")
    print(f"  {'24h Change':<14}: {fmt_change(change)}")
    print(f"  {'Market Cap':<14}: {fmt_marketcap(mcap)}")
    print("  ╚══════════════════════════════════════╝")

# ── Menu actions ───────────────────────────────────────────────────────────────

def show_single(choice: str):
    coin_id, name, symbol, icon = COINS[choice]
    display_coin(coin_id, name, symbol, icon)

def compare_coins():
    print("\n  Fetching both coins...\n")
    for _, (coin_id, name, symbol, icon) in COINS.items():
        display_coin(coin_id, name, symbol, icon)

def auto_refresh():
    try:
        secs = int(input("\n  Refresh every how many seconds? (min 10): "))
        secs = max(secs, 10)      # respect free API rate limits
    except ValueError:
        print("  [!] Invalid input. Using 30 seconds.")
        secs = 30

    print(f"\n  Live tracker started — refreshing every {secs}s. Press Ctrl+C to stop.\n")
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n    Auto-refreshing every {secs}s  |  Ctrl+C to stop\n")
            compare_coins()
            print(f"\n  Next refresh in {secs}s...")
            time.sleep(secs)
    except KeyboardInterrupt:
        print("\n\n  Live tracker stopped. Returning to menu...\n")

# ── Main menu ──────────────────────────────────────────────────────────────────

MENU = """
  ┌─────────────────────────────────┐
  │       CRYPTO PRICE TRACKER      │
  ├─────────────────────────────────┤
  │  1  →  Bitcoin  (BTC)           │
  │  2  →  Ethereum (ETH)           │
  │  3  →  Compare both             │
  │  4  →  Auto-refresh (live)      │
  │  0  →  Exit                     │
  └─────────────────────────────────┘
"""

def main():
    print("\n  Welcome to Crypto Price Tracker ")
    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip()

        if choice in ("1", "2"):
            show_single(choice)
        elif choice == "3":
            compare_coins()
        elif choice == "4":
            auto_refresh()
        elif choice == "0":
            print("\n  Goodbye! HODL strong. \n")
            break
        else:
            print("\n  [!] Invalid option. Enter 0–4.")

        input("\n  Press Enter to return to menu...")

if __name__ == "__main__":
    main()