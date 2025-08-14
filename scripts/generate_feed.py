#!/usr/bin/env python3
import csv
import os
import time
import json
import math
import datetime as dt
from pathlib import Path
from typing import Dict, Any, Optional

import requests
import yfinance as yf

# --------------- CONFIG ---------------

# Pick your base (no suffix) symbol that trades on BOTH NSE/BSE
# Example: RELIANCE, TCS, INFY, HDFCBANK, ITC, etc.
SYMBOL = os.getenv("STOCK_SYMBOL", "RELIANCE")

# Files
CSV_PATH = Path("store-stock-details.csv")
XML_PATH = Path("feed.xml")

# Poll interval (seconds)
INTERVAL_SEC = int(os.getenv("POLL_INTERVAL_SEC", "180"))  # 3 minutes

# Git push? Set GIT_PUSH=true and provide a tokened remote or pre-auth origin.
GIT_PUSH = os.getenv("GIT_PUSH", "false").lower() == "true"
GIT_COMMIT_MESSAGE = os.getenv("GIT_COMMIT_MESSAGE", "chore: update stock feed")

# --------------- HELPERS ---------------

def fmt_num(x: Optional[float]) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return ""
    # keep 2 decimals for money-ish fields
    return f"{x:.2f}"

def now_ist_iso() -> str:
    # Asia/Kolkata without external tz lib: offset +05:30
    return (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).replace(microsecond=0).isoformat() + "+05:30"

def ensure_csv_header(path: Path):
    header = [
        "timestamp", "exchange", "symbol",
        "open", "prev_close", "todays_low", "todays_high",
        "week52_low", "week52_high", "volume",
        "lower_circuit", "upper_circuit"
    ]
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def append_csv_row(path: Path, row: Dict[str, Any]):
    ensure_csv_header(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            row.get("timestamp",""), row.get("exchange",""), row.get("symbol",""),
            row.get("open",""), row.get("prev_close",""), row.get("todays_low",""), row.get("todays_high",""),
            row.get("week52_low",""), row.get("week52_high",""), row.get("volume",""),
            row.get("lower_circuit",""), row.get("upper_circuit","")
        ])

def write_xml(path: Path, records: Dict[str, Dict[str, Any]]):
    # records: {"NSE": {...}, "BSE": {...}}
    ts = now_ist_iso()
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<stockFeed generatedAt="{ts}">')

    for ex in ["NSE", "BSE"]:
        r = records.get(ex, {})
        sym = r.get("symbol", "")
        lines.append(f'  <stock exchange="{ex}" symbol="{sym}">')
        lines.append(f'    <open>{r.get("open","")}</open>')
        lines.append(f'    <prevClose>{r.get("prev_close","")}</prevClose>')
        lines.append(f'    <todaysLow>{r.get("todays_low","")}</todaysLow>')
        lines.append(f'    <todaysHigh>{r.get("todays_high","")}</todaysHigh>')
        lines.append(f'    <week52Low>{r.get("week52_low","")}</week52Low>')
        lines.append(f'    <week52High>{r.get("week52_high","")}</week52High>')
        lines.append(f'    <volume>{r.get("volume","")}</volume>')
        lines.append(f'    <lowerCircuit>{r.get("lower_circuit","")}</lowerCircuit>')
        lines.append(f'    <upperCircuit>{r.get("upper_circuit","")}</upperCircuit>')
        lines.append(f'  </stock>')

    lines.append('</stockFeed>')
    path.write_text("\n".join(lines), encoding="utf-8")

