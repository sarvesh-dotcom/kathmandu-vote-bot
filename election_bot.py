import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select

BOT_TOKEN = "8716448487:AAHiQmGr1sPugDfdKTJ3jKZuF8m6ThY5BiU"
CHAT_ID = "-430883755"

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("telegram error:", e)

def fetch_results():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/chromium"

        driver = webdriver.Chrome(options=options)
        print("browser started")

        driver.get("https://result.election.gov.np/MapElectionResult2082.aspx")
        time.sleep(5)

        # select province
        Select(driver.find_element("css selector", "select[data-bind*='states']")).select_by_visible_text("बागमती प्रदेश")
        time.sleep(2)

        # district
        Select(driver.find_element("css selector", "select[data-bind*='filterDistricts']")).select_by_visible_text("काठमाडौं")
        time.sleep(2)

        # constituency
        Select(driver.find_element("css selector", "select[data-bind*='filterConstituencies']")).select_by_visible_text("२")
        time.sleep(8)

        rows = driver.find_elements("css selector", ".chart-result-row")
        results = []

        for row in rows:
            try:
                name = row.find_element("css selector", ".cand-basic span").text
                party = row.find_element("css selector", ".cand-party span").text
                votes = row.find_element("css selector", ".prog-count").text

                results.append({"name": name, "party": party, "votes": votes})
            except Exception as e:
                print("row parse error:", e)

        driver.quit()
        return results

    except Exception as e:
        print("selenium error:", e)
        return []


def format_message(results):
    msg = "📊 Kathmandu-2 Vote Update\n\n"
    for r in results:
        msg += f"{r['name']} ({r['party']}) — {r['votes']}\n"
    return msg


def main():
    print("🚀 bot started")
    last = None

    while True:
        try:
            results = fetch_results()

            if last is None:
                last = results
                print("initial snapshot")
            elif results != last:
                send_message(format_message(results))
                print("update sent")
                last = results
            else:
                print("no change")

        except Exception as e:
            print("loop error:", e)

        time.sleep(30)


if __name__ == "__main__":
    main()