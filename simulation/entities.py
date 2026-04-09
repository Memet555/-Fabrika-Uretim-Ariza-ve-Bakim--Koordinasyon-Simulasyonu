"""
Simülasyon varlıklarını (Entity) tanımlar.
"""
from dataclasses import dataclass

@dataclass
class Job:
    """Kuyruğa giren ve makinede işlenen sipariş/iş varlığı."""
    job_id: int
    arrival_time: float
    start_time: float = -1.0
    end_time: float = -1.0

    @property
    def wait_time(self) -> float:
        """Kuyrukta bekleme süresini hesaplar."""
        if self.start_time >= 0:
            return self.start_time - self.arrival_time
        return 0.0

    @property
    def time_in_system(self) -> float:
        """Sisteme giriş ve işin bitişi arasındaki toplam süreyi hesaplar."""
        if self.end_time >= 0:
            return self.end_time - self.arrival_time
        return 0.0