def fetch_yf_snapshot(ticker: str) -> Dict[str, Any]:
    """
    Pulls a quote snapshot via yfinance fast_info + info fallback.
    Works for both NSE (.NS) and BSE (.BO) symbols.
    """
    tk = yf.Ticker(ticker)
    fi = {}
    try:
        fi = tk.fast_info or {}
    except Exception:
        fi = {}

    # Fallbacks from .info are slower but safer
    info = {}
    try:
        info = tk.info or {}
    except Exception:
        info = {}

    def g(key, *alts):
        for k in (key, *alts):
            v = fi.get(k, None)
            if v is not None:
                return v
        for k in (key, *alts):
            v = info.get(k, None)
            if v is not None:
                return v
        return None

    return {
        "open": fmt_num(g("open", "regularMarketOpen")),
        "prev_close": fmt_num(g("previousClose", "regularMarketPreviousClose")),
        "todays_low": fmt_num(g("dayLow", "regularMarketDayLow")),
        "todays_high": fmt_num(g("dayHigh", "regularMarketDayHigh")),
        "week52_low": fmt_num(g("yearLow", "fiftyTwoWeekLow")),
        "week52_high": fmt_num(g("yearHigh", "fiftyTwoWeekHigh")),
        "volume": str(g("volume", "regularMarketVolume") or "")
    }

def fetch_nse_circuits(symbol_no_suffix: str) -> Dict[str, Optional[str]]:
    """
    Hits NSE's public quote API for price bands (circuit limits).
    Note: NSE site is picky about headers; emulate a browser.
    If it fails, return empty values.
    """
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol_no_suffix.upper()}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol_no_suffix.upper()}",
        "Connection": "keep-alive"
    }
    s = requests.Session()
    try:
        # Warm-up to get cookies
        s.get("https://www.nseindia.com/", headers=headers, timeout=10)
        r = s.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        band = data.get("priceBand", {}) or data.get("priceband", {}) or {}
        lower = band.get("lower", None)
        upper = band.get("upper", None)
        return {
            "lower_circuit": fmt_num(float(lower)) if lower is not None else "",
            "upper_circuit": fmt_num(float(upper)) if upper is not None else ""
        }
    except Exception:
        return {"lower_circuit": "", "upper_circuit": ""}

def make_record(exchange: str, symbol_no_suffix: str) -> Dict[str, Any]:
    if exchange == "NSE":
        yf_ticker = f"{symbol_no_suffix}.NS"
    elif exchange == "BSE":
        yf_ticker = f"{symbol_no_suffix}.BO"
    else:
        raise ValueError("exchange must be NSE or BSE")

    snap = fetch_yf_snapshot(yf_ticker)

    # Circuits: NSE via API; BSE left blank (BSE API is inconsistent)
    if exchange == "NSE":
        circuits = fetch_nse_circuits(symbol_no_suffix)
    else:
        circuits = {"lower_circuit": "", "upper_circuit": ""}

    rec = {
        "timestamp": now_ist_iso(),
        "exchange": exchange,
        "symbol": symbol_no_suffix.upper(),
        **snap,
        **circuits
    }
    return rec

def push_to_git():
    # Assumes you’re inside a git repo with write access.
    # If using a PAT in the remote URL, ensure it’s already set.
    try:
        import subprocess
        subprocess.run(["git", "add", str(CSV_PATH), str(XML_PATH)], check=True)
        # avoid empty commit if nothing changed
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if diff.returncode != 0:
            subprocess.run(["git", "commit", "-m", GIT_COMMIT_MESSAGE], check=True)
            subprocess.run(["git", "push"], check=True)
    except Exception as e:
        print(f"[git] push skipped/failed: {e}")

def run_once(symbol: str):
    nse = make_record("NSE", symbol)
    bse = make_record("BSE", symbol)

    # Append CSV rows
    append_csv_row(CSV_PATH, nse)
    append_csv_row(CSV_PATH, bse)

    # Regenerate XML with the latest snapshot for both
    write_xml(XML_PATH, {"NSE": nse, "BSE": bse})

    if GIT_PUSH:
        push_to_git()

    print(f"[{now_ist_iso()}] Updated CSV + XML for {symbol.upper()}")

def main():
    print(f"Polling {SYMBOL.upper()} on NSE/BSE every {INTERVAL_SEC}s. Ctrl+C to stop.")
    while True:
        try:
            run_once(SYMBOL)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            # Log and continue – don’t crash the loop
            print(f"[error] {e}")
        time.sleep(INTERVAL_SEC)

if __name__ == "__main__":
    main()
