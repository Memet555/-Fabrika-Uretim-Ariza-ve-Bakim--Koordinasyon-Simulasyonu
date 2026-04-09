"""
SimPy süreçlerini (Process) tanımlayan modül.
"""
import simpy
import random
from config.default_config import ARRIVAL_RATES
from simulation.entities import Job

def job_generator(env, config, machine_pool, tech_resource, metrics_collector):
    """Belirli aralıklarla yeni iş (sipariş) üretir."""
    job_id = 0
    arrival_rate_level = config.get("arrival_rate_level", "normal")
    interarrival_time = ARRIVAL_RATES.get(arrival_rate_level, 10.0)
    
    while True:
        job_id += 1
        job = Job(job_id=job_id, arrival_time=env.now)
        metrics_collector.add_job(job)
        
        env.process(process_job(env, job, config, machine_pool, tech_resource, metrics_collector))
        
        # Sonraki iş için bekle (Eksponansiyel dağılım)
        yield env.timeout(random.expovariate(1.0 / max(interarrival_time, 0.1)))

def process_job(env, job, config, machine_pool, tech_resource, metrics_collector):
    """Bir işin makinede işlenmesi, makine arızası ve bakım süreci."""
    # Uygun bir makine talep et, boş makine yoksa bekle (Kuyruk oluşumu)
    machine_id = yield machine_pool.get()
    
    # İş makineye girdi (işlem başlıyor)
    job.start_time = env.now
    
    # Arıza kontrolü (iş başına rastgele arıza olasılığı)
    if random.random() < config.get("breakdown_probability", 0.1):
        metrics_collector.total_breakdowns += 1
        metrics_collector.machine_breakdowns[machine_id] = metrics_collector.machine_breakdowns.get(machine_id, 0) + 1
        start_downtime = env.now
        
        # Bakım teknisyeni talep et (Eğer tüm teknisyenler meşgulse makine burada durur/bekler)
        with tech_resource.request() as tech_req:
            yield tech_req
            # Tamir süresi (Eksponansiyel dağılım)
            repair_time = random.expovariate(1.0 / max(config.get("mean_repair_time", 20.0), 0.1))
            yield env.timeout(repair_time)
            metrics_collector.technician_busy_time += repair_time
            
        downtime = env.now - start_downtime
        metrics_collector.machine_downtime[machine_id] = metrics_collector.machine_downtime.get(machine_id, 0.0) + downtime
    
    # İşi işle (Eksponansiyel dağılım ile işlem süresi)
    process_time = random.expovariate(1.0 / max(config.get("mean_process_time", 8.0), 0.1))
    yield env.timeout(process_time)
    
    # Makinenin üretimde çalıştığı süreyi kaydet
    metrics_collector.machine_busy_time[machine_id] = metrics_collector.machine_busy_time.get(machine_id, 0.0) + process_time
    
    # İşi tamamlandı işaretle
    job.end_time = env.now
    metrics_collector.record_completed_job()
    
    # Makineyi havuza geri bırak ki diğer işler alabilsin
    machine_pool.put(machine_id)
