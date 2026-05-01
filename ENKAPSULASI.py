# ============================================================
# BAGIAN 2C: ENKAPSULASI — Rekam Medis Pasien MediRek
# ============================================================

class RekamMedisSOAP:
    """
    Class RekamMedisSOAP menerapkan enkapsulasi:
    - Atribut PUBLIC   : nama_pasien, nomor_rm, tanggal_kunjungan
    - Atribut PROTECTED: _catatan_perawat, _keluhan_utama
    - Atribut PRIVATE  : __diagnosis, __resep_obat, __biaya_tindakan
    """

    # Kode akses internal — dalam sistem nyata ini disimpan di ENV/DB
    __KODE_DOKTER = "DOC-MEDIREK-2024"
    __KODE_ADMIN  = "ADMIN-RSUD-001"

    def __init__(self, nomor_rm, nama_pasien, tanggal_kunjungan):
        # ── PUBLIC — boleh diakses langsung ────────────────────
        self.nomor_rm           = nomor_rm
        self.nama_pasien        = nama_pasien
        self.tanggal_kunjungan  = tanggal_kunjungan

        # ── PROTECTED — sebaiknya hanya diakses internal klinik ─
        self._catatan_perawat   = ""
        self._keluhan_utama     = ""

        # ── PRIVATE — hanya bisa diakses dari dalam class ini ───
        self.__diagnosis        = None
        self.__kode_icd         = None
        self.__resep_obat       = []
        self.__tindakan         = ""
        self.__biaya_tindakan   = 0.0
        self.__is_rujukan       = False
        self.__catatan_rujukan  = ""

    # ── SETTER: mengisi data private (dengan validasi) ───────
    def set_pemeriksaan_perawat(self, keluhan, catatan_perawat):
        """Data dari perawat bersifat protected — akses internal klinik."""
        self._keluhan_utama   = keluhan
        self._catatan_perawat = catatan_perawat
        print(f"  ✅ Data perawat berhasil disimpan untuk {self.nama_pasien}")

    def set_diagnosis(self, diagnosis, kode_icd, tindakan, kode_dokter):
        """
        Data diagnosis & tindakan SANGAT RAHASIA.
        Hanya bisa diisi dokter dengan kode akses valid.
        """
        if kode_dokter == self.__KODE_DOKTER:
            self.__diagnosis = diagnosis
            self.__kode_icd  = kode_icd
            self.__tindakan  = tindakan
            print(f"  ✅ Diagnosis & tindakan berhasil disimpan.")
        else:
            print(f"  ❌ AKSES DITOLAK! Kode dokter tidak valid.")

    def tambah_resep(self, nama_obat, dosis, frekuensi, kode_dokter):
        """Resep obat hanya bisa diisi dokter ber-kode."""
        if kode_dokter == self.__KODE_DOKTER:
            self.__resep_obat.append({
                'obat'      : nama_obat,
                'dosis'     : dosis,
                'frekuensi' : frekuensi
            })
            print(f"  ✅ Resep '{nama_obat}' ditambahkan.")
        else:
            print(f"  ❌ AKSES DITOLAK! Kode dokter tidak valid.")

    def set_biaya(self, biaya, kode_admin):
        """Biaya tindakan adalah rahasia bisnis — hanya admin."""
        if kode_admin == self.__KODE_ADMIN:
            if biaya >= 0:
                self.__biaya_tindakan = biaya
                print(f"  ✅ Biaya tindakan berhasil diperbarui: Rp {biaya:,.0f}")
            else:
                print(f"  ❌ Biaya tidak boleh negatif!")
        else:
            print(f"  ❌ AKSES DITOLAK! Kode admin tidak valid.")

    def set_rujukan(self, catatan_rujukan, kode_dokter):
        """Mengatur status rujukan pasien — hanya dokter."""
        if kode_dokter == self.__KODE_DOKTER:
            self.__is_rujukan      = True
            self.__catatan_rujukan = catatan_rujukan
            print(f"  ✅ Pasien ditandai sebagai RUJUKAN.")
        else:
            print(f"  ❌ AKSES DITOLAK!")

    # ── GETTER: membaca data private ─────────────────────────
    def get_rekam_medis_lengkap(self, kode_dokter):
        """Rekam medis lengkap hanya bisa dibaca oleh dokter."""
        if kode_dokter != self.__KODE_DOKTER:
            print("  ❌ AKSES DITOLAK — Anda tidak memiliki izin membaca rekam medis.")
            return
        print(f"  No. RM             : {self.nomor_rm}")
        print(f"  Nama Pasien        : {self.nama_pasien}")
        print(f"  Tanggal Kunjungan  : {self.tanggal_kunjungan}")
        print(f"  Keluhan Utama      : {self._keluhan_utama or '-'}")
        print(f"  Catatan Perawat    : {self._catatan_perawat or '-'}")
        print(f"  Diagnosis          : {self.__diagnosis or 'Belum diisi'}")
        print(f"  Kode ICD           : {self.__kode_icd or '-'}")
        print(f"  Tindakan           : {self.__tindakan or '-'}")
        if self.__resep_obat:
            print(f"  Resep Obat         :")
            for r in self.__resep_obat:
                print(f"     • {r['obat']} — {r['dosis']} ({r['frekuensi']})")
        else:
            print(f"  Resep Obat         : Tidak ada")
        print(f"  Status Rujukan     : {'🔄 Dirujuk' if self.__is_rujukan else '✅ Tidak dirujuk'}")
        if self.__is_rujukan:
            print(f"  Catatan Rujukan    : {self.__catatan_rujukan}")

    def get_biaya(self, kode_admin):
        """Biaya tindakan hanya bisa dibaca oleh admin."""
        if kode_admin == self.__KODE_ADMIN:
            return f"Rp {self.__biaya_tindakan:,.0f}"
        return "❌ AKSES DITOLAK — Data biaya bersifat rahasia."

    def tampilkan_info_publik(self):
        """Hanya menampilkan data yang boleh diketahui publik."""
        print(f"  No. RM   : {self.nomor_rm}")
        print(f"  Pasien   : {self.nama_pasien}")
        print(f"  Tanggal  : {self.tanggal_kunjungan}")


