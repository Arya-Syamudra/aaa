import pandas as pd

# Membaca file referensi
file_laki = "./app/data/referensi_imt_laki_laki.csv"
file_perempuan = "./app/data/referensi_imt_perempuan.csv"

# Pastikan CSV memiliki header yang sesuai
df_referensi_laki = pd.read_csv(file_laki, delimiter=";")
df_referensi_perempuan = pd.read_csv(file_perempuan, delimiter=";")


print(df_referensi_laki.head())
print(df_referensi_perempuan.head())


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

    print(imt)

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

# Contoh penggunaan fungsi
status_imt_laki = klasifikasi_imt_u(umur=28, berat_badan=6.7, tinggi_badan_cm=71, jenis_kelamin="Laki-laki")
status_imt_perempuan = klasifikasi_imt_u(umur=24, berat_badan=13.0, tinggi_badan_cm=95, jenis_kelamin="Perempuan")

print("Status gizi IMT/U untuk laki-laki:", status_imt_laki)
print("Status gizi IMT/U untuk perempuan:", status_imt_perempuan)
