import pandas as pd
from flask import Blueprint, render_template, request

# Membaca file referensi
file_laki = "./app/data/referensi_imt_laki_laki.csv"
file_perempuan = "./app/data/referensi_imt_perempuan.csv"

# Pastikan CSV memiliki header yang sesuai
df_referensi_laki = pd.read_csv(file_laki, delimiter=";")
df_referensi_perempuan = pd.read_csv(file_perempuan, delimiter=";")

# Fungsi menghitung IMT
def hitung_imt(berat_badan, tinggi_badan_cm):
    tinggi_badan_m = tinggi_badan_cm / 100  # Konversi ke meter
    return berat_badan / (tinggi_badan_m ** 2)

# Fungsi klasifikasi IMT/U
def klasifikasi_imt_u(umur, berat_badan, tinggi_badan_cm, jenis_kelamin="Laki-laki"):
    """
    Mengklasifikasikan status gizi berdasarkan IMT/U.

    Args:
        umur (int): Umur dalam bulan.
        berat_badan (float): Berat badan dalam kg.
        tinggi_badan_cm (float): Tinggi badan dalam cm.
        jenis_kelamin (str): Jenis kelamin ("Laki-laki" atau "Perempuan").

    Returns:
        str: Kategori status gizi.
    """
    # Pilih referensi berdasarkan jenis kelamin
    if jenis_kelamin == "Laki-laki":
        referensi = df_referensi_laki
    elif jenis_kelamin == "Perempuan":
        referensi = df_referensi_perempuan
    else:
        return "Jenis kelamin tidak valid."

    # Hitung IMT
    imt = hitung_imt(berat_badan, tinggi_badan_cm)

    # Filter referensi berdasarkan umur
    referensi = referensi[referensi["Umur (bulan)"] == umur]
    if referensi.empty:
        return "Data referensi tidak ditemukan untuk umur ini."

    # Bandingkan IMT dengan referensi
    z_scores = referensi.iloc[0]
    if imt < z_scores["-3 SD"]:
        return "Gizi Buruk"
    elif z_scores["-3 SD"] <= imt < z_scores["-2 SD"]:
        return "Gizi Kurang"
    elif z_scores["-2 SD"] <= imt <= z_scores["+2 SD"]:
        return "Gizi Baik"
    elif z_scores["+2 SD"] < imt <= z_scores["+3 SD"]:
        return "Gizi Lebih"
    else:
        return "Obesitas"

# Flask Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Halaman pertama dengan tombol 'Mulai Periksa'."""
    return render_template('index.html')

@bp.route('/form', methods=['GET', 'POST'])
def form():
    """Halaman kedua dengan form input data balita."""
    if request.method == 'POST':
        data = {
            'nama': request.form['nama'],
            'jenis_kelamin': request.form['jenis_kelamin'],
            'umur': int(request.form['umur']),
            'berat_badan': float(request.form['berat_badan']),
            'tinggi_badan': float(request.form['tinggi_badan'])
        }
        # Gunakan fungsi classify untuk klasifikasi
        result = classify(data)
        return render_template('result.html', data=data, result=result)
    return render_template('form.html')

def classify(data):
    """Fungsi untuk klasifikasi status gizi."""
    umur = data['umur']
    berat_badan = data['berat_badan']
    tinggi_badan = data['tinggi_badan']
    jenis_kelamin = data['jenis_kelamin']
    
    # Gunakan fungsi klasifikasi IMT/U
    return klasifikasi_imt_u(umur, berat_badan, tinggi_badan, jenis_kelamin)
