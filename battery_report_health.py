import os
import subprocess
import re
from datetime import datetime
from bs4 import BeautifulSoup

def analyze_battery():
    print("=== WINDOWS PİL ANALİZ ARACI ===")

    report_path = "battery-report.html"
    try:
        subprocess.run(
            ['powercfg', '/batteryreport', '/output', report_path],
            check=True, shell=True, capture_output=True, text=True, timeout=30
        )
        print(f"✓ Rapor oluşturuldu: {report_path}")
    except Exception as e:
        print(f"⛔ Rapor oluşturma hatası: {str(e)}")
        return

    try:
        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')

        rows = soup.find_all('tr')
        design_cap = full_cap = None

        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                label = cols[0].get_text(strip=True).lower()
                value = cols[1].get_text(strip=True).lower()

                if 'tasarım kapasitesi' in label or 'design capacity' in label:
                    design_cap = int(re.sub(r'[^\d]', '', value))
                    if 'wh' in value and not 'mwh' in value:
                        design_cap *= 1000

                elif 'tam şarj kapasitesi' in label or 'full charge capacity' in label:
                    full_cap = int(re.sub(r'[^\d]', '', value))
                    if 'wh' in value and not 'mwh' in value:
                        full_cap *= 1000

        if design_cap is not None and full_cap is not None:
            health = (full_cap / design_cap) * 100 if design_cap > 0 else 0

            print("\n🔋 PİL SAĞLIK SONUÇLARI")
            print("═"*40)
            print(f"📅 Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⚡ Tasarım Kapasitesi: {design_cap:,} mWh")
            print(f"🔌 Tam Şarj Kapasitesi: {full_cap:,} mWh")
            print(f"❤️  Pil Sağlığı: %{health:.1f}")

            print("\n📊 DEĞERLENDİRME:")
            if health > 105:
                print("🤔 ANORMAL: Bu değer gerçekçi değil (muhtemelen birim hatası)")
            elif health < 75:
                print("🚨 KRİTİK: Pil değişimi gerekli (%75 altı)")
            elif health < 85:
                print("⚠️ UYARI: Performans düşük (%85 altı)")
            elif health < 95:
                print("🔵 NORMAL: Küçük kapasite kaybı")
            else:
                print("✅ MÜKEMMEL: Fabrika performansında")
        else:
            print("\n⛔ Gerekli kapasite değerleri bulunamadı.")

    except Exception as e:
        print(f"\n⛔ ANALİZ HATASI: {str(e)}")
    finally:
        if os.path.exists(report_path):
            os.remove(report_path)
            print("\n♻️ Geçici rapor silindi")

if __name__ == "__main__":
    analyze_battery()
