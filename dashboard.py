import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Dashboard Prediksi Akademik Mahasiswa PTI",
    layout="centered"
)

st.title("Dashboard Prediksi Performa Akademik Mahasiswa")
st.write("Seluruh data wajib diisi untuk memperoleh hasil prediksi dan analisis.")


# ======================
# KONVERSI NILAI & MAPPING MK
# ======================
nilai_map = {
    "A": 4.00,
    "B+": 3.50,
    "B": 3.00,
    "C+": 2.50,
    "C": 2.00,
    "D+": 1.50,
    "D": 1.00,
    "E": 0.00
}

tema_mk = {
    # A – Computing Education Thinking Paradigm Course
    "CIE61402": "A",
    "CIE61403": "A",

    # B – Information Technology Management Course
    "CIE61404": "B",
    "CSD60701": "B",
    "CSD60005": "B",
    "CSD60011": "B",

    # C –
    "CIE61113": "C",
    "CIE60027": "C",
    "CIE61114": "C",
    "CIE61115": "C",
    "CIE60026": "C",
    "CIE62305": "C",
    "CIE62306": "C",
    "CIE60031": "C",
    "CIE60064": "C",
    "CIE60065": "C",

    # D – Data-based Decision Making Course
    "CSD60702": "D",
    "CIE61212": "D",
    "CIE60058": "D",
    "CSD60015": "D",
    "CSD60013": "D",
    "CIE60044": "D",
    "CIE60046": "D",
    "CIE60045": "D",

    # E – Interrelated Information Technology Course
    "CIE62116": "E",
    "CIE62117": "E",
    "CSD60002": "E",

    # F – Immersive Instructional Systems Course
    "CIE62118": "F",
    "CIE62307": "F",
    "CIE62308": "F",
    "CIE60028": "F",
    "CIE60052": "F",
    "CIE60056": "F",
    "CIE60053": "F",
    "CIE60054": "F",
    "CIE60055": "F",

    # G – Research Data Analysis Course
    "CSD60716": "G",
    "CSD60715": "G",
    "CIE60029": "G",
    "CIE60030": "G",
    "CIE60061": "G",
    "CIE60060": "G",
    "CIE60062": "G",

    # H – Advanced Information Technology Course
    "CIE61215": "H",
    "CSD60713": "H",
    "CSD60711": "H",
    "CSD60714": "H",
    "CIE60037": "H",
    "CIE60048": "H",
    "CSD60003": "H",
    "CSD60009": "H",
    "CSD60010": "H",
    "CSD60014": "H",
    "CIE60049": "H",
    "CIE60035": "H",
    "CIE60051": "H",

    # I – Public Communication Skill Course
    "CIE61119": "I",
    "CIE60057": "I",
    "CIE61120": "I"
}

def kategori_mk(kode):
    kode = str(kode).strip().upper()

    # MK Pilihan Prodi A sampai I
    if kode in tema_mk:
        return "MK_PILIHAN_PRODI"

    # MK Pilihan Universitas harus lebih dulu
    elif kode in ["UBU60029", "UBU60030"]:
        return "MK_PILIHAN_UNIVERSITAS"

    # MK Wajib
    elif kode.startswith("MPK"):
        return "MK_WAJIB_UMUM"
    elif kode.startswith("UBU"):
        return "MK_WAJIB_UNIVERSITAS"
    elif kode.startswith("COM"):
        return "MK_WAJIB_FAKULTAS"
    elif kode.startswith(("CIE", "CSD")):
        return "MK_WAJIB_PRODI"

    else:
        return "LAINNYA"



# ======================
# KETERANGAN BIDANG A–I
# ======================
keterangan_bidang = {
    "A": "Computing Education Thinking Paradigm Course",
    "B": "Information Technology Management Course",
    "C": "Non Formal Education Course",
    "D": "Data based Decision Making Course",
    "E": "Interrelated Information Technology Course",
    "F": "Immersive Instructional Systems Course",
    "G": "Research Data Analysis Course",
    "H": "Advanced Information Technology Course",
    "I": "Public Communication Skill Course"
    }

