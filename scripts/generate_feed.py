import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import os

TOP_N = 100  # Limit to top 100 stocks
OUTPUT_FILE = "feed.xml"

def fetch_latest_bse_isin_csv():
    base_url = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx"
    try:
        r = requests.get(base_url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Look for EQ_ISINCODE CSV link
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "EQ_ISINCODE" in href and href.endswith(".csv"):
                if not href.startswith("http"):
                    href = "https://www.bseindia.com" + href
                return href
        raise Exception("No EQ_ISINCODE CSV found")
    except Exception as e:
        print(f"Failed to fetch BSE ISIN CSV link: {e}")
        return None

def fetch_nse_equity_list():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    try:
        df = pd.read_csv(url)
        print(f"Loaded NSE master rows: {len(df)}")
        return df
    except Exception as e:
        print(f"Failed to load NSE equity list: {e}")
        return pd.DataFrame()

def fetch_live_data(symbol, exchange):
    """
    Placeholder for live price API call.
    You can integrate NSE/BSE live API here.
    """
    return {
        "live_price": 100.00,
        "low": 98.50,
        "high": 101.25,
        "52w_low": 75.00,
        "52w_high": 120.00,
        "open_price": 99.50,
        "prev_close": 99.00,
        "volume": 150000,
        "lower_circuit": 80.00,
        "upper_circuit": 120.00
    }

def generate_rss_feed(items):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "NSE & BSE Stock Feed"
    ET.SubElement(channel, "link").text = "https://yourdomain.com"
    ET.SubElement(channel, "description").text = "Live NSE & BSE stock updates"
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    for item in items:
        it = ET.SubElement(channel, "item")
        ET.SubElement(it, "title").text = f"{item['BSE']} | {item['NSE']} | {item['name']}"
        desc_text = f"{item['BSE']} | {item['NSE']} | {item['name']} | {item['live_price']} | {item['low']} | {item['high']} | {item['52w_low']} | {item['52w_high']} | {item['open_price']} | {item['prev_close']} | {item['volume']} | {item['lower_circuit']} | {item['upper_circuit']}"
        ET.SubElement(it, "description").text = desc_text
        ET.SubElement(it, "link").text = "https://yourdomain.com/stocks/" + item['NSE']

    tree = ET.ElementTree(rss)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(items)} entries to {OUTPUT_FILE}")

def main():
    print(f"Starting feed generation: {datetime.utcnow().isoformat()}")
    
    # Fetch NSE master list
    nse_df = fetch_nse_equity_list()
    if nse_df.empty:
        print("No NSE data. Exiting.")
        return

    # Fetch BSE ISIN CSV
    bse_url = fetch_latest_bse_isin_csv()
    if bse_url:
        try:
            bse_df = pd.read_csv(bse_url)
            print(f"Loaded BSE ISIN rows: {len(bse_df)}")
        except Exception as e:
            print(f"Failed to load BSE data: {e}")
            bse_df = pd.DataFrame()
    else:
        bse_df = pd.DataFrame()

    # Merge or map NSE/BSE if ISIN matching is needed
    top_symbols = nse_df.head(TOP_N)

    feed_items = []
    for _, row in top_symbols.iterrows():
        symbol = row['SYMBOL']
        name = row['NAME OF COMPANY']
        live_data = fetch_live_data(symbol, "NSE")

        feed_items.append({
            "BSE": "BSE_CODE" if not bse_df.empty else "",
            "NSE": symbol,
            "name": name,
            **live_data
        })

    generate_rss_feed(feed_items)
    print(f"Done at {datetime.utcnow().isoformat()}")

if __name__ == "__main__":
    main()
