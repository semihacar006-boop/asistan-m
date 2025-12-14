import streamlit as st
import google.generativeai as genai
import toml
import pandas as pd
import os
from datetime import datetime, date

# ---------------------------------------------------------
# 1. DİNAMİK TARİH VE YAŞ HESAPLAMALARI (ZAMAN ALGISI)
# ---------------------------------------------------------
def calculate_age(birth_date):
    """Doğum tarihine göre güncel yaşı hesaplar."""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_education_status(grad_date):
    """Mezuniyet tarihine göre öğrenci/mezun durumunu belirler."""
    today = date.today()
    if today >= grad_date:
        return "Mezun (Lisans Derecesi Tamamlandı)"
    else:
        # Kalan süreyi hesapla
        remaining_days = (grad_date - today).days
        months = remaining_days // 30
        return f"4. Sınıf Öğrencisi (Tahmini Mezuniyet: Eylül 2025 - Kalan Süre: ~{months} ay)"

# Semih'in Sabit Verileri
BIRTH_DATE = date(2000, 7, 21)
GRADUATION_DATE = date(2025, 9, 4)

# Dinamik Veriler
CURRENT_AGE = calculate_age(BIRTH_DATE)
EDU_STATUS = get_education_status(GRADUATION_DATE)
TODAY_STR = date.today().strftime("%d.%m.%Y") # Yapay zekaya bugünü bildirmek için

# ---------------------------------------------------------
# 2. ADAY PROFİLİ VE ANALİZİ (YAPAY ZEKA BEYNİ)
# ---------------------------------------------------------
# f-string kullanarak dinamik verileri metne gömüyoruz
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

# ---------------------------------------------------------
# 3. SAYFA AYARLARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Semih ACAR - Dijital Mülakat Asistanı",
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 4. ZİYARETÇİ LOGLAMA SİSTEMİ
# ---------------------------------------------------------
LOG_FILE = "ziyaretci_loglari.xlsx"

def save_visitor_info(name, company, position):
    """Ziyaretçi bilgilerini Excel dosyasına kaydeder."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        "Tarih": [now],
        "Ad Soyad": [name],
        "Şirket": [company],
        "Pozisyon": [position]
    }
    df_new = pd.DataFrame(new_data)

    if os.path.exists(LOG_FILE):
        try:
            df_old = pd.read_excel(LOG_FILE)
            df_final = pd.concat([df_old, df_new], ignore_index=True)
            df_final.to_excel(LOG_FILE, index=False)
        except Exception as e:
            st.error(f"Log dosyası güncellenirken hata oluştu: {e}")
    else:
        df_new.to_excel(LOG_FILE, index=False)

if "visitor_submitted" not in st.session_state:
    st.session_state.visitor_submitted = False

# --- GİRİŞ FORMU ---
if not st.session_state.visitor_submitted:
    st.markdown("<h1 style='text-align: center;'>Hoş Geldiniz</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Semih ACAR'ın Dijital Asistanı ile görüşmeye başlamadan önce lütfen kendinizi tanıtın.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("visitor_form"):
            v_name = st.text_input("Adınız Soyadınız")
            v_company = st.text_input("Şirket Adı")
            v_position = st.text_input("Pozisyonunuz / Ünvanınız")
            
            submit_btn = st.form_submit_button("Sohbete Başla", type="primary")
            
            if submit_btn:
                if v_name and v_company:
                    save_visitor_info(v_name, v_company, v_position)
                    st.session_state.visitor_submitted = True
                    st.rerun()
                else:
                    st.warning("Lütfen Ad ve Şirket alanlarını doldurunuz.")
    st.stop()


# ---------------------------------------------------------
# 5. YAN PANEL VE LOGO
# ---------------------------------------------------------
# --- ESKİ KODU SİL, YERİNE BUNU YAPIŞTIR ---
try:
    # Streamlit Cloud'da şifreler st.secrets içinden okunur, dosya aranmaz.
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("HATA: Streamlit Cloud ayarlarında GOOGLE_API_KEY bulunamadı!")
        st.stop()
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")
    st.stop()

# CSS Tasarımı 
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .stChatMessage { padding: 1.2rem; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    [data-testid="chatMessage-assistant"] { background-color: #ffffff; border-left: 5px solid #0d6efd; }
    [data-testid="chatMessage-user"] { background-color: #e9ecef; border-right: 5px solid #495057; flex-direction: row-reverse; text-align: right; }
    [data-testid="chatMessage-user"] > div:first-child { margin-right: 0; margin-left: 1rem; }
    .profile-title { font-size: 1.6rem; font-weight: 700; color: #212529; margin-top: 10px; text-align: center;}
    .profile-subtitle { font-size: 0.95rem; color: #6c757d; margin-bottom: 20px; text-align: center; font-style: italic;}
    .contact-row { display: flex; align-items: center; margin-bottom: 12px; font-size: 0.95rem; }
    .contact-icon { margin-right: 10px; font-size: 1.2rem; }
    .contact-link { text-decoration: none; color: #343a40; transition: color 0.3s; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    col_l, col_m, col_r = st.columns([1, 2, 1])
    
    with col_m:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=130)
        elif os.path.exists("unnamed.jpg"):
            st.image("unnamed.jpg", width=130)
        else:
            st.warning("Logo bulunamadı!")

    st.markdown("<div class='profile-title'>Semih ACAR</div>", unsafe_allow_html=True)
    st.markdown("<div class='profile-subtitle'>Elektrik-Elektronik Mühendisi<br>& Yazılım Geliştirici</div>", unsafe_allow_html=True)
    
    st.write("---")
    # Dinamik bilgileri Sidebar'da da gösterelim
    st.info(f"Teknik uzmanlığın ötesinde, stratejik karar alma ve ekip yönetimi konularında yetkin, vizyoner bir mühendis.")
    
    st.write("---")
    st.subheader("İletişim")
    st.markdown(f"""
        <div class='contact-row'><span class='contact-icon'>📧</span><a href='mailto:semihacar006@gmail.com' class='contact-link'>E-Posta Gönder</a></div>
        <div class='contact-row'><span class='contact-icon'>🔗</span><a href='http://linkedin.com/in/semih-acar-0606-sa' target='_blank' class='contact-link'>LinkedIn</a></div>
        <div class='contact-row'><span class='contact-icon'>📍</span><span>Ankara, Türkiye</span></div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. GEMINI SYSTEM PROMPT (ZAMAN BİLİNCİ EKLENDİ)
# ---------------------------------------------------------
system_instruction = f"""
Sen Semih ACAR'ı temsil eden üst düzey bir AI asistanısın. 

BUGÜNÜN TARİHİ: {TODAY_STR}
(Tüm cevaplarını bu tarihe göre ver. Örneğin kullanıcı "Ne zaman mezun olacak?" derse bugüne göre hesap yap.)

ADAY PROFİLİ:
{CANDIDATE_PROFILE}

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

# ---------------------------------------------------------
# 7. SOHBET ARAYÜZÜ
# ---------------------------------------------------------
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
        message_placeholder = st.empty()
        full_response = ""
        try:
            for chunk in st.session_state.chat_session.send_message(prompt, stream=True):
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        # --- EN ALTTAKİ HATA KISMINI BÖYLE GÜNCELLE ---
        except Exception as e:
            # "Bağlantı hatası" yerine gerçek hatayı yazdırıyoruz
            st.error(f"YAPAY ZEKA HATASI: {e}")