import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

fake = Faker()
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd801vDKeACaus9G35mgJ7zYKHNRKJUf-3PO4j904WnCH5QrA/viewform"
NUM_SUBMISSIONS = 120  # test with 5 first

GENDERS = ["Male", "Female"]
YES_NO = ["Yes", "No"]
SEMESTERS = [str(i) for i in range(1, 9)]
CGPA_RANGES = ["Below 2.5", "2.5–2.99", "3.00–3.49", "3.5–4.00"]
LIKERT_SCALE = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
FREQUENCY = ["Always", "Often", "Sometimes", "Rarely", "Never"]
PERFORMANCE = ["Excellent", "Good", "Average", "Poor"]

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def fill_form():
    driver.get(FORM_URL)
    time.sleep(random.uniform(1.5, 3))

    questions = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')

    for i, q in enumerate(questions):
        try:
            # --- Radio / Likert / Multiple Choice ---
            choices = q.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
            if choices:
                choice = random.choice(choices)
                wait.until(EC.element_to_be_clickable(choice))
                driver.execute_script("arguments[0].click();", choice)
                time.sleep(0.3)
                continue

            # --- Short answer / text ---
            text_inputs = q.find_elements(By.TAG_NAME, "input")
            if text_inputs:
                text_inputs[0].send_keys(fake.first_name())
                continue

            # --- Dropdowns ---
            selects = q.find_elements(By.TAG_NAME, "select")
            if selects:
                options_list = selects[0].find_elements(By.TAG_NAME, "option")
                option_to_select = random.choice(options_list[1:])  # skip placeholder
                option_to_select.click()
                time.sleep(0.3)
                continue

        except Exception as e:
            print(f"Question {i+1} skipped: {e}")

    # --- Submit button ---
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Submit"]/ancestor::div[@role="button"]')))
    driver.execute_script("arguments[0].click();", submit_btn)
    time.sleep(random.uniform(1, 2))

# --- Main loop ---
for n in range(NUM_SUBMISSIONS):
    try:
        fill_form()
        print(f"[{n+1}/{NUM_SUBMISSIONS}] Submitted successfully!")
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"[{n+1}/{NUM_SUBMISSIONS}] Submission failed: {e}")
        time.sleep(2)

driver.quit()
