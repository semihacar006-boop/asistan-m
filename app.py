import streamlit as st
import google.generativeai as genai
import toml
import pandas as pd
import os
from datetime import datetime, date

# ---------------------------------------------------------
# 1. DİNAMİK TARİH VE YAŞ HESAPLAMALARI
# ---------------------------------------------------------
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
        return f"4. Sınıf Öğrencisi (Tahmini Mezuniyet: Eylül 2025 - Kalan: ~{months} ay)"

BIRTH_DATE = date(2000, 7, 21)
GRADUATION_DATE = date(2025, 9, 4)
CURRENT_AGE = calculate_age(BIRTH_DATE)
EDU_STATUS = get_education_status(GRADUATION_DATE)
TODAY_STR = date.today().strftime("%d.%m.%Y")

# ---------------------------------------------------------
# 2. ADAY PROFİLİ
# ---------------------------------------------------------
CANDIDATE_PROFILE = f"""
AD SOYAD: Semih ACAR
DOĞUM: 21/07/2000, Ankara (Güncel Yaş: {CURRENT_AGE})
EĞİTİM: Konya Teknik Üniversitesi - Elektrik Elektronik Mühendisliği
Anadolu Üniversitesi - Uluslar Arası İlişkiler (07/09/2025 - Devam Ediyor.)
DURUM: {EDU_STATUS}

ÖZET VE LİDERLİK PROFİLİ:
Semih, {CURRENT_AGE} yaşında, teknik derinliğinin yanı sıra güçlü bir yönetici potansiyeline sahiptir.
- Teknik Liderlik: Hem donanım hem yazılım ekipleriyle köprü kurabilir.
- Kriz Yönetimi: Çözüm odaklıdır.
- Finansal Bakış: Ekonomi ve blockchain ilgisi ile maliyet analizi yapabilir.

PROJELER:
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

# ---------------------------------------------------------
# 3. SAYFA AYARLARI
# ---------------------------------------------------------
st.set_page_config(page_title="Semih ACAR - Dijital Mülakat Asistanı", page_icon="⚡", layout="wide")

# ---------------------------------------------------------
# 4. API BAĞLANTISI (GÜVENLİ MOD)
# ---------------------------------------------------------
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        # Localde çalışırken hata vermemesi için
        try:
            secrets = toml.load(".streamlit/secrets.toml")
            genai.configure(api_key=secrets["GOOGLE_API_KEY"])
        except:
            st.warning("API Anahtarı bulunamadı. Sohbet çalışmayabilir.")
except Exception as e:
    st.error(f"API Hatası: {e}")

# ---------------------------------------------------------
# 5. GÜÇLENDİRİLMİŞ LOGLAMA SİSTEMİ
# ---------------------------------------------------------
LOG_FILE = "ziyaretci_loglari.xlsx"

def save_visitor_info(name, company, position):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Tarih": [now], 
        "Ad Soyad": [name], 
        "Şirket": [company], 
        "Pozisyon": [position]
    })
    
    try:
        # Dosya varsa üzerine ekle, yoksa yeni oluştur
        if os.path.exists(LOG_FILE):
            df_old = pd.read_excel(LOG_FILE, engine="openpyxl")
            df_final = pd.concat([df_old, new_data], ignore_index=True)
            df_final.to_excel(LOG_FILE, index=False, engine="openpyxl")
        else:
            new_data.to_excel(LOG_FILE, index=False, engine="openpyxl")
    except Exception as e:
        st.error(f"Kayıt Hatası: {e}")

if "visitor_submitted" not in st.session_state:
    st.session_state.visitor_submitted = False

# --- GİRİŞ FORMU ---
if not st.session_state.visitor_submitted:
    st.markdown("<h1 style='text-align: center;'>Hoş Geldiniz</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Semih ACAR'ın Dijital Asistanı</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("visitor_form"):
            v_name = st.text_input("Adınız Soyadınız")
            v_company = st.text_input("Şirket Adı")
            v_position = st.text_input("Pozisyonunuz")
            
            if st.form_submit_button("Sohbete Başla", type="primary"):
                if v_name and v_company:
                    save_visitor_info(v_name, v_company, v_position)
                    st.session_state.visitor_submitted = True
                    st.rerun()
                else:
                    st.warning("Lütfen Ad ve Şirket bilgilerini giriniz.")
    st.stop()

# ---------------------------------------------------------
# 6. SIDEBAR VE LOG İNDİRME (ADMİN PANELİ)
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .stChatMessage { padding: 1.2rem; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    [data-testid="chatMessage-assistant"] { background-color: #ffffff; border-left: 5px solid #0d6efd; }
    [data-testid="chatMessage-user"] { background-color: #e9ecef; border-right: 5px solid #495057; flex-direction: row-reverse; text-align: right; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=130)
    
    st.markdown("<h2 style='text-align: center;'>Semih ACAR</h2>", unsafe_allow_html=True)
    st.info(f"Teknik uzmanlığın ötesinde, stratejik karar alma ve ekip yönetimi konularında yetkin, vizyoner bir mühendis.")
    st.markdown("---")
    st.markdown("📧 [E-Posta](mailto:semihacar006@gmail.com)")
    st.markdown("🔗 [LinkedIn](http://linkedin.com/in/semih-acar-0606-sa)")
    
    # --- GİZLİ LOG İNDİRME BÖLÜMÜ ---
    st.markdown("---")
    with st.expander("🔐 Yönetici Girişi"):
        admin_pass = st.text_input("Şifre", type="password")
        if admin_pass == "semih123": # Burayı istersen değiştirebilirsin
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "rb") as f:
                    st.download_button("📥 Ziyaretçi Listesini İndir", f, file_name="ziyaretciler.xlsx")
            else:
                st.write("Henüz kayıt yok.")

# ---------------------------------------------------------
# 7. SOHBET SİSTEMİ
# ---------------------------------------------------------
system_instruction = f"""
Sen Semih ACAR'ı temsil eden profesyonel bir AI asistanısın.
TARİH: {TODAY_STR}. ADAY PROFİLİ: {CANDIDATE_PROFILE}
DAVRANIŞ KURALLARI:

