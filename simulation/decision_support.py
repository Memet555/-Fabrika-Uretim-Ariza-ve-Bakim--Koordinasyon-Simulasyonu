"""
Basit kural-tabanlı (rule-based) karar destek mantığı.
"""

def generate_recommendations(metrics, config):
    """Simülasyon sonuçlarına göre stage-specific (istasyon bazlı) karar destek önerileri üretir."""
    recommendations = []
    total_time = config.get("simulation_time", 480)
    
    # 1. Teknisyen kullanım oranı kontrolü
    num_techs = config.get("num_technicians", 1)
    if num_techs > 0:
        tech_utilization = (metrics.technician_busy_time / (total_time * num_techs)) * 100
        if tech_utilization > 80:
            recommendations.append(f"🔴 **Bakım Darboğazı:** Teknisyen kullanım oranı çok yüksek (%{tech_utilization:.1f}). Makineler arıza sonrası tamirci bekliyor olabilir. Ek teknisyen istihdamı düşünülmeli.")
        elif tech_utilization < 20:
             recommendations.append(f"🟢 **Bakım Kapasitesi:** Teknisyen kullanım oranı düşük (%{tech_utilization:.1f}). Bakım ekibi atıl kapasitede, farklı görevlere atanabilir.")
    else:
        # Arıza olasılıklarından herhangi biri 0'dan büyükse
        has_breakdowns = (config.get("breakdown_prob_kesim", 0) > 0 or 
                          config.get("breakdown_prob_montaj", 0) > 0 or 
                          config.get("breakdown_prob_paketleme", 0) > 0)
        if has_breakdowns:
            recommendations.append("🔴 **Kritik Risk:** Sistemde teknisyen sayısı 0 olmasına rağmen makine arıza olasılığı tanımlanmış! Herhangi bir arıza hattı tamamen durduracaktır.")
    
    # 2. İstasyon Bazlı Ortalama Bekleme Süreleri ve Darboğaz Tespiti
    started_jobs = [j for j in metrics.jobs if j.start_time_s1 >= 0]
    if started_jobs:
        avg_wait_s1 = sum(j.wait_time_s1 for j in started_jobs) / len(started_jobs)
        avg_wait_s2 = sum(j.wait_time_s2 for j in started_jobs if j.start_time_s2 >= 0) / len([j for j in started_jobs if j.start_time_s2 >= 0]) if any(j.start_time_s2 >= 0 for j in started_jobs) else 0.0
        avg_wait_s3 = sum(j.wait_time_s3 for j in started_jobs if j.start_time_s3 >= 0) / len([j for j in started_jobs if j.start_time_s3 >= 0]) if any(j.start_time_s3 >= 0 for j in started_jobs) else 0.0
        
        waits = [("Kesim", avg_wait_s1), ("Montaj", avg_wait_s2), ("Paketleme", avg_wait_s3)]
        bottleneck_stage, max_wait = max(waits, key=lambda x: x[1])
        
        if max_wait > 5.0: # 5 dakikadan fazla bekleme varsa ciddi darboğaz
            recommendations.append(f"🟠 **Kuyruk/Darboğaz Uyarısı:** En büyük darboğaz **{bottleneck_stage}** aşamasında oluşuyor. Bu istasyondaki ortalama bekleme süresi **{max_wait:.1f} dk**. Buradaki makine sayısını artırmanız veya işlem süresini kısaltmanız gerekir.")
        else:
            recommendations.append(f"✅ **Kuyruk Durumu:** İstasyonlar arasındaki bekleme süreleri dengeli (en fazla {max_wait:.1f} dk). Akış stabil görünüyor.")
            
    # 3. Aşama Bazlı Makine Kullanım Analizleri
    stages = {
        "Kesim": config.get("num_machines_kesim", 3),
        "Montaj": config.get("num_machines_montaj", 2),
        "Paketleme": config.get("num_machines_paketleme", 2)
    }
    
    for stage_name, num_m in stages.items():
        if num_m > 0:
            stage_busy_sum = sum(metrics.machine_busy_time.get(f"{stage_name}-{i+1}", 0.0) for i in range(num_m))
            stage_util = (stage_busy_sum / (total_time * num_m)) * 100
            if stage_util > 85.0:
                recommendations.append(f"🟠 **Kapasite Sınırı:** **{stage_name}** makineleri çok yüksek yoğunlukta çalışıyor (%{stage_util:.1f}). Aşırı yüklenme arıza sıklığını artırabilir.")
            elif stage_util < 30.0:
                recommendations.append(f"🔵 **Düşük Verim:** **{stage_name}** makinelerinin kullanım oranı düşük (%{stage_util:.1f}). Atıl kapasite söz konusu, makine sayısı azaltılabilir.")
                
    if not recommendations:
        recommendations.append("✅ Sistem şu anda dengeli çalışıyor. Belirgin bir darboğaz, kuyruk problemi veya aşırı kaynak sıkıntısı tespit edilmedi.")
        
    return recommendations
