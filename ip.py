import geoip2.database
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

# GeoLite2 veritabanı yolu
geoip2_db_path_city = 'C:/Users/sentu/Desktop/geolite/GeoLite2-City.mmdb'

# USOM API ve GeoLite2 ile IP bilgilerini alıyoruz
def get_all_ip_info():
    all_ip_data = []  # Tüm verileri saklamak için bir liste

    # USOM API'de sayfa döngüsü (1'den 528'e kadar)
    for page in range(1, 529):
        try:
            url = f"https://www.usom.gov.tr/api/address/index?type=ip&page={page}"
            response = requests.get(url)
            
            # 429 hatası alındığında bekleme süresi
            if response.status_code == 429:
                print(f"Sayfa {page} için 429 hatası alındı. Bekliyorum...")
                time.sleep(60)  # 60 saniye bekle
                continue  # Sayfayı atla ve tekrar dene

            response.raise_for_status()  # Hata durumu için kontrol

            data = response.json()
            if data.get("models"):
                for entry in data["models"]:
                    ip = entry.get("url", "Unknown")
                    criticality = entry.get("criticality_level", "Unknown")

                    # GeoLite2 ile IP bilgilerini al
                    try:
                        with geoip2.database.Reader(geoip2_db_path_city) as geoip2_reader:
                            city_info = geoip2_reader.city(ip)
                            country_name = city_info.country.name
                            city_name = city_info.city.name if city_info.city.name else "Unknown"
                            latitude = city_info.location.latitude if city_info.location.latitude else "Unknown"
                            longitude = city_info.location.longitude if city_info.location.longitude else "Unknown"
                    except geoip2.errors.AddressNotFoundError:
                        country_name, city_name, latitude, longitude = "Unknown", "Unknown", "Unknown", "Unknown"
                    except Exception:
                        country_name, city_name, latitude, longitude = "Unknown", "Unknown", "Unknown", "Unknown"

                    # Veriyi kaydet
                    all_ip_data.append({
                        'IP': ip,
                        'Country': country_name,
                        'City': city_name,
                        'Latitude': latitude,
                        'Longitude': longitude,
                        'Criticality': criticality
                    })

            print(f"Sayfa {page}: Başarıyla işlendi.")
        except requests.exceptions.RequestException as e:
            print(f"USOM API'den Sayfa {page} için hata oluştu: {e}")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu (Sayfa {page}): {e}")

    # Verileri 'criticality_level' değerine göre sıralama
    if all_ip_data:
        # Önce criticality_level'ı sayısal değere dönüştürüp sıralama yapalım
        for entry in all_ip_data:
            try:
                entry['Criticality'] = int(entry['Criticality'])
            except ValueError:
                entry['Criticality'] = -1  # Geçersiz olanlar için negatif değer

        # 'Criticality' bazında azalan sırayla sıralama
        sorted_data = sorted(all_ip_data, key=lambda x: x['Criticality'], reverse=True)

        # Pandas DataFrame'e dönüştür
        df = pd.DataFrame(sorted_data)

        # CSV dosyası olarak kaydet
        df.to_csv("usom_ip_geo_data_sorted.csv", index=False, encoding="utf-8")
        print("\nVeriler 'usom_ip_geo_data_sorted.csv' dosyasına kaydedildi.")

        # Verileri görselleştir
        visualize_data(df)
    else:
        print("Herhangi bir veri alınamadı.")

# Matplotlib ile tüm ülkeler için sütun grafiği oluşturma
def visualize_data(df):
    # Ülkelere göre ortalama Criticality değeri
    country_criticality = df.groupby('Country')['Criticality'].mean().sort_values(ascending=False)

    # Sütun grafiği oluştur
    plt.figure(figsize=(12, 8))
    country_criticality.plot(kind='bar', color='skyblue')
    plt.title("Ülkelere Göre Ortalama Kritiklik Seviyesi", fontsize=16)
    plt.xlabel('Ülke', fontsize=12)
    plt.ylabel('Ortalama Kritiklik Seviyesi', fontsize=12)
    plt.xticks(rotation=90, ha='right')
    plt.tight_layout()
    plt.show()

# Fonksiyonu çalıştır
get_all_ip_info()
