"""
Basit kural-tabanlı (rule-based) karar destek mantığı.
"""

def generate_recommendations(metrics, config):
    """Simülasyon sonuçlarına göre metin tabanlı karar destek önerileri üretir."""
    recommendations = []
    total_time = config.get("simulation_time", 480)
    
    # 1. Teknisyen kullanım oranı kontrolü
    num_techs = config.get("num_technicians", 1)
    if num_techs > 0:
        tech_utilization = (metrics.technician_busy_time / (total_time * num_techs)) * 100
        if tech_utilization > 80:
            recommendations.append(f"🔴 Teknisyen kullanım oranı çok yüksek (%{tech_utilization:.1f}). Bakım süreçlerinde darboğaz yaşanıyor, ek teknisyen eklenebilir veya tamir süreleri iyileştirilebilir.")
        elif tech_utilization < 20:
             recommendations.append(f"🟢 Teknisyen kullanım oranı oldukça düşük (%{tech_utilization:.1f}). Bakım ekibi atıl durumda, farklı alanlara yönlendirilebilirler.")
    elif config.get("breakdown_probability", 0) > 0:
        recommendations.append("🔴 Teknisyen sayısı 0 olmasına rağmen makine arıza olasılığı mevcut! Arıza durumunda sistem tamamen kilitlenecektir. Sisteme teknisyen eklemelisiniz.")
    
    # 2. Makine darboğazı ve kullanım analizi
    high_util_machines = []
    num_machines = config.get("num_machines", 3)
    for machine_id in range(num_machines):
        m_name = f"Makine-{machine_id+1}"
        busy_time = metrics.machine_busy_time.get(m_name, 0)
        util = (busy_time / total_time) * 100
        if util > 85:
            high_util_machines.append(m_name)
            
    if high_util_machines:
        recommendations.append(f"🟠 Darboğaz Uyarısı: {', '.join(high_util_machines)} birimlerinde kapasite kullanımı %85'in üzerinde. Bu makineler hatta darboğaz oluşturuyor olabilir.")
        
    # 3. Kuyruk bekleme süresi kontrolü
    started_jobs = [j for j in metrics.jobs if j.start_time >= 0]
    avg_wait = sum(j.wait_time for j in started_jobs) / len(started_jobs) if started_jobs else 0
    if avg_wait > config.get("mean_process_time", 8) * 3:
        recommendations.append(f"🟠 Ortalama bekleme süresi çok yüksek ({avg_wait:.1f} dk). Parçalar işleme girmek için uzun süre kuyrukta harcıyor. Makine kapasitesi mutlaka artırılmalı veya arıza/duruş süreleri kısaltılmalı.")
        
    # 4. Duruş ve arıza süreleri
    total_downtime = sum(metrics.machine_downtime.values())
    if num_machines > 0 and (total_downtime / (num_machines * total_time)) > 0.20:
        recommendations.append(f"🔴 Toplam duruş süresi kritik seviyede ({total_downtime:.1f} dk). Sistem toplam çalışma vaktinin %20'sinden fazlasını atıl/arızalı geçiriyor. Arıza oranını düşürücü kestirimci bakım yapılmalı.")
        
    if not recommendations:
        recommendations.append("✅ Sistem şu anda dengeli çalışıyor. Belirgin bir darboğaz, kuyruk problemi veya aşırı kaynak sıkıntısı tespit edilmedi.")
        
    return recommendations
