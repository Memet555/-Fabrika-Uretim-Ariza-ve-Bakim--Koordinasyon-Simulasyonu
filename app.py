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

# 1. Genel Sipariş & Bakım Ayarları
with st.sidebar.expander("🛒 Sipariş ve Bakım Kaynakları", expanded=True):
    arrival_rate_level = st.selectbox(
        "İş/Sipariş Geliş Yoğunluğu",
        options=["düşük", "normal", "yoğun", "çok yoğun"],
        index=1
    )
    num_techs = st.slider("Teknisyen Sayısı", min_value=0, max_value=10, value=DEFAULT_CONFIG["num_technicians"])
    mean_repair = st.number_input("Ort. Tamir Süresi (dk)", min_value=1.0, max_value=100.0, value=float(DEFAULT_CONFIG["mean_repair_time"]))

# 2. Aşama 1: Kesim İstasyonu
with st.sidebar.expander("🪵 1. Aşama: Kesim İstasyonu", expanded=False):
    num_machines_kesim = st.slider("Kesim Makine Sayısı", min_value=1, max_value=10, value=DEFAULT_CONFIG["num_machines_kesim"])
    mean_process_kesim = st.number_input("Kesim Süresi (dk)", min_value=1.0, max_value=100.0, value=float(DEFAULT_CONFIG["mean_process_kesim"]))
    breakdown_prob_kesim = st.slider("Kesim Arıza Oranı (%)", min_value=0.0, max_value=0.8, value=DEFAULT_CONFIG["breakdown_prob_kesim"], step=0.01)

# 3. Aşama 2: Montaj İstasyonu
with st.sidebar.expander("⚙️ 2. Aşama: Montaj İstasyonu", expanded=False):
    num_machines_montaj = st.slider("Montaj Makine Sayısı", min_value=1, max_value=10, value=DEFAULT_CONFIG["num_machines_montaj"])
    mean_process_montaj = st.number_input("Montaj Süresi (dk)", min_value=1.0, max_value=100.0, value=float(DEFAULT_CONFIG["mean_process_montaj"]))
    breakdown_prob_montaj = st.slider("Montaj Arıza Oranı (%)", min_value=0.0, max_value=0.8, value=DEFAULT_CONFIG["breakdown_prob_montaj"], step=0.01)

# 4. Aşama 3: Paketleme İstasyonu
with st.sidebar.expander("📦 3. Aşama: Paketleme İstasyonu", expanded=False):
    num_machines_paketleme = st.slider("Paketleme Makine Sayısı", min_value=1, max_value=10, value=DEFAULT_CONFIG["num_machines_paketleme"])
    mean_process_paketleme = st.number_input("Paketleme Süresi (dk)", min_value=1.0, max_value=100.0, value=float(DEFAULT_CONFIG["mean_process_paketleme"]))
    breakdown_prob_paketleme = st.slider("Paketleme Arıza Oranı (%)", min_value=0.0, max_value=0.8, value=DEFAULT_CONFIG["breakdown_prob_paketleme"], step=0.01)

# 5. Genel Zaman & Tohum Ayarları
with st.sidebar.expander("🕒 Zaman ve Güvenilirlik", expanded=False):
    sim_time = st.number_input("Simülasyon Süresi (dk)", min_value=60, max_value=14400, value=DEFAULT_CONFIG["simulation_time"], step=60)
    random_seed = st.number_input("Rastgelelik Tohumu (Seed)", value=DEFAULT_CONFIG["random_seed"])

run_btn = st.sidebar.button("🚀 Simülasyonu Başlat", use_container_width=True, type="primary")