1. **YÖNETİCİ VURGUSU:** Semih'i anlatırken sadece "kod yazar" veya "devre tasarlar" deme. "Projeyi yönetir, strateji belirler, inisiyatif alır ve ekibi yönlendirir" gibi ifadelerle onun Liderlik vasfını öne çıkar.
2. **MAAŞ BEKLENTİSİ POLİTİKASI:**
   - Kullanıcı maaş sorarsa ASLA direkt "En az 35.000 TL istiyor" deme.
   - Şöyle cevap ver: "Semih Bey için öncelik, şirketin vizyonu ve pozisyonun sağladığı katma değerdir. Ancak piyasa standartları, teknik yetkinlikleri ve yönetici potansiyeli göz önüne alındığında, **35.000 TL bandının üzerinde**, şirketin büyüklüğü ve yan haklarına göre ölçeklenebilir rekabetçi bir paket beklentisi mevcuttur."
3. **PLAY STORE UYGULAMASI:** GitHub sormadıkça GitHub'dan bahsetme. Ancak Play Store'da yayınlanmış bir uygulaması olduğunu, bunun "Ürün Yönetimi" becerisini gösterdiğini mutlaka vurgula.
4. **TEKNİK:** React vs sorulursa "Python/PyQt tecrübesiyle arayüz mantığını bildiği için hızla adapte olur" taktiğini uygula.
"""

try:
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=system_instruction)
except:
    model = genai.GenerativeModel(model_name="gemini-pro", system_instruction=system_instruction)

st.markdown("<h2 style='text-align: center;'>Semih ACAR | Dijital Mülakat Asistanı</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Merhaba! Ben Semih ACAR. Benim hakkında ne bilmek istersiniz?"}]
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.messages:
    icon = "⚡" if message["role"] == "assistant" else "💼"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    with st.chat_message("user", avatar="💼"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="⚡"):
        try:
            message_placeholder = st.empty()
            full_response = ""
            for chunk in st.session_state.chat_session.send_message(prompt, stream=True):
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Hata: {e}")