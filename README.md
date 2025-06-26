USOM IP Adres Analizi ve Görselleştirmesi
Proje Tanımı
Bu Python projesinde, USOM (Ulusal Siber Olaylara Müdahale Merkezi) API'sinden zararlı IP adresleri toplanmakta ve analiz edilmektedir. IP adreslerine ait coğrafi konum bilgileri (ülke, şehir, enlem, boylam) GeoLite2 veritabanı kullanılarak elde edilmektedir. IP adresleri kritiklik seviyelerine göre sıralanmakta ve CSV dosyası olarak kaydedilmektedir. Son olarak, Matplotlib kütüphanesi ile ülkeler bazında ortalama kritiklik seviyelerini görselleştiren bir grafik oluşturulmaktadır.

Özellikler
USOM API'den IP adresleri verisi çekme

GeoLite2 veritabanı ile IP konum bilgilerini sorgulama

Kritik seviyeye göre veri temizleme ve sıralama

CSV dosyası olarak veriyi kaydetme

Ülkelere göre ortalama kritiklik seviyelerini görselleştirme

Gereksinimler
Python 3.x

requests kütüphanesi

geoip2 kütüphanesi

pandas kütüphanesi

matplotlib kütüphanesi

Gerekli kütüphaneleri yüklemek için:

bash
Kopyala
Düzenle
pip install requests geoip2 pandas matplotlib
Kullanım
MaxMind sitesinden GeoLite2 City veritabanını indirip .mmdb dosyasını proje dizinine veya uygun bir klasöre yerleştirin.

Python dosyasındaki GeoLite2 veritabanı yolunu güncelleyin.

ip.py dosyasını çalıştırın:

bash
Kopyala
Düzenle
python ip.py
Program USOM API'den verileri çekip analiz edecek ve usom_ip_geo_data_sorted.csv dosyasını oluşturacaktır.

Ortalama kritiklik seviyelerini gösteren grafik otomatik olarak açılacaktır.

Notlar
API 429 (istek sınırı aşımı) hatası alındığında script 60 saniye bekleyip işlemlere devam eder.

Bazı IP adreslerinin konum bilgileri bulunmayabilir.

