"""
Genel yardımcı fonksiyonlar
"""

def format_time(minutes: float) -> str:
    """
    Dakika cinsinden süreyi okunabilir 'X saat Y dakika' formatına çevirir.
    """
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    if hours > 0:
        return f"{hours}s {mins}d"
    return f"{mins}d"
