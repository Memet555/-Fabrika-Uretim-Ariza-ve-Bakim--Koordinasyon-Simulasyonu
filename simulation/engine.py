"""
Ana simülasyon orkestrasyon sınıfı.
"""
import simpy
import random
from simulation.metrics import MetricsCollector
from simulation.processes import job_generator

class FactorySimulation:
    """SimPy Environment kurulumu ve kaynakların yönetimi."""
    def __init__(self, config):
        self.config = config
        self.env = simpy.Environment()
        self.metrics = MetricsCollector()
        
        # Tekrar edilebilirlik için
        random.seed(self.config.get("random_seed", 42))
        
        # Bakım teknisyenleri kaynağı
        self.tech_resource = simpy.Resource(self.env, capacity=self.config.get("num_technicians", 1))
        
        # Makineler için ayrık havuz (Her makinenin kendi kimliği olması için Store kullanıldı)
        self.machine_pool = simpy.Store(self.env, capacity=self.config.get("num_machines", 3))
        for i in range(self.config.get("num_machines", 3)):
            self.machine_pool.put(f"Makine-{i+1}")
            
    def run(self):
        """Simülasyon sürecini başlatır ve belirtilen süre kadar işletir."""
        # İş üreten süreci ekle
        self.env.process(job_generator(
            self.env, 
            self.config, 
            self.machine_pool, 
            self.tech_resource, 
            self.metrics
        ))
        
        # Motoru çalıştır
        self.env.run(until=self.config.get("simulation_time", 480))
        
        return self.metrics
