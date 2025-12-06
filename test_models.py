import google.generativeai as genai
import toml

# Secrets dosyasından anahtarı çek
try:
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["GOOGLE_API_KEY"]
    print("✅ API Anahtarı bulundu.")
except:
    print("❌ HATA: .streamlit/secrets.toml dosyası okunamadı veya anahtar yok.")
    exit()

genai.configure(api_key=api_key)

print("\n🔍 Google Hesabına Tanımlı Modeller Aranıyor...\n")

try:
    found = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"👉 Kullanabileceğin Model İsmi: {m.name}")
            found = True
            
    if not found:
        print("❌ Hiçbir model bulunamadı. API Anahtarında bir sorun olabilir.")
        
except Exception as e:
    print(f"❌ Bir hata oluştu: {e}")

input("\nÇıkmak için Enter'a bas...")