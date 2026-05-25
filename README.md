# 🏭 Fabrika Üretim Hattı ve Darboğaz Simülasyonu

Bu proje, bir fabrikadaki çok aşamalı üretim hattını **Ayrık Olay Simülasyonu (Discrete Event Simulation)** mantığıyla modelleyen dinamik bir benzetim uygulamasıdır. **SimPy** kütüphanesi üzerine kurulan simülasyon motoru; siparişlerin gelişinden itibaren istasyonlar üzerindeki kuyruk yönetimini, makine arızalarını, ortak bakım ekibi (teknisyen) müdahalelerini ve darboğazları gerçekçi bir şekilde taklit eder.

---

## 🚀 Temel Özellikler
- **Ardışık 3 Aşamalı Üretim Hattı:** Siparişler sırasıyla **Kesim**, **Montaj** ve **Paketleme** istasyonlarından geçerek tamamlanır.
- **İstasyon Bazlı Darboğaz (Bottleneck) Analizi:** İstasyonlardaki ortalama bekleme süreleri ve makine kullanım oranları anlık olarak hesaplanarak hattın en yavaş noktası otomatik tespit edilir.
- **Dinamik Streamlit Arayüzü:** Her istasyon için bağımsız makine sayıları, ortalama işlem süreleri ve makine arıza oranları arayüzden anlık olarak simüle edilebilir.
- **Kutu Grafiği (Box Plot) Analizi:** Her istasyonun kuyruk bekleme sürelerinin dağılımını, varyansını ve uç değerlerini yan yana kıyaslayan Plotly tabanlı grafikler içerir.
- **Sentetik Veri İhracı:** Makine öğrenmesi veya veri analizi çalışmalarında kullanılmak üzere simülasyon çıktılarını **Sipariş Verileri (CSV)** ve **Makine Performans Günlükleri (CSV)** olarak indirme desteği sunar.
- **Karar Destek Sistemi:** Simülasyon sonunda rule-based (kural tabanlı) motor çalışarak hat verimliliğini artıracak öneriler üretir.

---

## 🛠️ Kullanılan Teknolojiler
- **Python 3.11+**
- **SimPy**: Ayrık Olay Simülasyon motoru
- **Streamlit**: Web tabanlı veri görselleştirme ve kontrol arayüzü
- **Pandas & NumPy**: Sentetik veri yönetimi ve analizi
- **Plotly**: Etkileşimli veri grafikleri

---

## 📂 Proje Yapısı
```text
├── app.py                     # Ana Streamlit uygulama ve arayüz dosyası
├── requirements.txt           # Gerekli Python kütüphaneleri
├── config/
│   └── default_config.py      # Varsayılan simülasyon ve istasyon parametreleri
├── simulation/
│   ├── engine.py              # SimPy Environment ve kaynak tanımları
│   ├── entities.py            # İş (Job) nesnesi ve aşama zaman damgaları
│   ├── processes.py           # Ardışık akış (Kesim -> Montaj -> Paketleme) kuralları
│   ├── metrics.py             # Metrik toplama ve analiz veri yapısı
│   └── decision_support.py    # Darboğaz saptama ve öneri motoru
└── ui/
    └── charts.py              # Box plot ve makine kullanım grafik çizicileri
```

---

## ⚙️ Kurulum ve Çalıştırma

1. Proje dizininde bir sanal ortam oluşturun ve aktif edin:
   ```bash
   python -m venv venv
   
   # Windows için:
   .\venv\Scripts\activate
   
   # macOS/Linux için:
   source venv/bin/activate
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Simülasyon uygulamasını başlatın:
   ```bash
   streamlit run app.py
   ```

---

## 📊 Simülasyon Senaryoları
Uygulamayı başlattıktan sonra yan paneldeki parametreler ile şu testleri gerçekleştirebilirsiniz:
1. **Hat Dengeleme (Line Balancing):** İstasyonlardaki makine sayılarını ve sürelerini optimize ederek kuyrukları sıfırlamaya çalışın.
2. **Kapasite ve Arıza Analizi:** Yüksek arıza oranlarında onarım teknisyenlerinin doluluk oranını (% Utilization) ve makinelerin arıza duruş sürelerini gözlemleyin.
3. **Sentetik Veri Üretimi:** Simülasyonu çalıştırdıktan sonra alt kısımda beliren butonları kullanarak veri setlerini bilgisayarınıza kaydedin.
