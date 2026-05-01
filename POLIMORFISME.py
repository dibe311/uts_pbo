# ============================================================
# BAGIAN 2B: POLIMORFISME — Sistem Antrian & Billing MediRek
# ============================================================

# ── BASE CLASS ──────────────────────────────────────────────
class AntrianBase:
    """
    Base class dengan method hitung_biaya() yang akan
    di-override (ditimpa) oleh masing-masing subclass.
    """
    STATUS_LIST = ('waiting', 'called', 'in_progress', 'done', 'cancelled')

    def __init__(self, nomor_antrian, nama_pasien, nama_dokter,
                 tanggal, tarif_dasar):
        self.nomor_antrian  = nomor_antrian
        self.nama_pasien    = nama_pasien
        self.nama_dokter    = nama_dokter
        self.tanggal        = tanggal
        self.tarif_dasar    = tarif_dasar
        self.status         = 'waiting'

    def hitung_biaya(self):
        """Method POLIMORFIK — akan di-override di tiap subclass."""
        raise NotImplementedError("Subclass harus mengimplementasikan hitung_biaya()")

    def update_status(self, status_baru):
        if status_baru in self.STATUS_LIST:
            self.status = status_baru
            print(f"  🔄 Antrian {self.nomor_antrian} status → [{status_baru.upper()}]")
        else:
            print(f"  ❌ Status tidak valid!")

    def tampilkan_tagihan(self):
        """Satu method untuk semua jenis antrian — polimorfisme!"""
        biaya = self.hitung_biaya()   # <-- satu pemanggilan, hasil beda-beda
        print(f"  No. Antrian : {self.nomor_antrian}")
        print(f"  Pasien      : {self.nama_pasien}")
        print(f"  Dokter      : {self.nama_dokter}")
        print(f"  Tanggal     : {self.tanggal}")
        print(f"  Tarif Dasar : Rp {self.tarif_dasar:>10,.0f}")
        print(f"  Total Bayar : Rp {biaya:>10,.0f}")


# ── SUBCLASS 1: Antrian Umum (bayar mandiri) ─────────────────
class AntrianUmum(AntrianBase):
    """Pasien umum — bayar penuh tanpa subsidi."""

    def hitung_biaya(self):              # OVERRIDE method parent
        return self.tarif_dasar          # bayar 100%

    def tampilkan_tagihan(self):
        print("┌─ TAGIHAN PASIEN UMUM ───────────────────────┐")
        super().tampilkan_tagihan()
        print(f"  Keterangan  : Pembayaran mandiri penuh")
        print("└─────────────────────────────────────────────┘")


# ── SUBCLASS 2: Antrian BPJS ─────────────────────────────────
class AntrianBPJS(AntrianBase):
    """Pasien peserta BPJS — ditanggung penuh, biaya pasien = 0."""

    def __init__(self, nomor_antrian, nama_pasien, nama_dokter,
                 tanggal, tarif_dasar, nomor_bpjs):
        super().__init__(nomor_antrian, nama_pasien, nama_dokter,
                         tanggal, tarif_dasar)
        self.nomor_bpjs = nomor_bpjs     # atribut tambahan BPJS

    def hitung_biaya(self):              # OVERRIDE method parent
        return 0                         # gratis, ditanggung BPJS

    def tampilkan_tagihan(self):
        print("┌─ TAGIHAN PASIEN BPJS ───────────────────────┐")
        super().tampilkan_tagihan()
        print(f"  No. BPJS    : {self.nomor_bpjs}")
        print(f"  Keterangan  : ✅ Ditanggung BPJS Kesehatan")
        print("└─────────────────────────────────────────────┘")


# ── SUBCLASS 3: Antrian Rujukan Spesialis ────────────────────
class AntrianRujukan(AntrianBase):
    """Pasien rujukan ke spesialis — tarif spesialis + biaya administrasi rujukan."""
    BIAYA_ADMINISTRASI_RUJUKAN = 25_000
    MULTIPLIER_SPESIALIS       = 1.5    # tarif spesialis 50% lebih mahal

    def __init__(self, nomor_antrian, nama_pasien, nama_dokter,
                 tanggal, tarif_dasar, asal_faskes, catatan_rujukan=''):
        super().__init__(nomor_antrian, nama_pasien, nama_dokter,
                         tanggal, tarif_dasar)
        self.asal_faskes      = asal_faskes      # misal: Puskesmas Caruban
        self.catatan_rujukan  = catatan_rujukan

    def hitung_biaya(self):              # OVERRIDE method parent
        tarif_spesialis = self.tarif_dasar * self.MULTIPLIER_SPESIALIS
        return tarif_spesialis + self.BIAYA_ADMINISTRASI_RUJUKAN

    def tampilkan_tagihan(self):
        print("┌─ TAGIHAN PASIEN RUJUKAN ────────────────────┐")
        super().tampilkan_tagihan()
        print(f"  Asal Faskes : {self.asal_faskes}")
        print(f"  Adm Rujukan : Rp {self.BIAYA_ADMINISTRASI_RUJUKAN:>10,.0f}")
        print(f"  Keterangan  : ⭐ Tarif spesialis + adm rujukan")
        if self.catatan_rujukan:
            print(f"  Catatan     : {self.catatan_rujukan}")
        print("└─────────────────────────────────────────────┘")


# ── DEMONSTRASI POLIMORFISME ─────────────────────────────────
# Buat daftar antrian dengan tipe BERBEDA
daftar_antrian = [
    AntrianUmum(
        nomor_antrian = 'U-001',
        nama_pasien   = 'Siti Rahayu',
        nama_dokter   = 'dr. Budi Santoso',
        tanggal       = '2024-05-20',
        tarif_dasar   = 150_000
    ),
    AntrianBPJS(
        nomor_antrian = 'B-002',
        nama_pasien   = 'Ahmad Pasien',
        nama_dokter   = 'dr. Budi Santoso',
        tanggal       = '2024-05-20',
        tarif_dasar   = 150_000,
        nomor_bpjs    = '0001234567890'
    ),
    AntrianRujukan(
        nomor_antrian   = 'R-003',
        nama_pasien     = 'Raden Wijaya',
        nama_dokter     = 'dr. Kartika, Sp.PD',
        tanggal         = '2024-05-20',
        tarif_dasar     = 300_000,
        asal_faskes     = 'Puskesmas Caruban',
        catatan_rujukan = 'Hipertensi tidak terkontrol'
    ),
]

# SATU LOOP, SATU METHOD — tapi hasilnya berbeda untuk tiap objek!
print("=" * 50)
print("     SISTEM BILLING ANTRIAN — MEDIREK")
print("=" * 50)
for i, antrian in enumerate(daftar_antrian, 1):
    print(f"\n[ Antrian #{i} — {type(antrian).__name__} ]")
    antrian.tampilkan_tagihan()          # ← POLIMORFISME di sini!
    antrian.update_status('called')

print("\n" + "=" * 50)
print("   REKAP TOTAL PENDAPATAN HARI INI")
print("=" * 50)
total = sum(a.hitung_biaya() for a in daftar_antrian)
print(f"  Total Pendapatan Klinik : Rp {total:,.0f}")
print(f"  Total Pasien Terlayani  : {len(daftar_antrian)} orang")