tab_prediksi, tab_info = st.tabs(
    ["Prediksi", "Informasi Lengkap"]
)

with tab_prediksi:
 
    # ======================
    # LOAD MODEL
    # ======================
    model = joblib.load("Performa.pkl")
    encoders = joblib.load("Encoder.pkl")
    fitur_model = joblib.load("Fitur_model.pkl")

    # ======================
    # INPUT DATA UMUM
    # ======================
    st.subheader("A. Data Umum Mahasiswa")

    jenis_kelamin = st.selectbox("Jenis Kelamin", ["--Pilih--"] + list(encoders["JENIS_KELAMIN"].classes_))
    seleksi = st.selectbox("Jalur Seleksi", ["--Pilih--"] + list(encoders["SELEKSI"].classes_))
    kerja_ayah = st.selectbox("Pekerjaan Ayah",["--Pilih--"] + list(encoders["KERJA_AYAH"].classes_))
    kerja_ibu = st.selectbox("Pekerjaan Ibu", ["--Pilih--"] + list(encoders["KERJA_IBU"].classes_))
    didik_ayah = st.selectbox("Pendidikan Ayah", ["--Pilih--"] + list(encoders["DIDIK_AYAH"].classes_))
    didik_ibu = st.selectbox("Pendidikan Ibu", ["--Pilih--"] + list(encoders["DIDIK_IBU"].classes_))



    riwayat_prestasi = st.selectbox("Riwayat Prestasi", ["Tidak Ada", "Ada"])
    riwayat_beasiswa = st.selectbox("Riwayat Beasiswa", ["Tidak Ada", "Ada"])



    colA, colB, colC = st.columns(3)

    with colA:
        ips1 = st.number_input("IPS Semester 1", 0.0, 4.0, step=0.01)
        ips2 = st.number_input("IPS Semester 2", 0.0, 4.0, step=0.01)

    with colB:
        ips3 = st.number_input("IPS Semester 3", 0.0, 4.0, step=0.01)
        ips4 = st.number_input("IPS Semester 4", 0.0, 4.0, step=0.01)

    with colC:
        ips5 = st.number_input("IPS Semester 5", 0.0, 4.0, step=0.01)




    # ======================
    # INPUT KHS (OPS I B)
    # ======================
    st.subheader("B. Input KHS Mahasiswa")

    df_khs = st.data_editor(
        pd.DataFrame({"KODE_MK": ["" for _ in range(10)],
                    "NILAI": ["" for _ in range(10)]}),
        num_rows="dynamic",
        use_container_width=True
    )

    # ======================
    # PROSES
    # ======================
    if st.button("Prediksi dan Analisis"):
    # Validasi selectbox
        if jenis_kelamin == "--Pilih--" or seleksi == "--Pilih--" or kerja_ayah == "--Pilih--" or kerja_ibu == "--Pilih--" or didik_ayah == "--Pilih--" or didik_ibu == "--Pilih--":
            st.warning("Harap isi semua data terlebih dahulu.")
            st.stop()

    # Validasi
        # ======================
        # BERSIHKAN DATA KHS
        # ======================
        df_khs = df_khs.dropna()
        df_khs["KODE_MK"] = df_khs["KODE_MK"].astype(str).str.upper().str.strip()
        df_khs["NILAI"] = df_khs["NILAI"].astype(str).str.upper().str.strip()
        df_khs = df_khs[df_khs["KODE_MK"] != ""]

        if df_khs.empty:
            st.warning("Data KHS belum diisi")
            st.stop()

        # ======================
        # KONVERSI NILAI & MAPPING
        # ======================
        df_khs["NILAI_ANGKA"] = df_khs["NILAI"].map(nilai_map)
        df_khs["BIDANG"] = df_khs["KODE_MK"].map(tema_mk)
        df_khs["KATEGORI_MK"] = df_khs["KODE_MK"].apply(kategori_mk)

        # ======================
        # DATA VALID (NILAI ADA)
        # ======================
        df_valid = df_khs.dropna(subset=["NILAI_ANGKA"])

        if df_valid.empty:
            st.warning("Tidak ada nilai MK yang valid")
            st.stop()
        
        # ======================
        # HITUNG RATA RATA NILAI
        # ======================

        rata_mk = (
        df_valid
        .groupby("KATEGORI_MK")["NILAI_ANGKA"]
        .mean()
)
        jumlah_mk = len(df_valid)

        # ======================
        # HITUNG RATA-RATA BIDANG A–I
        # ======================

        df_bidang = df_valid.dropna(subset=["BIDANG"])

        rata_bidang = (
            df_bidang
            .groupby("BIDANG")["NILAI_ANGKA"]
            .mean()
        )

        # pastikan semua bidang A–I ada
        for b in list("ABCDEFGHI"):
            if b not in rata_bidang:
                rata_bidang[b] = 0.0

        rata_bidang = rata_bidang.sort_index()

        # ======================
        # AMBIL BIDANG UNGGUL (SEMUA DENGAN NILAI MAKS)
        # ======================
        max_bidang = rata_bidang.max()
        bidang_unggul = rata_bidang[rata_bidang == max_bidang].index.tolist()

        # ======================
        # HITUNG RATA-RATA KATEGORI MK
        # ======================
        rata_kategori = (
            df_valid
            .groupby("KATEGORI_MK")["NILAI_ANGKA"]
            .mean()
        )

        max_kategori = rata_kategori.max()
        kategori_unggul = rata_kategori[rata_kategori == max_kategori].index.tolist()





        kategori_wajib = {
            "MK_WAJIB_PRODI": 0.0,
            "MK_WAJIB_FAKULTAS": 0.0,
            "MK_WAJIB_UMUM": 0.0,
            "MK_WAJIB_UNIVERSITAS": 0.0,
            "MK_PILIHAN_PRODI": 0.0
        }

        for k in kategori_wajib:
            if k not in rata_mk:
                rata_mk[k] = 0.0



        # Hitung tren IPS otomatis
        ips_list = [ips1, ips2, ips3, ips4, ips5]
        tren_ips = ips5 - ips1

        # ======================
        # DATA UNTUK MODEL ML
        # ======================
        data_ml = {
        "JENIS_KELAMIN": jenis_kelamin,
        "SELEKSI": seleksi,
        "KERJA_AYAH": kerja_ayah,
        "KERJA_IBU": kerja_ibu,
        "DIDIK_AYAH": didik_ayah,
        "DIDIK_IBU": didik_ibu,
        "IPS_SEM1": ips1,
        "IPS_SEM2": ips2,
        "IPS_SEM3": ips3,
        "IPS_SEM4": ips4,
        "IPS_SEM5": ips5,
        "TREN_IPS": tren_ips,
        "RIWAYAT_PRESTASI": 1 if riwayat_prestasi == "Ada" else 0,
        "RIWAYAT_BEASISWA": 1 if riwayat_beasiswa == "Ada" else 0,
        "RATA2_MK_WAJIB_PRODI": rata_mk["MK_WAJIB_PRODI"],
        "RATA2_MK_WAJIB_FAKULTAS": rata_mk["MK_WAJIB_FAKULTAS"],
        "RATA2_MK_WAJIB_UMUM": rata_mk["MK_WAJIB_UMUM"],
        "RATA2_MK_WAJIB_UNIVERSITAS": rata_mk["MK_WAJIB_UNIVERSITAS"],
        "RATA2_MK_PILIHAN_PRODI": rata_mk["MK_PILIHAN_PRODI"]
            
        }

        df_input = pd.DataFrame([data_ml])

        for col in encoders:
            df_input[col] = encoders[col].transform(df_input[col].astype(str))

        df_input = df_input[fitur_model]

        prediksi = model.predict(df_input)[0]
        probabilitas = model.predict_proba(df_input).max()

        # ======================
        # OUTPUT RINGKASAN
        # ======================
        st.subheader("Ringkasan Perhitungan Akademik")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Jumlah Mata Kuliah", jumlah_mk)
        col2.metric("Tren IPS", f"{tren_ips:.2f}", 
                    delta="Meningkat" if tren_ips > 0 else ("Menurun" if tren_ips < 0 else "Stabil"))

        # Tambahkan line chart IPS semester
        st.line_chart(pd.DataFrame({
            "Semester": ["IPS1", "IPS2", "IPS3", "IPS4", "IPS5"],
            "Nilai IPS": [ips1, ips2, ips3, ips4, ips5]
        }).set_index("Semester"))


        # ======================
        # OUTPUT PREDIKSI
        # ======================
        st.subheader("Hasil Prediksi Performa Akademik")
        
        # Mapping label dengan deskripsi
        if prediksi == 0:
            label_prediksi = "IPK < 3.5 (performa akademik lebih rendah)"
        else:
            label_prediksi = "IPK ≥ 3.5 (performa akademik lebih tinggi)"
        
        st.success(f"Kategori Performa Akademik: {label_prediksi}")
        
        st.write(
            f"Tingkat Keyakinan Model terhadap hasil prediksi sebesar "
            f"{probabilitas:.2f}"
        )


        # ======================
        # ANALISIS BIDANG
        # ======================
        st.subheader("Analisis Bidang Keahlian (A–I)")
        st.bar_chart(rata_bidang)

        if len(bidang_unggul) == 1:
            b = bidang_unggul[0]
            st.write(
                f"Mahasiswa cenderung unggul pada **Bidang {b}** "
                f"({keterangan_bidang[b]})."
            )
        else:
            daftar_bidang = [
                f"Bidang {b} ({keterangan_bidang[b]})"
                for b in bidang_unggul
            ]
            st.write(
                "Mahasiswa menunjukkan kecenderungan unggul pada beberapa bidang, yaitu: "
                + ", ".join(daftar_bidang) + "."
            )

        # ======================
        # ANALISIS KATEGORI MK
        # ======================
        st.subheader("Analisis Kategori Mata Kuliah")
        # Buang kategori 'LAINNYA' dari data 
        rata_kategori_filtered = rata_kategori.drop(index='LAINNYA', errors='ignore')
        st.bar_chart(rata_kategori_filtered)
        # Buang 'LAINNYA' dari daftar kategori unggul 
        kategori_unggul_filtered = [k for k in kategori_unggul if k != 'LAINNYA']

        if len(kategori_unggul_filtered) == 1:
            st.write(
                f"Mahasiswa cenderung unggul pada kategori mata kuliah **{kategori_unggul_filtered[0]}**."
            )
        elif len(kategori_unggul_filtered) > 1:
            st.write(
                "Mahasiswa menunjukkan kecenderungan unggul pada beberapa kategori mata kuliah, yaitu: " + ", ".join(kategori_unggul_filtered) + "."
            )
        else:
            st.write("Tidak ada kategori unggul yang ditampilkan.")


        # ======================
        # DEBUG (OPSIONAL)
        # ======================
        with st.expander("DEBUG DATA"):
            st.write("Data KHS Lengkap")
            st.dataframe(df_khs)
            st.write("Data Valid")
            st.dataframe(df_valid)