# ── DEMONSTRASI ENKAPSULASI ──────────────────────────────────
rm = RekamMedisSOAP('RM-2024-001', 'Ahmad Pasien', '2024-05-20')

print("=" * 55)
print("   DEMO ENKAPSULASI — REKAM MEDIS MEDIREK")
print("=" * 55)

# 1. Data publik bisa diakses langsung
print("\n[1] Info Publik Rekam Medis:")
rm.tampilkan_info_publik()

# 2. Mencoba akses data private langsung → GAGAL
print("\n[2] Mencoba akses __diagnosis langsung dari luar class:")
try:
    print(rm.__diagnosis)
except AttributeError as e:
    print(f"  ❌ ERROR: {e}")
    print("  Data private tidak bisa diakses langsung dari luar class!")

# 3. Input data oleh perawat (protected)
print("\n[3] Perawat Merekam Keluhan & Catatan:")
rm.set_pemeriksaan_perawat(
    keluhan          = 'Sakit kepala, pusing, mual sejak 2 hari',
    catatan_perawat  = 'TD: 150/90, Suhu: 37.2°C, Nadi: 88bpm'
)

# 4. Dokter mengisi diagnosis (kode salah)
print("\n[4] Dokter Mengisi Diagnosis (kode salah):")
rm.set_diagnosis('Hipertensi Grade 2', 'I11', 'Konsultasi & edukasi', 'KODE-SALAH')

# 5. Dokter mengisi diagnosis (kode benar)
print("\n[5] Dokter Mengisi Diagnosis (kode benar):")
rm.set_diagnosis('Hipertensi Grade 2', 'I11', 'Konsultasi & edukasi', 'DOC-MEDIREK-2024')

# 6. Dokter menambah resep
print("\n[6] Dokter Menambah Resep Obat:")
rm.tambah_resep('Amlodipine 5mg',  '1 tablet', '1×1 pagi',  'DOC-MEDIREK-2024')
rm.tambah_resep('Captopril 25mg',  '1 tablet', '2×1',       'DOC-MEDIREK-2024')

# 7. Admin menetapkan biaya (kode salah)
print("\n[7] Admin Menetapkan Biaya (kode salah):")
rm.set_biaya(250_000, 'KODE-ADMIN-SALAH')

# 8. Admin menetapkan biaya (kode benar)
print("\n[8] Admin Menetapkan Biaya (kode benar):")
rm.set_biaya(250_000, 'ADMIN-RSUD-001')

# 9. Dokter membaca rekam medis lengkap
print("\n[9] Dokter Membaca Rekam Medis Lengkap:")
print("-" * 55)
rm.get_rekam_medis_lengkap('DOC-MEDIREK-2024')

# 10. Pasien/pihak lain mencoba membaca rekam medis
print("\n[10] Pihak Luar Mencoba Membaca Rekam Medis:")
rm.get_rekam_medis_lengkap('KODE-SEMBARANGAN')

# 11. Admin melihat biaya
print("\n[11] Admin Melihat Biaya Tindakan:")
print(f"  Biaya: {rm.get_biaya('ADMIN-RSUD-001')}")
