import streamlit as st
import pandas as pd
from config.default_config import DEFAULT_CONFIG
from simulation.engine import FactorySimulation
from simulation.decision_support import generate_recommendations
from ui.charts import plot_machine_utilization, plot_wait_times, plot_hourly_heatmap

# Sayfa yapılandırması
st.set_page_config(page_title="Fabrika Simülasyonu", layout="wide", page_icon="🏭")

st.title("🏭 Fabrika Üretim, Arıza ve Bakım Koordinasyon Simülasyonu")
st.markdown("""
> **Problem Tanımı:** Fabrikada makine arızaları ve yetersiz bakım kaynağı nedeniyle üretim hattında gecikmeler, kuyruk birikmeleri ve verim kaybı oluşmaktadır.
""")

# ---- YAN MENÜ (SIDEBAR) KONTROLLERİ ----
st.sidebar.header("⚙️ Simülasyon Parametreleri")

arrival_rate_level = st.sidebar.selectbox(
    "İş/Sipariş Geliş Yoğunluğu",
    options=["düşük", "normal", "yoğun", "çok yoğun"],
    index=1
)

num_machines = st.sidebar.slider("Makine Sayısı", min_value=1, max_value=20, value=DEFAULT_CONFIG["num_machines"])
num_techs = st.sidebar.slider("Teknisyen Sayısı", min_value=0, max_value=10, value=DEFAULT_CONFIG["num_technicians"])
breakdown_prob = st.sidebar.slider("Arıza Olasılığı (İş Başına Düşen %)", min_value=0.0, max_value=0.8, value=DEFAULT_CONFIG["breakdown_probability"], step=0.01)

st.sidebar.markdown("---")
mean_process = st.sidebar.number_input("Ort. İşlem Süresi (dk)", min_value=1.0, max_value=100.0, value=float(DEFAULT_CONFIG["mean_process_time"]))
mean_repair = st.sidebar.number_input("Ort. Tamir Süresi (dk)", min_value=1.0, max_value=100.0, value=float(DEFAULT_CONFIG["mean_repair_time"]))

sim_time = st.sidebar.number_input("Simülasyon Süresi (dk)", min_value=60, max_value=14400, value=DEFAULT_CONFIG["simulation_time"], step=60)
random_seed = st.sidebar.number_input("Rastgelelik Tohumu (Seed)", value=DEFAULT_CONFIG["random_seed"])

run_btn = st.sidebar.button("🚀 Simülasyonu Başlat", use_container_width=True, type="primary")

# ---- SİMÜLASYONU VE ARAYÜZÜ YÜKLE ----
if run_btn:
    # Kullanıcıdan alınan parametreleri config dictionary'sine yükle
    config = {
        "arrival_rate_level": arrival_rate_level,
        "num_machines": num_machines,
        "num_technicians": num_techs,
        "breakdown_probability": breakdown_prob,
        "mean_process_time": mean_process,
        "mean_repair_time": mean_repair,
        "simulation_time": sim_time,
        "random_seed": random_seed
    }
    
    with st.spinner('Simülasyon çalışıyor ve veriler işleniyor...'):
        # Simülasyon motorunu başlat ve çalıştır
        sim = FactorySimulation(config)
        metrics = sim.run()
        
    st.success("✅ Simülasyon başarıyla tamamlandı!")
    
    # Metrikleri hesaplamak için varsayılan zamanlar
    total_time = config["simulation_time"]
    
    # KPI 1-2-3-4-5 Hesaplamaları
    completed_jobs = metrics.total_completed_jobs
    jobs_with_start = [j for j in metrics.jobs if j.start_time >= 0]
    avg_wait = sum(j.wait_time for j in jobs_with_start) / len(jobs_with_start) if jobs_with_start else 0.0
    throughput = completed_jobs / (total_time / 60) if total_time > 0 else 0
    
    # Teknisyen kullanım oranı
    if num_techs > 0:
        tech_util = (metrics.technician_busy_time / (total_time * num_techs)) * 100
    else:
        tech_util = 100.0 if breakdown_prob > 0 else 0.0 # Arıza varsa teknisyen yoksa tıkanır
        
    # --- ÜST KPI KARTLARI ---
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📦 Tamamlanan İş", f"{completed_jobs}")
    col2.metric("⏱️ Ort. Bekleme Süresi", f"{avg_wait:.1f} dk")
    col3.metric("🔧 Toplam Arıza", f"{metrics.total_breakdowns}")
    col4.metric("📈 Throughput (/Saat)", f"{throughput:.1f}")
    
    # Teknisyen kullanımının rengini ayarlamak zor ama Streamlit'te yön gösterici var (delta değil de direkt renk vermek için HTML olabilir, biz sade tutuyoruz)
    col5.metric("👷 Teknisyen Kullanımı", f"%{tech_util:.1f}")
    
    st.markdown("---")
    
    # --- VERİ HAZIRLAMA (DATAFRAMELER) ---
    machine_data = []
    for i in range(num_machines):
        m_name = f"Makine-{i+1}"
        busy = metrics.machine_busy_time.get(m_name, 0.0)
        down = metrics.machine_downtime.get(m_name, 0.0)
        
        util_pct = min((busy / total_time) * 100, 100)
        down_pct = min((down / total_time) * 100, 100)
        
        machine_data.append({
            "Makine": m_name,
            "Kullanım Oranı (%)": util_pct,
            "Duruş Oranı (%)": down_pct
        })
    df_machines = pd.DataFrame(machine_data)
    
    jobs_data = [{
        "İş ID": j.job_id,
        "Geliş Zamanı": j.arrival_time,
        "Bekleme Süresi (dk)": j.wait_time,
        "Sistemde Kalma Süresi (dk)": j.time_in_system
    } for j in jobs_with_start]
    df_jobs = pd.DataFrame(jobs_data)
    
    # --- GRAFİKLER ---
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(plot_machine_utilization(df_machines, total_time), use_container_width=True)
        
    with col_chart2:
        st.plotly_chart(plot_wait_times(df_jobs), use_container_width=True)
        
    col_heat, col_decision = st.columns(2)
    with col_heat:
        st.plotly_chart(plot_hourly_heatmap(df_jobs), use_container_width=True)
        
    with col_decision:
        st.subheader("💡 Karar Destek Sistemi Önerileri")
        st.markdown("Aşağıdaki öneriler simülasyon sonuçlarında oluşan metrikler üzerinden kural bazlı (rule-based) olarak üretilmiştir:")
        recommendations = generate_recommendations(metrics, config)
        for rec in recommendations:
             # Eğer "darboğaz" / "yüksek" geçiyorsa kırmızı / uyarı (warning veya error)
             if "Darboğaz" in rec or "yüksek (" in rec or "0 olmasına rağmen" in rec or "kritik" in rec:
                 st.warning(rec)
             elif "düşük (" in rec:
                 st.info(rec)
             else:
                 st.success(rec)
            
    # --- DETAYLI TABLO ---
    with st.expander("📊 Makine Bazlı Detaylı Çıktı Tablosunu Göster"):
        st.dataframe(df_machines.style.format({
            "Kullanım Oranı (%)": "{:.2f}%", 
            "Duruş Oranı (%)": "{:.2f}%"
        }), use_container_width=True)
        
else:
    st.info("👈 Tüm parametreleri sol panelden ayarlayıp, simülasyonu izlemek için 'Simülasyonu Başlat' butonuna tıklayınız.")
