# ============================================================
# BAGIAN 2A: INHERITANCE — Sistem Pengguna MediRek
# ============================================================

# ── PARENT CLASS (Kategori Umum) ────────────────────────────
class PenggunaBase:
    """
    Parent class: menyimpan atribut umum yang dimiliki
    SEMUA jenis pengguna sistem MediRek.
    """
    def __init__(self, nama, email, telepon=None):
        self.nama      = nama
        self.email     = email
        self.telepon   = telepon
        self.is_active = True

    def tampilkan_info_dasar(self):
        """Method umum yang bisa dipakai semua child class."""
        status = '✅ Aktif' if self.is_active else '❌ Nonaktif'
        print(f"  Nama     : {self.nama}")
        print(f"  Email    : {self.email}")
        print(f"  Telepon  : {self.telepon or '-'}")
        print(f"  Status   : {status}")

    def toggle_aktif(self):
        """Mengaktifkan/menonaktifkan akun."""
        self.is_active = not self.is_active
        kondisi = 'DIAKTIFKAN' if self.is_active else 'DINONAKTIFKAN'
        print(f"  ⚙️  Akun {self.nama} berhasil {kondisi}.")


# ── CHILD CLASS 1: Admin ─────────────────────────────────────
class Admin(PenggunaBase):             # mewarisi PenggunaBase
    """
    Child class untuk pengguna dengan role Admin.
    Mewarisi semua atribut PenggunaBase, lalu menambahkan
    kemampuan mengelola seluruh pengguna sistem.
    """
    def __init__(self, nama, email, telepon=None):
        super().__init__(nama, email, telepon)   # panggil constructor parent
        self.daftar_user_dikelola = []           # atribut khusus admin

    def tambah_user(self, pengguna):
        """Admin dapat menambahkan pengguna baru ke sistem."""
        self.daftar_user_dikelola.append(pengguna)
        print(f"  ➕ [{self.nama}] menambahkan user: {pengguna.nama} ({pengguna.__class__.__name__})")

    def tampilkan_semua_user(self):
        """Menampilkan daftar semua user yang dikelola."""
        print(f"\n  📋 Daftar User Dikelola oleh {self.nama}:")
        for i, u in enumerate(self.daftar_user_dikelola, 1):
            status = '✅' if u.is_active else '❌'
            print(f"     {i}. {status} [{u.__class__.__name__:8s}] {u.nama} — {u.email}")

    def tampilkan_profil(self):
        print("┌─ PROFIL ADMIN ──────────────────────────────┐")
        self.tampilkan_info_dasar()               # pakai method parent
        print(f"  Role     : 🔑 Administrator")
        print(f"  Hak      : Kelola semua user & sistem")
        print("└─────────────────────────────────────────────┘")


# ── CHILD CLASS 2: Dokter ────────────────────────────────────
class Dokter(PenggunaBase):            # mewarisi PenggunaBase
    """
    Child class untuk pengguna dengan role Dokter.
    Mewarisi semua atribut PenggunaBase, lalu menambahkan
    atribut khusus profil dokter.
    """
    def __init__(self, nama, email, spesialisasi='Dokter Umum',
                 nomor_sip=None, telepon=None):
        super().__init__(nama, email, telepon)   # panggil constructor parent
        self.spesialisasi  = spesialisasi        # atribut khusus dokter
        self.nomor_sip     = nomor_sip           # Surat Izin Praktik
        self.pasien_hari_ini = 0

    def periksa_pasien(self, nama_pasien):
        self.pasien_hari_ini += 1
        print(f"  🩺 {self.nama} ({self.spesialisasi}) memeriksa: {nama_pasien}")
        print(f"     Pasien ke-{self.pasien_hari_ini} hari ini.")

    def tampilkan_profil(self):
        print("┌─ PROFIL DOKTER ─────────────────────────────┐")
        self.tampilkan_info_dasar()               # pakai method parent
        print(f"  Role         : 👨‍⚕️ Dokter")
        print(f"  Spesialisasi : {self.spesialisasi}")
        print(f"  No. SIP      : {self.nomor_sip or 'Belum diisi'}")
        print("└─────────────────────────────────────────────┘")


# ── CHILD CLASS 3: Perawat ───────────────────────────────────
class Perawat(PenggunaBase):           # mewarisi PenggunaBase
    """
    Child class untuk pengguna dengan role Perawat.
    Mewarisi semua atribut PenggunaBase, lalu menambahkan
    kemampuan melakukan pemeriksaan awal pasien.
    """
    def __init__(self, nama, email, telepon=None):
        super().__init__(nama, email, telepon)   # panggil constructor parent
        self.total_pemeriksaan_awal = 0          # atribut khusus perawat

    def input_tanda_vital(self, nama_pasien, tekanan_darah, suhu, nadi, saturasi):
        """Merekam tanda vital pasien sebelum diperiksa dokter."""
        self.total_pemeriksaan_awal += 1
        print(f"  🩹 {self.nama} merekam tanda vital: {nama_pasien}")
        print(f"     Tekanan Darah : {tekanan_darah} mmHg")
        print(f"     Suhu          : {suhu} °C")
        print(f"     Nadi          : {nadi} bpm")
        print(f"     Saturasi O₂   : {saturasi}%")

    def tampilkan_profil(self):
        print("┌─ PROFIL PERAWAT ────────────────────────────┐")
        self.tampilkan_info_dasar()               # pakai method parent
        print(f"  Role  : 👩‍⚕️ Perawat")
        print(f"  Tugas : Input pemeriksaan awal & tanda vital")
        print("└─────────────────────────────────────────────┘")


# ── PENGGUNAAN ───────────────────────────────────────────────
admin   = Admin  ('Administrator',    'admin@medirek.id')
dokter  = Dokter ('dr. Budi Santoso', 'dokter@medirek.id',
                  spesialisasi='Penyakit Dalam', nomor_sip='SIP-2024-001')
perawat = Perawat('Sari Perawat',     'perawat@medirek.id', '08112345678')

print("=" * 50)
print("   SISTEM PENGGUNA MEDIREK — INHERITANCE")
print("=" * 50)

print()
admin.tampilkan_profil()

print()
dokter.tampilkan_profil()

print()
perawat.tampilkan_profil()

print("\n" + "=" * 50)
print("   SIMULASI AKTIVITAS HARIAN")
print("=" * 50)

admin.tambah_user(dokter)
admin.tambah_user(perawat)
admin.tampilkan_semua_user()

print()
perawat.input_tanda_vital('Ahmad Pasien', '120/80', 36.5, 80, 98)

print()
dokter.periksa_pasien('Ahmad Pasien')
dokter.periksa_pasien('Siti Rahayu')