with tab_info:
    st.subheader("Informasi Perhitungan")

    st.markdown("""
    Tab ini berisi penjelasan mengenai variabel yang digunakan dalam model prediksi:
    
    - **Jenis Kelamin & Seleksi**: faktor demografi dan jalur masuk mahasiswa.
    - **Kerja Ayah/Ibu & Pendidikan Ayah/Ibu**: latar belakang keluarga yang dapat memengaruhi dukungan akademik.
    - **Riwayat Prestasi & Beasiswa**: indikator non-akademik yang menunjukkan pencapaian dan dukungan finansial.
    - **IPS Semester 1–5 & Tren IPS**: menggambarkan perkembangan nilai mahasiswa dari waktu ke waktu.
    - **Rata-rata MK Wajib (Prodi, Fakultas, Universitas, Umum) & MK Pilihan Prodi**: menunjukkan konsistensi capaian akademik berdasarkan kelompok mata kuliah.
    - **IPK Semester 6**: indikator utama performa akademik mahasiswa secara keseluruhan.
    
    Informasi ini membantu pengguna dashboard memahami konteks variabel yang digunakan dalam proses klasifikasi performa akademik.
    """)


    st.subheader("Informasi Bidang Keahlian")
    for k, v in keterangan_bidang.items():
        st.write(f"Bidang {k}: {v}")

    st.subheader("Daftar Mata Kuliah Berdasarkan Kategori")

    data_mk = [
        # MK Wajib Umum
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Agama Islam", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Agama Katolik", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Agama Protestan", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Agama Hindu", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Agama Buddha", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Kewarganegaraan", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Bahasa Indonesia", "SKS": 2},
        {"Kategori": "MK Wajib Umum", "Mata Kuliah": "Pancasila", "SKS": 2},

        # MK Wajib Universitas
        {"Kategori": "MK Wajib Universitas", "Mata Kuliah": "Tugas Akhir Skripsi", "SKS": 6},
        {"Kategori": "MK Wajib Universitas", "Mata Kuliah": "Praktik Kerja Lapangan", "SKS": 4},
        {"Kategori": "MK Wajib Universitas", "Mata Kuliah": "Kewirausahaan", "SKS": 2},
        {"Kategori": "MK Wajib Universitas", "Mata Kuliah": "Bahasa Inggris", "SKS": 2},
        {"Kategori": "MK Wajib Universitas", "Mata Kuliah": "Pengabdian Kepada Masyarakat", "SKS": 4},

        # MK Wajib Fakultas
        {"Kategori": "MK Wajib Fakultas", "Mata Kuliah": "Pemrograman Dasar", "SKS": 5},
        {"Kategori": "MK Wajib Fakultas", "Mata Kuliah": "Matematika Diskrit", "SKS": 2},
        {"Kategori": "MK Wajib Fakultas", "Mata Kuliah": "Pengantar Keilmuan Komputer", "SKS": 2},
        {"Kategori": "MK Wajib Fakultas", "Mata Kuliah": "Metode Penelitian dan Penulisan Ilmiah", "SKS": 3},
        {"Kategori": "MK Wajib Fakultas", "Mata Kuliah": "Etika Profesi", "SKS": 2},
        {"Kategori": "MK Wajib Fakultas", "Mata Kuliah": "Capstone Project", "SKS": 3},

        # MK Wajib Program Studi
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Perkembangan Peserta Didik", "SKS": 3},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Filsafat Pendidikan dan Sains", "SKS": 4},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Komunikasi dan Teknologi Pendidikan", "SKS": 3},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Pengembangan Kurikulum", "SKS": 3},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Pembelajaran Berdiferensiasi", "SKS": 2},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Teori dan Sains Belajar", "SKS": 3},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Lingkungan Pembelajaran Digital", "SKS": 3},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Penilaian Hasil Belajar", "SKS": 3},
        {"Kategori": "MK Wajib Program Studi", "Mata Kuliah": "Pembelajaran Mikro", "SKS": 3},

        
       
    ]

    df_kurikulum = pd.DataFrame(data_mk)
    st.subheader("Daftar Mata Kuliah Wajib")
    st.dataframe(df_kurikulum, use_container_width=True)


   
    data_mk2 = [
     # MK Pilihan Universitas
        {"Kategori": "MK Pilihan Universitas", "Mata Kuliah": "Perspektif Global", "SKS": 3},
        {"Kategori": "MK Pilihan Universitas", "Mata Kuliah": "Pengantar Artificial Intelligence", "SKS": 4},
    ]
    df_kurikulum = pd.DataFrame(data_mk2)
    st.subheader("Daftar Mata Kuliah Pilihan Universitas")
    st.dataframe(df_kurikulum, use_container_width=True)


    mk_pilihan_prodi = [
        # TEMA A
        {"Tema": "A", "Mata Kuliah": "Paradigma Berpikir Komputasi", "SKS": 3},
        {"Tema": "A", "Mata Kuliah": "Paradigma Berpikir Sistem Desain", "SKS": 3},

        # TEMA B
        {"Tema": "B", "Mata Kuliah": "Manajemen Proyek Teknologi Informasi", "SKS": 3},
        {"Tema": "B", "Mata Kuliah": "Manajemen Layanan Teknologi Informasi", "SKS": 3},

        # TEMA C
        {"Tema": "C", "Mata Kuliah": "Pengembangan Program Pelatihan Teknologi Informasi", "SKS": 3},
        {"Tema": "C", "Mata Kuliah": "Pendidikan Orang Dewasa dan Berkelanjutan", "SKS": 3},
        {"Tema": "C", "Mata Kuliah": "Manajemen Sistem Pendidikan", "SKS": 3},
        {"Tema": "C", "Mata Kuliah": "Pembelajaran Sosial Emosional", "SKS": 3},
        {"Tema": "C", "Mata Kuliah": "Pembelajaran Inklusif", "SKS": 3},

        # TEMA D
        {"Tema": "D", "Mata Kuliah": "Sistem Pendukung Keputusan", "SKS": 3},
        {"Tema": "D", "Mata Kuliah": "Sistem Belajar Mesin", "SKS": 3},

        # TEMA E
        {"Tema": "E", "Mata Kuliah": "Teknologi Komputasi Awan", "SKS": 3},
        {"Tema": "E", "Mata Kuliah": "Teknologi Peranti Internet", "SKS": 3},

        # TEMA F
        {"Tema": "F", "Mata Kuliah": "Sistem Pembelajaran Bergamifikasi dan Terpersonalisasi", "SKS": 3},
        {"Tema": "F", "Mata Kuliah": "Sistem Pembelajaran Berbasis Multimedia, Gim, dan Peranti Bergerak", "SKS": 3},
        {"Tema": "F", "Mata Kuliah": "Sistem Pembelajaran Jarak Jauh", "SKS": 3},

        # TEMA G
        {"Tema": "G", "Mata Kuliah": "Analisis Data Penelitian Kualitatif", "SKS": 3},
        {"Tema": "G", "Mata Kuliah": "Analisis Data Penelitian Kuantitatif", "SKS": 3},

        # TEMA H
        {"Tema": "H", "Mata Kuliah": "Pengembangan Aplikasi Peranti Bergerak", "SKS": 3},
        {"Tema": "H", "Mata Kuliah": "Jaringan Terapan", "SKS": 3},
        {"Tema": "H", "Mata Kuliah": "Perancangan Pengalaman Pengguna", "SKS": 3},
        {"Tema": "H", "Mata Kuliah": "Jaminan Kualitas Perangkat Lunak", "SKS": 3},

        # TEMA I
        {"Tema": "I", "Mata Kuliah": "Multimodal Storytelling", "SKS": 3},
        {"Tema": "I", "Mata Kuliah": "Literasi Digital", "SKS": 3}
    ]

    df_mk_pilihan = pd.DataFrame(mk_pilihan_prodi)

    st.subheader("Daftar Mata Kuliah Pilihan Program Studi")
    st.dataframe(df_mk_pilihan, use_container_width=True)






