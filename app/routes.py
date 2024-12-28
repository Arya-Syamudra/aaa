import pandas as pd
from flask import Blueprint, render_template, request

# Membaca file referensi
file_laki = "./app/data/referensi_imt_laki_laki_balita.csv"
file_perempuan = "./app/data/referensi_imt_perempuan_balita.csv"
file_laki_remaja = "./app/data/referensi_imt_laki_laki_remaja.csv"
file_perempuan_remaja = "./app/data/referensi_imt_perempuan_remaja.csv"

df_referensi_laki = pd.read_csv(file_laki, delimiter=";")
df_referensi_perempuan = pd.read_csv(file_perempuan, delimiter=";")
df_referensi_laki_remaja = pd.read_csv(file_laki_remaja, delimiter=";")
df_referensi_perempuan_remaja = pd.read_csv(file_perempuan_remaja, delimiter=";")

def hitung_imt(berat_badan, tinggi_badan_cm):
    tinggi_badan_m = tinggi_badan_cm / 100
    return berat_badan / (tinggi_badan_m ** 2)

def klasifikasi_imt_u(umur, berat_badan, tinggi_badan_cm, jenis_kelamin):
    if jenis_kelamin == "Laki-laki":
        referensi = df_referensi_laki
    elif jenis_kelamin == "Perempuan":
        referensi = df_referensi_perempuan
    else:
        return "Jenis kelamin tidak valid."

    imt = hitung_imt(berat_badan, tinggi_badan_cm)
    referensi = referensi[referensi["Umur (bulan)"] == umur]
    if referensi.empty:
        return "Data referensi tidak ditemukan untuk umur ini."

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

def klasifikasi_imt_u_remaja(tahun, bulan, berat_badan, tinggi_badan_cm, jenis_kelamin):
    if jenis_kelamin == "Laki-laki":
        referensi = df_referensi_laki_remaja
    elif jenis_kelamin == "Perempuan":
        referensi = df_referensi_perempuan_remaja
    else:
        return "Jenis kelamin tidak valid."

    imt = hitung_imt(berat_badan, tinggi_badan_cm)
    referensi = referensi[(referensi["Umur (Tahun)"] == tahun) & (referensi["Umur (bulan)"] == bulan)]
    if referensi.empty:
        return "Data referensi tidak ditemukan untuk umur ini."

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

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/data_balita', methods=['GET', 'POST'])
def data_balita():
    if request.method == 'POST':
        try:
            data = {
                'nama': request.form['nama'],
                'jenis_kelamin': request.form['jenis_kelamin'],
                'bulan': int(request.form['bulan']),
                'berat_badan': float(request.form['berat_badan']),
                'tinggi_badan': float(request.form['tinggi_badan'])
            }
            result = classify(data)
            return render_template('hasil.html', data=data, result=result, kategori="balita")
        except (ValueError, TypeError):
            return "Input tidak valid. Silakan periksa kembali data Anda."
    return render_template('data_balita.html')

@bp.route('/data_remaja', methods=['GET', 'POST'])
def data_remaja():
    if request.method == 'POST':
        try:
            data = {
                'nama': request.form['nama'],
                'jenis_kelamin': request.form['jenis_kelamin'],
                'tahun': int(request.form['tahun']),
                'bulan': int(request.form['bulan']),
                'berat_badan': float(request.form['berat_badan']),
                'tinggi_badan': float(request.form['tinggi_badan'])
            }
            result = classify_remaja(data)
            return render_template('hasil.html', data=data, result=result, kategori="remaja")
        except (ValueError, TypeError):
            return "Input tidak valid. Silakan periksa kembali data Anda."
    return render_template('data_remaja.html')

def classify(data):
    umur = data['bulan']
    berat_badan = data['berat_badan']
    tinggi_badan = data['tinggi_badan']
    jenis_kelamin = data['jenis_kelamin']
    return klasifikasi_imt_u(umur, berat_badan, tinggi_badan, jenis_kelamin)

def classify_remaja(data):
    tahun = data['tahun']
    bulan = data['bulan']
    berat_badan = data['berat_badan']
    tinggi_badan = data['tinggi_badan']
    jenis_kelamin = data['jenis_kelamin']
    return klasifikasi_imt_u_remaja(tahun, bulan, berat_badan, tinggi_badan, jenis_kelamin)

@bp.route('/hasil', methods=['POST'])
def hasil():
    data = request.form.to_dict()
    if 'bulan' in data and 'tahun' not in data:
        data['bulan'] = int(data['bulan'])
        data['berat_badan'] = float(data['berat_badan'])
        data['tinggi_badan'] = float(data['tinggi_badan'])
        result = classify(data)
        kategori = "balita"
    elif 'tahun' in data and 'bulan' in data:
        data['tahun'] = int(data['tahun'])
        data['bulan'] = int(data['bulan'])
        data['berat_badan'] = float(data['berat_badan'])
        data['tinggi_badan'] = float(data['tinggi_badan'])
        result = classify_remaja(data)
        kategori = "remaja"
    else:
        return "Data tidak lengkap. Pastikan semua field diisi."

    return render_template(
       'hasil.html', 
        name=data['nama'], 
        gender=data['jenis_kelamin'],
        age=data.get('bulan', None),
        year=data.get('tahun', None),
        month=data.get('bulan', None),
        weight=data['berat_badan'],
        height=data['tinggi_badan'],
        result=result,
        kategori=kategori
    )
