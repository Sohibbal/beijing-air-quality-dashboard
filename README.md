# 🌫️ Beijing Air Quality Data Analysis

Proyek analisis data kualitas udara Beijing (2013-2017) untuk Submission Dicoding - Belajar Analisis Data dengan Python.

## 📊 Dataset

Air Quality Dataset dari UCI Machine Learning Repository berisi data kualitas udara dari 12 stasiun monitoring di Beijing dengan 17,000+ records per stasiun dari Maret 2013 hingga Februari 2017.

**Polutan yang diukur:**
- **PM2.5, PM10**: Particulate matter (partikel debu halus)
- **SO2, NO2, CO, O3**: Gas polutan
- **TEMP, PRES, DEWP, RAIN, WSPM**: Data meteorologi

## 🎯 Pertanyaan Bisnis

1. **Bagaimana pola temporal polusi udara (PM2.5) di Beijing dari tahun 2013-2017, dan apakah terdapat perbedaan signifikan antar musim serta antar jam dalam sehari?**

2. **Bagaimana distribusi geografis tingkat polusi udara di berbagai stasiun monitoring di Beijing, dan stasiun mana yang memiliki kualitas udara paling buruk?**

## 📁 Struktur Proyek

```
Submission/
├── dashboard/
│   ├── dashboard.py          # Streamlit dashboard
│   └── README.md             # Dashboard documentation
├── data/
│   ├── PRSA_Data_*.csv       # Raw data (12 stasiun)
│   └── cleaned_air_quality.csv  # Processed data (generated from notebook)
├── notebook.ipynb            # Jupyter notebook analisis lengkap
├── requirements.txt          # Python dependencies
└── README.md                 # Dokumentasi proyek
```

## 🚀 Setup & Installation

### 1. Clone atau Download Repository

```bash
git clone <repo-url>
cd Submission
```

### 2. Install Dependencies

Pastikan Anda memiliki Python 3.8+ terinstall, kemudian:

```bash
pip install -r requirements.txt
```

**Catatan**: Untuk dashboard, install juga:
```bash
pip install streamlit-folium
```

### 3. Jalankan Jupyter Notebook

```bash
jupyter notebook notebook.ipynb
```

Jalankan semua cell dari awal hingga akhir. Notebook akan:
- Load dan membersihkan data dari 12 stasiun
- Melakukan EDA dan visualisasi
- Generate file `cleaned_air_quality.csv` untuk dashboard
- Menampilkan analisis lanjutan (geospatial, clustering, temporal binning)

### 4. Jalankan Streamlit Dashboard

Setelah notebook selesai dijalankan:

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## 🌐 Live Dashboard

Dashboard dapat diakses online di: **[Coming Soon - Streamlit Cloud]**

## 📈 Hasil Analisis

### Insight Utama:

1. **Pola Temporal**:
   - Polusi PM2.5 tertinggi terjadi di musim **dingin** (Desember-Februari), rata-rata mencapai >100 µg/m³
   - Polusi terendah di musim **summer** (Juni-Agustus), rata-rata ~60 µg/m³
   - Pola harian menunjukkan puncak polusi di **jam sibuk** pagi (7-9 AM) dan sore (5-7 PM)

2. **Distribusi Geografis**:
   - Stasiun dengan kualitas udara **terburuk**: Gucheng, Wanshouxigong, Dongsi
   - Stasiun dengan kualitas udara **terbaik**: Dingling, Huairou (area pinggiran Beijing)
   - Perbedaan signifikan antara pusat kota vs pinggiran (hingga 30% lebih rendah)

3. **Korelasi**:
   - PM2.5 dan PM10 berkorelasi sangat kuat (r > 0.9)
   - Suhu berkorelasi negatif dengan polusi (-0.4)
   - Tekanan udara berkorelasi positif dengan polusi (+0.3)

### Analisis Lanjutan yang Diterapkan:

✅ **Geospatial Analysis**: Visualisasi peta distribusi polusi menggunakan Folium dengan marker interaktif untuk setiap stasiun

✅ **Clustering Analysis**: Manual grouping stasiun menjadi 4 cluster (Low, Medium, High, Very High) berdasarkan rata-rata PM2.5

✅ **Temporal Binning**: Analisis pola musiman (4 musim) dan pola harian (rush hour vs non-rush hour)

## 🎨 Fitur Dashboard

- 📊 **Interactive Visualizations**: Charts yang dapat di-zoom dan di-filter
- 🗺️ **Geospatial Map**: Peta interaktif Beijing dengan marker stasiun
- ⏰ **Temporal Analysis**: Analisis pola musiman dan harian
- 🎯 **Advanced Analytics**: Clustering dan correlation analysis
- 🎛️ **Dynamic Filters**: Filter berdasarkan tanggal, stasiun, dan polutan
- 📈 **KPI Metrics**: Ringkasan statistik real-time

## 📝 Teknologi yang Digunakan

- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Geospatial**: Folium
- **Dashboard**: Streamlit
- **Analysis**: SciPy untuk statistical testing

## 👤 Author

**Nama**: [Masukkan Nama Anda]  
**Email**: [Masukkan Email Anda]  
**Dicoding ID**: [Masukkan ID Dicoding Anda]

## 📚 Data Source

Dataset: [Beijing Multi-Site Air-Quality Data - UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data)

Citation: Zhang, S., Guo, B., Dong, A., He, J., Xu, Z. and Chen, S.X. (2017) Cautionary Tales on Air-Quality Improvement in Beijing, Proceedings of the Royal Society A, Volume 473, No. 2205, September.

## 📄 License

Proyek ini dibuat untuk keperluan submission Dicoding. Dataset bersumber dari UCI ML Repository.
