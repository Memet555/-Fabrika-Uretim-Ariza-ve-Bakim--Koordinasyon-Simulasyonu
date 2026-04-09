"""
Arayüz için gerekli Plotly grafiklerini oluşturur.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_machine_utilization(metrics_df, total_time):
    """Makinelerin çalışma ve duruş oranlarını yığılı çubuk grafik (Stacked Bar) ile gösterir."""
    if metrics_df.empty:
        return go.Figure()
        
    fig = go.Figure(data=[
        go.Bar(name='Üretim (Aktif)', x=metrics_df['Makine'], y=metrics_df['Kullanım Oranı (%)'], marker_color='#2ca02c'),
        go.Bar(name='Arıza / Bekleme', x=metrics_df['Makine'], y=metrics_df['Duruş Oranı (%)'], marker_color='#d62728'),
    ])
    
    # Y-Ekseni %100'ü geçmesin
    fig.update_layout(
        barmode='stack', 
        title="Makine Kapasite Kullanım ve Duruş Oranları",
        yaxis=dict(title='Yüzde (%)', range=[0, 105])
    )
    return fig

def plot_wait_times(jobs_df):
    """İşlerin kuyrukta bekleme sürelerinin histogram dağılımını gösterir."""
    if jobs_df.empty:
        return go.Figure()
    fig = px.histogram(
        jobs_df, 
        x='Bekleme Süresi (dk)', 
        nbins=20, 
        title='Sipariş/İş Bekleme Süresi Dağılımı',
        color_discrete_sequence=['#1f77b4'],
        labels={'Bekleme Süresi (dk)': 'Bekleme Süresi (Dakika)', 'count': 'İş Sayısı'}
    )
    return fig

def plot_hourly_heatmap(jobs_df):
    """Zamana (Örn: Saat dilimine) yayılan iş geliş yoğunluğunu ısı haritası olarak gösterir."""
    if jobs_df.empty:
        return go.Figure()
        
    # Geliş zamanını 60 dakikalık (saatlik) dilimlere grupla
    jobs_df['Saat Dilimi'] = (jobs_df['Geliş Zamanı'] // 60).astype(int) + 1
    
    # Her saat başı gelen işlerin toplam sayısını al
    heatmap_data = jobs_df.groupby('Saat Dilimi').size().reset_index(name='Gelen İş Sayısı')
    
    # Sadece görselleştirmek için Y eksenine statik bir değer atayalım ('Hat Yoğunluğu' vb.)
    heatmap_data['Metrik'] = 'Geliş Sıklığı'
    
    fig = px.density_heatmap(
        heatmap_data, 
        x="Saat Dilimi", 
        y="Metrik", 
        z="Gelen İş Sayısı", 
        color_continuous_scale="YlOrRd", 
        title="Zamana Göre Üretim Hattı Yoğunluğu (Isı Haritası)"
    )
    return fig
