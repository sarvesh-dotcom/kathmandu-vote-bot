import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Telegram config
BOT_TOKEN = "8716448487:AAHiQmGr1sPugDfdKTJ3jKZuF8m6ThY5BiU"
CHAT_ID = "-430883755"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def fetch_results():
    options = webdriver.ChromeOptions()

    # headless for cloud
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(options=options)

    driver.get("https://result.election.gov.np/MapElectionResult2082.aspx")
    time.sleep(5)

    # select province (प्रदेश) -> बागमती प्रदेश
    Select(driver.find_element("css selector", "select[data-bind*='states']")).select_by_visible_text("बागमती प्रदेश")
    time.sleep(2)

    # select district (जिल्ला) -> काठमाडौं
    Select(driver.find_element("css selector", "select[data-bind*='filterDistricts']")).select_by_visible_text("काठमाडौं")
    time.sleep(2)

    # select constituency -> २
    Select(driver.find_element("css selector", "select[data-bind*='filterConstituencies']")).select_by_visible_text("२")
    time.sleep(8)  # wait for results

    rows = driver.find_elements("css selector", ".chart-result-row")

    results = []

    for row in rows:
        try:
            name = row.find_element("css selector", ".cand-basic span").text
            party = row.find_element("css selector", ".cand-party span").text
            votes = row.find_element("css selector", ".prog-count").text

            results.append({
                "name": name,
                "party": party,
                "votes": votes
            })
        except:
            continue

    driver.quit()
    return results


def format_message(results):
    msg = "📊 Kathmandu-2 Vote Update\n\n"
    for r in results:
        msg += f"{r['name']} ({r['party']}) — {r['votes']}\n"
    return msg


def main():
    last_snapshot = None

    while True:
        try:
            results = fetch_results()

            if last_snapshot is None:
                last_snapshot = results
                print("initial snapshot stored")
                time.sleep(30)
                continue

            if results != last_snapshot:
                message = format_message(results)
                send_message(message)
                print("update sent")
                last_snapshot = results
            else:
                print("no change")

        except Exception as e:
            print("error:", e)

        time.sleep(30)


if __name__ == "__main__":
    main()