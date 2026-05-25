"""
Varsayılan yapılandırma ayarlarını içerir.
"""

# Yoğunluk seviyelerine göre geliş aralıkları (interarrival times) dakika cinsinden
ARRIVAL_RATES = {
    "düşük": 15,
    "normal": 10,
    "yoğun": 5,
    "çok yoğun": 2
}

DEFAULT_CONFIG = {
    "arrival_rate_level": "normal", # düşük, normal, yoğun, çok yoğun
    
    # Makine Sayıları
    "num_machines_kesim": 3,
    "num_machines_montaj": 2,
    "num_machines_paketleme": 2,
    
    # Ortalama İşlem Süreleri (dakika)
    "mean_process_kesim": 6.0,
    "mean_process_montaj": 10.0,
    "mean_process_paketleme": 5.0,
    
    # Arıza Olasılıkları (% olarak iş başına)
    "breakdown_prob_kesim": 0.05,
    "breakdown_prob_montaj": 0.10,
    "breakdown_prob_paketleme": 0.03,
    
    # Ortak Kaynaklar
    "num_technicians": 1,
    "mean_repair_time": 15.0, # Ortak teknisyenlerin ortalama tamir süresi
    
    "simulation_time": 480, # 8 saatlik bir vardiya (dakika cinsinden)
    "random_seed": 42
}
