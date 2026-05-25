"""
Simülasyon varlıklarını (Entity) tanımlar.
"""
from dataclasses import dataclass

@dataclass
class Job:
    """Kuyruğa giren ve makinede işlenen sipariş/iş varlığı (Kesim, Montaj, Paketleme aşamalı)."""
    job_id: int
    arrival_time: float
    
    # Aşama 1: Kesim
    start_time_s1: float = -1.0
    end_time_s1: float = -1.0
    
    # Aşama 2: Montaj
    start_time_s2: float = -1.0
    end_time_s2: float = -1.0
    
    # Aşama 3: Paketleme
    start_time_s3: float = -1.0
    end_time_s3: float = -1.0

    @property
    def wait_time_s1(self) -> float:
        if self.start_time_s1 >= 0:
            return self.start_time_s1 - self.arrival_time
        return 0.0

    @property
    def wait_time_s2(self) -> float:
        if self.start_time_s2 >= 0 and self.end_time_s1 >= 0:
            return self.start_time_s2 - self.end_time_s1
        return 0.0

    @property
    def wait_time_s3(self) -> float:
        if self.start_time_s3 >= 0 and self.end_time_s2 >= 0:
            return self.start_time_s3 - self.end_time_s2
        return 0.0

    @property
    def total_wait_time(self) -> float:
        return self.wait_time_s1 + self.wait_time_s2 + self.wait_time_s3

    @property
    def time_in_system(self) -> float:
        """Sisteme giriş ve işin tamamen bitişi (Aşama 3 sonu) arasındaki toplam süre."""
        if self.end_time_s3 >= 0:
            return self.end_time_s3 - self.arrival_time
        return 0.0