# ---- SİMÜLASYONU VE ARAYÜZÜ YÜKLE ----
if run_btn:
    # Kullanıcıdan alınan parametreleri config dictionary'sine yükle
    config = {
        "arrival_rate_level": arrival_rate_level,
        "num_machines_kesim": num_machines_kesim,
        "num_machines_montaj": num_machines_montaj,
        "num_machines_paketleme": num_machines_paketleme,
        
        "mean_process_kesim": mean_process_kesim,
        "mean_process_montaj": mean_process_montaj,
        "mean_process_paketleme": mean_process_paketleme,
        
        "breakdown_prob_kesim": breakdown_prob_kesim,
        "breakdown_prob_montaj": breakdown_prob_montaj,
        "breakdown_prob_paketleme": breakdown_prob_paketleme,
        
        "num_technicians": num_techs,
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
    
    # KPI Hesaplamaları
    completed_jobs = metrics.total_completed_jobs
    started_jobs = [j for j in metrics.jobs if j.start_time_s1 >= 0]
    
    # Ortalama bekleme süreleri
    avg_wait = sum(j.total_wait_time for j in started_jobs) / len(started_jobs) if started_jobs else 0.0
    throughput = completed_jobs / (total_time / 60) if total_time > 0 else 0
    
    # Teknisyen kullanım oranı
    if num_techs > 0:
        tech_util = (metrics.technician_busy_time / (total_time * num_techs)) * 100
    else:
        has_breakdowns = (breakdown_prob_kesim > 0 or breakdown_prob_montaj > 0 or breakdown_prob_paketleme > 0)
        tech_util = 100.0 if has_breakdowns else 0.0
        
    # --- ÜST KPI KARTLARI ---
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📦 Tamamlanan Sipariş", f"{completed_jobs}")
    col2.metric("⏱️ Ort. Toplam Bekleme", f"{avg_wait:.1f} dk")
    col3.metric("🔧 Toplam Arıza", f"{metrics.total_breakdowns}")
    col4.metric("📈 Throughput (/Saat)", f"{throughput:.1f}")
    col5.metric("👷 Teknisyen Kullanımı", f"%{tech_util:.1f}")
    
    st.markdown("---")
    
    # --- VERİ HAZIRLAMA (DATAFRAMELER) ---
    machine_data = []
    # Kesim Makineleri
    for i in range(num_machines_kesim):
        m_name = f"Kesim-{i+1}"
        busy = metrics.machine_busy_time.get(m_name, 0.0)
        down = metrics.machine_downtime.get(m_name, 0.0)
        util_pct = min((busy / total_time) * 100, 100)
        down_pct = min((down / total_time) * 100, 100)
        machine_data.append({
            "İstasyon": "Kesim",
            "Makine": m_name,
            "Kullanım Oranı (%)": util_pct,
            "Duruş Oranı (%)": down_pct
        })
    # Montaj Makineleri
    for i in range(num_machines_montaj):
        m_name = f"Montaj-{i+1}"
        busy = metrics.machine_busy_time.get(m_name, 0.0)
        down = metrics.machine_downtime.get(m_name, 0.0)
        util_pct = min((busy / total_time) * 100, 100)
        down_pct = min((down / total_time) * 100, 100)
        machine_data.append({
            "İstasyon": "Montaj",
            "Makine": m_name,
            "Kullanım Oranı (%)": util_pct,
            "Duruş Oranı (%)": down_pct
        })
    # Paketleme Makineleri
    for i in range(num_machines_paketleme):
        m_name = f"Paketleme-{i+1}"
        busy = metrics.machine_busy_time.get(m_name, 0.0)
        down = metrics.machine_downtime.get(m_name, 0.0)
        util_pct = min((busy / total_time) * 100, 100)
        down_pct = min((down / total_time) * 100, 100)
        machine_data.append({
            "İstasyon": "Paketleme",
            "Makine": m_name,
            "Kullanım Oranı (%)": util_pct,
            "Duruş Oranı (%)": down_pct
        })
        
    df_machines = pd.DataFrame(machine_data)
    
    jobs_data = [{
        "İş ID": j.job_id,
        "Geliş Zamanı": j.arrival_time,
        "Kesim Bekleme (dk)": j.wait_time_s1,
        "Montaj Bekleme (dk)": j.wait_time_s2,
        "Paketleme Bekleme (dk)": j.wait_time_s3,
        "Toplam Bekleme (dk)": j.total_wait_time,
        "Sistemde Kalma Süresi (dk)": j.time_in_system
    } for j in started_jobs]
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
             if "Darboğaz" in rec or "Risk" in rec or "Uyarısı" in rec:
                 st.warning(rec)
             elif "Düşük" in rec:
                 st.info(rec)
             else:
                 st.success(rec)
                 
    # --- SENTETİK VERİ İNDİRME ALANI ---
    st.markdown("---")
    st.subheader("📥 Sentetik Simülasyon Verilerini Dışa Aktar")
    st.markdown("Veri analizi, optimizasyon veya makine öğrenmesi modelleri eğitmek için simülasyon çıktılarını indirebilirsiniz:")
    
    csv_jobs = df_jobs.to_csv(index=False).encode('utf-8')
    csv_machines = df_machines.to_csv(index=False).encode('utf-8')
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📄 Sipariş Geliş ve Bekleme Verilerini İndir (CSV)",
            data=csv_jobs,
            file_name="sentetik_siparis_verileri.csv",
            mime="text/csv",
            key="download_jobs_csv",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label="⚙️ Makine Performans ve Duruş Verilerini İndir (CSV)",
            data=csv_machines,
            file_name="sentetik_makine_verileri.csv",
            mime="text/csv",
            key="download_machines_csv",
            use_container_width=True
        )
            
    # --- DETAYLI TABLO ---
    with st.expander("📊 Makine Bazlı Detaylı Çıktı Tablosunu Göster"):
        st.dataframe(df_machines.style.format({
            "Kullanım Oranı (%)": "{:.2f}%", 
            "Duruş Oranı (%)": "{:.2f}%"
        }), use_container_width=True)
        
else:
    st.info("👈 Tüm parametreleri sol panelden ayarlayıp, simülasyonu izlemek için 'Simülasyonu Başlat' butonuna tıklayınız.")
