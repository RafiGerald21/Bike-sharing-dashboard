Setup Environment

Anaconda

# 1. Buat environment baru
conda create --name main-ds python=3.11

# 2. Aktifkan environment
conda activate main-ds

# 3. Masuk ke folder proyek (yang berisi dashboard.py dan requirements.txt)
cd proyek_analisis_data

# 4. Pasang seluruh library
pip install -r requirements.txt
Venv
# 1. Masuk ke folder proyek
cd proyek_analisis_data

# 2. Buat virtual environment baru
python -m venv venv

# 3. Aktifkan environment
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# 4. Pasang seluruh library
pip install -r requirements.txt
Running Streamlit

Pastikan environment sudah aktif dan terminal berada di folder yang berisi dashboard.py beserta file datanya (.csv), lalu jalankan:

bash
streamlit run dashboard.py
Dashboard akan terbuka otomatis di browser. Jika tidak, buka alamat yang tampil di terminal, biasanya di http://localhost:8501.

 

## Deskripsi Proyek
Proyek analisis data ini bertujuan untuk mengeksplorasi **Bike Sharing Dataset**. Analisis difokuskan pada:
1. Pengaruh kondisi cuaca dan musim terhadap jumlah penyewaan sepeda harian.
2. Perbedaan pola penyewaan sepeda antara pengguna kasual (*casual*) dan pengguna terdaftar (*registered*) pada hari kerja dibandingkan hari libur selama periode 2011 hingga 2012.
 
## Struktur Direktori
```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt
