# Fabrika Üretim, Arıza ve Bakım Koordinasyon Simülasyonu

## Proje Özeti
Bu proje, bir fabrikadaki üretim hattını SimPy kütüphanesini kullanarak ayrık olay simülasyonu mantığında modellemektedir. Sistem dahilindeki işlerin varışı, makinelerde işlenmesi, olası arızalar ve onarım teknisyeni müdahaleleri gerçekçi fakat sade bir yaklaşımla modellenmiştir. Streamlit arayüzü sayesinde kullanıcı, ilgili parametreleri değiştirerek anlık analizler yapabilir ve sistem dar boğazlarını görebilir.

## Kullanılan Teknolojiler
- **Python 3.11+**
- **SimPy**: Ayrık Olay Simülasyon motoru
- **Streamlit**: Veri görselleştirme ve kullanıcı arayüzü
- **Pandas & NumPy**: Veri manipülasyonu 
- **Plotly**: Etkileşimli grafikler

## Problem Tanımı
**"Fabrikada makine arızaları ve yetersiz bakım kaynağı nedeniyle üretim hattında gecikmeler, kuyruk birikmeleri ve verim kaybı oluşmaktadır."**
Bu temel problemi test edip gözlemleyebilmek amacıyla hazırlanan uygulama; yoğunluk veya az kaynak durumunda bekleme süresi artışını tespit etmeyi sağlar.

## Temel Özellikler
- **Kuyruk ve Darboğaz Analizi**: Farklı senaryolarda nerede kuyruk biriktiği saptanır. 
- **Makine Arızaları ve Teknisyen Yönetimi**: Sınırlı bakım personeli kısıtı ile onarım süreçleri taklit edilir.
- **Dinamik Streamlit UI**: İşlem süresi, seed, arıza oranı gibi tüm parametreleri UI'dan ayarlayabilirsiniz.
- **Karar Destek Sistemi**: Simülasyon sonunda hesaplanmış metrikleri inceleyerek "teknisyen eklenmesi düşünülebilir", "darboğaz mevcut" gibi öneriler üretir.

## Kurulum Adımları
1. Proje dizininde (cmd/powershell) Python sanal ortamı oluşturun ve aktif edin (Önerilen):
   ```bash
   python -m venv venv
   
   # Windows için:
   .\venv\Scripts\activate
   
   # macOS/Linux için:
   # source venv/bin/activate
   ```

2. Gerekli kütüphaneleri indirin:
   ```bash
   pip install -r requirements.txt
   ```

## Çalıştırma Komutu
```bash
streamlit run app.py
```

## Örnek Kullanım
1. Uygulama açılınca sol menüden "İş Geliş Yoğunluğu" seçin.
2. Makine ve teknisyen sayılarını belirleyin.
3. Arıza olasılığını %0'dan %50'ye kadar teste tutabilirsiniz.
4. "Simülasyonu Başlat" butonuna tıklayıp grafikleri ve darboğaz saptamalarını inceleyin.

## Ekran Görüntüleri
Uygulama arayüzünden ve elde edilen analizlerden bazı görseller images kloseründe.

## KPI Açıklamaları
- **Tamamlanan İş**: Tüm simülasyon süresi boyunca üretilen iş.
- **Ortalama Bekleme**: İşlerin ilk kuyruğa girdikten sonra makineye girmesi için harcadığı ortalama vakit.
- **Toplam Arıza**: Gerçekleşen toplam makine bozulma sayısı.
- **Throughput (Saatlik)**: 1 simülasyon saatinde ortalama çıkarılan iş (verim).
- **Teknisyen Kullanımı**: Bakımcıların meşguliyet oranı. Yüksekse arıza onarımları kuyruğa girer.

## Proje Mimarisi
- `app.py`: Ana Streamlit giriş noktası ve UI çizicisi.
- `simulation/`: SimPy motorunun (engine.py), varlıkların (entities.py), süreçlerin (processes.py) bulunduğu çekirdek mekanizma. Ayrıca karar destek raporu (decision_support.py) üretilir.
- `ui/`: Plotly gibi kütüphaneler ile çizilen veri görsellerinin olduğu modül.
- `config/`: Parametre değerleri.

## Geliştirilebilecek Yönler
- AI destekli kararlar kullanılabilir.
- Öncelikli bakım veya VIP işler için Priority Resource eklenebilir.
