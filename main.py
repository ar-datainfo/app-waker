import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Load from environment (GitHub Secrets)
urls_env = os.environ.get("STREAMLIT_APP_URLS", "")
STREAMLIT_URLS = [u.strip() for u in urls_env.split(",") if u.strip()]

HUGGINGFACE_SPACES = [
    "https://huggingface.co/spaces/anirudh-rs/ai-stem-separator",
    "https://huggingface.co/spaces/anirudh-rs/collapse-signature",
]

HF_TOKEN = os.environ.get("HF_TOKEN")


def wake_streamlit(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        try:
            button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")
            ))
            button.click()
            print(f"✅ Streamlit: {url} — was sleeping, woke it up")
        except TimeoutException:
            print(f"✅ Streamlit: {url} — already awake")
    except Exception as e:
        print(f"❌ Streamlit: {url} — error: {e}")


def wake_huggingface(space_id):
    try:
        url = f"https://huggingface.co/api/spaces/{space_id}/restart?factory=true"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"✅ HuggingFace: {space_id} — wake request sent")
        else:
            print(f"⚠️ HuggingFace: {space_id} — status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ HuggingFace: {space_id} — error: {e}")


def main():
    # Wake Streamlit apps
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        for url in STREAMLIT_URLS:
            wake_streamlit(driver, url)
    finally:
        driver.quit()

    # Wake HuggingFace Spaces
    for space_id in HUGGINGFACE_SPACES:
        wake_huggingface(space_id)


if __name__ == "__main__":
    main()
