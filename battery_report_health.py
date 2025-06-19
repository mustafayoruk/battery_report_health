import os
import subprocess
import re
from datetime import datetime
import shutil

def save_to_history(timestamp, design, full, health):
    """Sonuçları CSV formatında kaydeder"""
    history_file = "battery_history.csv"
    header = "Tarih,Tasarım Kapasitesi (mWh),Tam Şarj Kapasitesi (mWh),Sağlık (%)\n"
    
    try:
        #Dosya yoksa başlıkla oluştur
        if not os.path.exists(history_file):
            with open(history_file, 'w', encoding='utf-8') as f:
                f.write(header)
        
        #Yeni kaydı ekle
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp},{design},{full},{health:.1f}\n")
        
        print(f"\n📈 Kayıt eklendi: {history_file}")
    except Exception as e:
        print(f"\n⛔ Kayıt hatası: {str(e)}")

def archive_report(report_path, timestamp):
    """Orijinal HTML raporunu arşivler"""
    archive_dir = "pil_rapor_arsivleri"
    try:
        os.makedirs(archive_dir, exist_ok=True)
        archive_file = f"{archive_dir}/rapor_{timestamp.replace(':', '').replace(' ', '_')}.html"
        shutil.copy(report_path, archive_file)
        print(f"📦 Orijinal rapor arşivlendi: {archive_file}")
    except Exception as e:
        print(f"\n⛔ Arşivleme hatası: {str(e)}")

def analyze_battery():
    print("BATTERY ANALYZE FOR WİNDOWS")
    
    #Rapor oluştur
    report_path = "battery-report.html"
    try:
        subprocess.run(
            ['powercfg', '/batteryreport', '/output', report_path],
            check=True, shell=True, capture_output=True, text=True, timeout=30
        )
        print("✓ Rapor oluşturuldu:", report_path)
    except Exception as e:
        print(f"⛔ Hata: {e.stderr if e.stderr else str(e)}")
        return

    #Raporu analiz et
    try:
        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        #Hem İngilizce hem Türkçe kapasite desenleri
        design_patterns = [
            r'Design Capacity\D*(\d+,?\d+)',  # İngilizce
            r'Tasarım Kapasitesi\D*(\d+,?\d+)'  # Türkçe
        ]
        full_charge_patterns = [
            r'Full Charge Capacity\D*(\d+,?\d+)',  # İngilizce
            r'Tam Şarj Kapasitesi\D*(\d+,?\d+)'  # Türkçe
        ]

        design_cap = None
        full_cap = None

        #Tüm desenleri dene
        for pattern in design_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                design_cap = int(match.group(1).replace(',', ''))
                break

        for pattern in full_charge_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                full_cap = int(match.group(1).replace(',', ''))
                break

        if design_cap and full_cap:
            #Birim kontrolü (Wh/mWh)
            if design_cap < 100:  # Wh cinsinden verilmişse
                design_cap *= 1000
                full_cap *= 1000

            health = (full_cap / design_cap) * 100
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            #Sonuçları göster
            print("\n🔋 PİL SAĞLIK SONUÇLARI")
            print("═"*40)
            print(f"📅 Rapor Tarihi: {timestamp}")
            print(f"⚡ Tasarım Kapasitesi: {design_cap:,} mWh")
            print(f"🔌 Tam Şarj Kapasitesi: {full_cap:,} mWh")
            print(f"❤️  Pil Sağlığı: %{health:.1f}")

            #Dosyaya kaydet (CSV formatında)
            save_to_history(timestamp, design_cap, full_cap, health)
            
            #Orijinal raporu arşivle
            archive_report(report_path, timestamp)

            #Sağlık durumu değerlendirmesi
            print("\n📊 DEĞERLENDİRME:")
            if health < 75:
                print("🚨 KRİTİK: Pil değişimi gerekli (%75 altı)")
            elif health < 85:
                print("⚠️ UYARI: Performans düşük (%85 altı)")
            elif health < 95:
                print("🔵 NORMAL: Küçük kapasite kaybı")
            else:
                print("✅ MÜKEMMEL: Fabrika performansında")

        else:
            print("\n⛔ Kapasite değerleri bulunamadı")
            print("ℹ️ HTML raporunu manuel olarak kontrol edin:", report_path)
            backup_path = f"rapor_hata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            shutil.copy(report_path, backup_path)
            print(f"⚠️ Orijinal rapor yedeklendi: {backup_path}")

    except Exception as e:
        print(f"\n⛔ ANALİZ HATASI: {str(e)}")
    finally:
        #Raporu silme (artık koruyoruz)
        print(f"\nℹ️ Rapor korundu: {report_path}")

if __name__ == "__main__":
    analyze_battery()
