import csv
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# CONFIG
TOP_N = 100
NSE_MASTER_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
BSE_MASTER_URL = "https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE.csv"

# Initialize NSE session with cookies for travel
def make_nse_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nseindia.com"
    })
    s.get("https://www.nseindia.com", timeout=10)
    time.sleep(0.5)
    return s

def fetch_csv_rows(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return list(csv.DictReader(resp.text.splitlines()))
    except Exception as e:
        print(f"⚠ Could not fetch CSV {url}: {e}")
        return []

def fetch_nse_price(symbol, session, max_retries=3):
    api = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    for attempt in range(1, max_retries+1):
        try:
            resp = session.get(api, timeout=10)
            if resp.status_code == 401 or resp.status_code == 403:
                print(f"Unauthorized {symbol}, attempt {attempt}")
                session = make_nse_session()
                time.sleep(1)
                continue
            resp.raise_for_status()
            if "application/json" in resp.headers.get("Content-Type",""):
                return resp.json().get("priceInfo", {})
            print(f"Non-JSON NSE response for {symbol}, attempt {attempt}")
        except Exception as e:
            print(f"Error fetching {symbol} from NSE: {e}")
        time.sleep(1 + attempt)  # backoff
    return {}  # fail-safe empty

def process(symbol, name, isin, bse_map, nse_session):
    price = fetch_nse_price(symbol, nse_session)
    return {
        "symbol": symbol,
        "name": name,
        "nse": price
    }

def build_rss(results):
    rss = ET.Element("rss", version="2.0")
    ch = ET.SubElement(rss, "channel")
    ET.SubElement(ch, "title").text = "Live NSE/BSE Feed"
    ET.SubElement(ch, "link").text = "https://your-site.com"
    ET.SubElement(ch, "description").text = "Real-time NSE/BSE stock updates"
    ET.SubElement(ch, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    for res in results:
        sym = res["symbol"]
        name = res["name"]
        n = res["nse"]
        nline = f"NSE: {name} | {n.get('lastPrice','-')} | {n.get('intraDayLow','-')} | {n.get('intraDayHigh','-')} | {n.get('low52','-')} | {n.get('high52','-')} | {n.get('open','-')} | {n.get('previousClose','-')} | {n.get('totalTradedVolume','-')} | {n.get('lowerCircuit','-')} | {n.get('upperCircuit','-')}"

        desc = f"""
        <p style="font-family: Arial; background:#1e71c9; color:#fff; padding:5px;"><strong>{sym}</strong></p>
        <p style="font-family: Arial; background:#fff; padding:5px;"><span style="color:#1e71c9;">{nline}</span></p>
        """
        item = ET.SubElement(ch, "item")
        ET.SubElement(item, "title").text = f"{sym} – {name}"
        ET.SubElement(item, "link").text = f"https://www.nseindia.com/get-quotes/equity?symbol={sym}"
        ET.SubElement(item, "pubDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        ET.SubElement(item, "description").text = desc.strip()
    ET.ElementTree(rss).write("feed.xml", encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(results)} entries to feed.xml")

def main():
    print("Starting:", datetime.now(timezone.utc).isoformat())
    nse_list = fetch_csv_rows(NSE_MASTER_URL)
    if not nse_list:
        print("No NSE list, abort.")
        return

    nse_session = make_nse_session()

    tasks = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        for row in nse_list[:TOP_N]:
            tasks.append(ex.submit(process, row["SYMBOL"], row["NAME OF COMPANY"], row.get("ISIN NUMBER",""), {}, nse_session))

        results = []
        for fut in as_completed(tasks):
            try:
                results.append(fut.result())
            except Exception as e:
                print("Error in task:", e)

    build_rss(results)
    print("Done:", datetime.now(timezone.utc).isoformat())

if __name__ == "__main__":
    main()
