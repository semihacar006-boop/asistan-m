# Dosya adı: api.py
from flask import Flask, request, jsonify
import google.generativeai as genai
import toml
import os
from datetime import date

app = Flask(__name__)

# --- 1. AYNI MANTIK VE VERİLER (App.py'den alındı) ---
def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_education_status(grad_date):
    today = date.today()
    if today >= grad_date:
        return "Mezun (Lisans Derecesi Tamamlandı)"
    else:
        remaining_days = (grad_date - today).days
        months = remaining_days // 30
        return f"4. Sınıf Öğrencisi (Tahmini Mezuniyet: Eylül 2025 - Kalan Süre: ~{months} ay)"

# Sabit Veriler
BIRTH_DATE = date(2000, 7, 21)
GRADUATION_DATE = date(2025, 9, 4)

# Dinamik Veriler
CURRENT_AGE = calculate_age(BIRTH_DATE)
EDU_STATUS = get_education_status(GRADUATION_DATE)
TODAY_STR = date.today().strftime("%d.%m.%Y")

# PROMPT (Senin yazdığın metnin aynısı)
CANDIDATE_PROFILE = f"""
AD SOYAD: Semih ACAR
DOĞUM: 21/07/2000, Ankara (Güncel Yaş: {CURRENT_AGE})
EĞİTİM: Konya Teknik Üniversitesi - Elektrik Elektronik Mühendisliği (19/08/2019 - 04/09/2025)
Anadolu Üniversitesi - Uluslar Arası İlişkiler (07/09/2025 - Devam Ediyor.)
EĞİTİM DURUMU: {EDU_STATUS}

ÖZET VE LİDERLİK PROFİLİ:
Semih, {CURRENT_AGE} yaşında, teknik derinliğinin yanı sıra güçlü bir yönetici ve lider potansiyeline sahiptir.
Sadece verilen işi yapan değil, süreci yöneten, strateji kuran ve ekibi yönlendirebilecek vizyona sahip bir mühendistir.
- Teknik Liderlik: Hem donanım hem yazılım ekipleriyle köprü kurabilir.
- Kriz Yönetimi: Proje süreçlerinde çıkan sorunlarda çözüm odaklı ve soğukkanlıdır.
- Finansal Bakış: Ekonomi ve blockchain ilgisi sayesinde projelerin maliyet/fayda analizini yapabilir.

PROJELER & DENEYİMLER:
1. PLAY STORE UYGULAMASI (Mobil Yazılım):
   - Kendi geliştirdiği mobil uygulamayı uçtan uca tasarlayıp Play Store'da yayınlamıştır. 
   - Bu proje, Semih'in bir ürünü "fikir aşamasından pazara sunma" (Product Management) yeteneğini kanıtlar.

2. Kapalı Çevrim Motor Kontrolü (Gömülü Sistemler):
   - STM32 ve Python (PyQt) entegrasyonu.
   
3. Çizgi İzleyen Robot (Otonom Sistemler):
   - Raspberry Pi ve Linux tabanlı otonom sürüş algoritmaları.

STAJLAR:
- ELİMKO & Pİ MAKİNA: Üretim ve AR-GE süreçlerinde aktif rol aldı.

TEKNİK YETENEKLER:
- Diller: Python (İleri), C, C++, MATLAB.
- Platformlar: STM32, Arduino, Proteus, Linux.
- Yetkinlikler: Proje Yönetimi, Mobil Uygulama Geliştirme, IoT.
"""

SYSTEM_INSTRUCTION = f"""
Sen Semih ACAR'ı temsil eden üst düzey bir AI asistanısın. 
BUGÜNÜN TARİHİ: {TODAY_STR}

ADAY PROFİLİ:
{CANDIDATE_PROFILE}

GÖREVİN:
Sen bir iş başvuru botu için "Brain (Beyin)" görevi görüyorsun. LinkedIn veya kariyer sitelerinde sorulan sorulara kısa, net ve Semih'in profilini en iyi yansıtacak şekilde cevap ver.

KURALLAR:
1. Eğer soru "Experience" (Yıl) soruyorsa sadece sayı ver (Örn: "2").
2. Eğer soru "Yes/No" sorusuysa sadece "Yes" veya "No" de.
3. Eğer açık uçlu bir soruysa (Örn: "Neden biz?"), Semih'in yönetici ve teknik yönünü birleştiren 2 cümlelik vurucu bir cevap yaz.
4. Maaş sorulursa: "35000+ (Negotiable based on benefits)" yaz.
"""

# --- 2. GOOGLE GEMINI AYARLARI ---
try:
    # Streamlit secrets dosyasını manuel okuyoruz
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Model Tanımlama
    try:
        model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=SYSTEM_INSTRUCTION)
    except:
        model = genai.GenerativeModel(model_name="gemini-pro", system_instruction=SYSTEM_INSTRUCTION)
        
except Exception as e:
    print(f"HATA: API Key okunamadı. .streamlit/secrets.toml dosyasının olduğundan emin ol. Hata: {e}")

# --- 3. API ENDPOINT (BOTUN BURAYA BAĞLANACAK) ---
@app.route('/ask', methods=['POST'])
def ask_gemini():
    data = request.json
    soru = data.get('question', '')
    
    if not soru:
        return jsonify({'error': 'Soru boş olamaz'}), 400
    
    try:
        # Gemini'ye soruyu gönder
        response = model.generate_content(soru)
        cevap = response.text.strip()
        
        # Botun loglarında görünmesi için terminale de yazdıralım
        print(f"SORU: {soru} \nCEVAP: {cevap}\n---")
        
        return jsonify({'answer': cevap})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Bu scripti çalıştırdığında localhost:5000 adresinde yayın yapacak
    app.run(port=5000, debug=True)