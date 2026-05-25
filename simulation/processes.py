"""
SimPy süreçlerini (Process) tanımlayan modül.
"""
import simpy
import random
from config.default_config import ARRIVAL_RATES
from simulation.entities import Job

def job_generator(env, config, pool_kesim, pool_montaj, pool_paketleme, tech_resource, metrics_collector):
    """Belirli aralıklarla yeni iş (sipariş) üretir."""
    job_id = 0
    arrival_rate_level = config.get("arrival_rate_level", "normal")
    interarrival_time = ARRIVAL_RATES.get(arrival_rate_level, 10.0)
    
    while True:
        job_id += 1
        job = Job(job_id=job_id, arrival_time=env.now)
        metrics_collector.add_job(job)
        
        env.process(process_job(env, job, config, pool_kesim, pool_montaj, pool_paketleme, tech_resource, metrics_collector))
        
        # Sonraki iş için bekle (Eksponansiyel dağılım)
        yield env.timeout(random.expovariate(1.0 / max(interarrival_time, 0.1)))

def run_stage(env, job, stage_name, machine_pool, tech_resource, mean_process_time, breakdown_probability, mean_repair_time, metrics_collector):
    """Bir siparişin tek bir aşamadaki (Kesim/Montaj/Paketleme) tüm sürecini (Kuyruk, Arıza, İşlem) yürütür."""
    # Uygun bir makine talep et, boş makine yoksa bekle (Kuyruk)
    machine_id = yield machine_pool.get()
    
    # Aşamaya giriş zamanını kaydet
    if stage_name == "kesim":
        job.start_time_s1 = env.now
    elif stage_name == "montaj":
        job.start_time_s2 = env.now
    elif stage_name == "paketleme":
        job.start_time_s3 = env.now
        
    # Arıza kontrolü (iş başına rastgele arıza olasılığı)
    if random.random() < breakdown_probability:
        metrics_collector.total_breakdowns += 1
        metrics_collector.machine_breakdowns[machine_id] = metrics_collector.machine_breakdowns.get(machine_id, 0) + 1
        start_downtime = env.now
        
        # Ortak bakım teknisyeni talep et (Teknisyen meşgulse makine bekler)
        with tech_resource.request() as tech_req:
            yield tech_req
            # Tamir süresi (Eksponansiyel dağılım)
            repair_time = random.expovariate(1.0 / max(mean_repair_time, 0.1))
            yield env.timeout(repair_time)
            metrics_collector.technician_busy_time += repair_time
            
        downtime = env.now - start_downtime
        metrics_collector.machine_downtime[machine_id] = metrics_collector.machine_downtime.get(machine_id, 0.0) + downtime
    
    # İşi işle (Eksponansiyel dağılım ile işlem süresi)
    process_time = random.expovariate(1.0 / max(mean_process_time, 0.1))
    yield env.timeout(process_time)
    
    # Makinenin aktif çalışma süresini kaydet
    metrics_collector.machine_busy_time[machine_id] = metrics_collector.machine_busy_time.get(machine_id, 0.0) + process_time
    
    # Aşama bitiş zamanını kaydet
    if stage_name == "kesim":
        job.end_time_s1 = env.now
    elif stage_name == "montaj":
        job.end_time_s2 = env.now
    elif stage_name == "paketleme":
        job.end_time_s3 = env.now
        
    # Makineyi havuza geri bırak ki diğer işler alabilsin
    machine_pool.put(machine_id)

def process_job(env, job, config, pool_kesim, pool_montaj, pool_paketleme, tech_resource, metrics_collector):
    """Bir siparişin tüm üretim hattı boyunca (Kesim -> Montaj -> Paketleme) sırayla akmasını sağlar."""
    # 1. Aşama: Kesim
    yield env.process(run_stage(
        env, job, "kesim", pool_kesim, tech_resource,
        config.get("mean_process_kesim", 6.0),
        config.get("breakdown_prob_kesim", 0.05),
        config.get("mean_repair_time", 15.0),
        metrics_collector
    ))
    
    # 2. Aşama: Montaj
    yield env.process(run_stage(
        env, job, "montaj", pool_montaj, tech_resource,
        config.get("mean_process_montaj", 10.0),
        config.get("breakdown_prob_montaj", 0.10),
        config.get("mean_repair_time", 15.0),
        metrics_collector
    ))
    
    # 3. Aşama: Paketleme
    yield env.process(run_stage(
        env, job, "paketleme", pool_paketleme, tech_resource,
        config.get("mean_process_paketleme", 5.0),
        config.get("breakdown_prob_paketleme", 0.03),
        config.get("mean_repair_time", 15.0),
        metrics_collector
    ))
    
    # Tüm aşamalar bittiğinde işi tamamlandı olarak işaretle
    metrics_collector.record_completed_job()
