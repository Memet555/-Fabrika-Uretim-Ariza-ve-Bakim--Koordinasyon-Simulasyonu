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
    "num_machines": 3,
    "num_technicians": 1,
    "breakdown_probability": 0.1, # 0.0 - 1.0 arası
    "mean_process_time": 8,
    "mean_repair_time": 20,
    "simulation_time": 480, # 8 saatlik bir vardiya (dakika cinsinden)
    "random_seed": 42
}
