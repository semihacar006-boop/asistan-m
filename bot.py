import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- AYARLAR ---
USERNAME = "semihacar006@gmail.com"    
PASSWORD = "032615948sa"                  
SEARCH_KEYWORD = "Elektrik Elektronik Mühendisi"
API_URL = "http://127.0.0.1:5000/ask"  # api.py'nin adresi

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Tarayıcı kapanmasın diye:
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def random_sleep(min_s=2, max_s=4):
    time.sleep(random.uniform(min_s, max_s))

#import requests

# API.PY dosyanın çalıştığı adres
API_URL = "http://127.0.0.1:5000/ask"

def ask_my_assistant(soru_metni):
    """
    LinkedIn'deki soruyu senin yerel yapay zeka asistanına sorar.
    """
    try:
        payload = {"question": soru_metni}
        # API'ye istek atıyoruz
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            cevap = response.json().get('answer')
            print(f"🤖 Asistan Cevabı: {cevap}")
            return cevap
        else:
            print("❌ Asistan cevap veremedi.")
            return None
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")
        print("Lütfen 'python api.py' komutuyla asistanı çalıştırdığından emin ol.")
        return None

    for job in job_cards:
        try:
            job.click()
            random_sleep(1, 2)
            
            # Kolay Başvuru Butonunu Ara
            apply_btn = driver.find_elements(By.CLASS_NAME, "jobs-apply-button--top-card")
            if apply_btn:
                print("🔵 Kolay Başvuru bulundu, tıklanıyor...")
                apply_btn[0].click()
                random_sleep()
                
                # --- FORMU DOLDURMA (AI DESTEKLİ) ---
                # Formdaki inputları bul (Label'lara göre)
                # Not: LinkedIn form yapısı karışıktır, bu basit bir örnektir.
                labels = driver.find_elements(By.TAG_NAME, "label")
                for label in labels:
                    soru = label.text
                    if soru:
                        cevap = ask_my_assistant(soru) # <--- BURADA API'YE GİDİYOR
                        
                        if cevap:
                            try:
                                # Label'ın altındaki input'u bulmaya çalış
                                input_id = label.get_attribute("for")
                                if input_id:
                                    inp = driver.find_element(By.ID, input_id)
                                    inp.clear()
                                    inp.send_keys(cevap)
                                    random_sleep(0.5, 1)
                            except:
                                pass
                
                print("✅ Form yapay zeka ile dolduruldu (Test modu - Gönderilmedi).")
                # Pencereyi kapat
                driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
                random_sleep()
                driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']").click()
            
        except Exception as e:
            print(f"Hata: {e}")
            continue

if __name__ == "__main__":
    driver = setup_driver()
    login_linkedin(driver)
    search_and_apply(driver)