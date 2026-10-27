import re
from abc import ABC, abstractmethod

def rp(angka):
    return "Rp" + f"{angka:,}".replace(",", ".")

def baris(kiri, kanan, indent=2, lebar=41):
    # teks kiri, harga rata kanan, total lebar selalu sama dengan garis struk
    sisa = lebar - indent - len(kanan) - 1
    return " " * indent + kiri[:sisa].ljust(sisa) + " " + kanan

def baca_int(prompt, minimal=1):
    while True:
        teks = input(prompt).strip()
        if "-" in teks:
            print("Gak boleh pakai tanda minus (-), isi 0 kalau gak ada.")
            continue
        if not teks.isdigit():
            print("Masukkan angka yang valid.")
            continue
        nilai = int(teks)
        if nilai < minimal:
            print(f"  Minimal {minimal}.")
            continue
        return nilai

def punya_huruf(teks):
    return any(c.isalpha() for c in teks)

def baca_nama():
    while True:
        nama = input("  Nama pelanggan: ").strip()
        if nama == "":
            return "Pelanggan"
        if punya_huruf(nama):
            return nama
        print("Nama harus huruf.")

def baca_no_hp():
    while True:
        no_hp = input("  No HP (isi 0 atau kosongkan jika gak ada): ").strip()
        if no_hp in ("", "0"):
            return "-"
        # angka saja, boleh diawali + dan boleh ada tanda - atau spasi di tengah
        if re.fullmatch(r"\+?\d[\d\- ]{6,14}\d", no_hp):
            return no_hp
        print("  No HP gak valid. Contoh: 0812-3456-7890")

class Menu(ABC):
    """Kelas abstrak untuk semua menu minuman di coffee shop."""
    jenis = "Menu"

    def __init__(self, nama, harga_dasar):
        self._nama = nama                  # protected
        self.__harga_dasar = harga_dasar   # private

    @property
    def nama(self):
        return self._nama

    @property
    def harga_dasar(self):
        return self.__harga_dasar

    @abstractmethod
    def rincian_tambahan(self):
        """Daftar (keterangan, biaya) tambahan di luar harga dasar.
        Tiap jenis menu beda cara hitungnya."""

    @abstractmethod
    def keterangan(self):
        """Keterangan singkat menu."""

    def hitung_harga(self):
        return self.harga_dasar + sum(biaya for _, biaya in self.rincian_tambahan())

    def tampilkan_info(self):
        print(f"[{self.jenis:<8}] {self._nama:<20} {rp(self.hitung_harga()):>10}  | {self.keterangan()}")

    def __str__(self):
        return f"{self._nama} ({rp(self.hitung_harga())})"

class Kopi(Menu):
    jenis = "Kopi"

    def __init__(self, nama, harga_dasar, shot=1):
        super().__init__(nama, harga_dasar)
        self.shot = shot 

    @classmethod
    def dari_input(cls, nama, harga):
        shot = baca_int("  Jumlah shot espresso: ")
        return cls(nama, harga, shot)

    def rincian_tambahan(self):
        # tiap tambahan shot +5000
        tambahan = self.shot - 1
        if tambahan == 0:
            return []
        return [(f"{tambahan} shot tambahan", tambahan * 5000)]

    def keterangan(self):
        return f"{self.shot} shot espresso"

class NonKopi(Menu):
    jenis = "Non-Kopi"

    def __init__(self, nama, harga_dasar, topping=None):
        super().__init__(nama, harga_dasar)
        self.topping = topping if topping else []  

    @classmethod
    def dari_input(cls, nama, harga):
        while True:
            teks = input("  Topping (pisah koma, kosongkan atau isi 0 jika gak ada): ").strip()
            if teks in ("", "0"):
                return cls(nama, harga, [])
            topping = [t.strip() for t in teks.split(",") if t.strip()]
            if all(punya_huruf(t) for t in topping):
                return cls(nama, harga, topping)
            print("Nama topping harus berupa huruf, bukan angka/simbol saja.")

    def rincian_tambahan(self):
        # tiap topping +3000
        return [(f"topping {t}", 3000) for t in self.topping]

    def keterangan(self):
        if not self.topping:
            return "tanpa topping"
        return "topping: " + ", ".join(self.topping)

class Blended(Menu):
    jenis = "Blended"

    def __init__(self, nama, harga_dasar, ukuran_ml=350):
        super().__init__(nama, harga_dasar)
        self.ukuran_ml = ukuran_ml  

    @classmethod
    def dari_input(cls, nama, harga):
        ukuran = baca_int("Ukuran (ml, minimal 350): ", 350)
        return cls(nama, harga, ukuran)

    def rincian_tambahan(self):
        # ukuran standar 350 ml, tiap +100 ml nambah 4000
        biaya = (self.ukuran_ml - 350) // 100 * 4000
        if biaya == 0:
            return []
        return [(f"ukuran {self.ukuran_ml} ml", biaya)]

    def keterangan(self):
        return f"{self.ukuran_ml} ml"

JENIS_MENU = {"1": Kopi, "2": NonKopi, "3": Blended}

class DaftarMenu:
    """Kumpulan menu. Objek Menu dibuat di luar lalu dimasukkan ke sini,
    jadi kalau DaftarMenu atau salah satu menu dihapus dari sini,
    objek Menu-nya tidak ikut hilang (agregasi)."""

    def __init__(self):
        self._daftar = []

    def tambah(self, menu):
        if any(m.nama.lower() == menu.nama.lower() for m in self._daftar):
            return False
        self._daftar.append(menu)
        return True

    def hapus(self, nomor):
        return self._daftar.pop(nomor - 1)

    def tampilkan(self):
        if not self._daftar:
            print("(menu masih kosong)")
        for i, m in enumerate(self._daftar, start=1):
            print(f"{i:>2}. ", end="")
            m.tampilkan_info()

    def __len__(self):
        return len(self._daftar)

    def __getitem__(self, indeks):
        return self._daftar[indeks]

    def __iter__(self):
        return iter(self._daftar)

class Pelanggan:
    def __init__(self, nama, no_hp):
        self.nama = nama
        self.no_hp = no_hp

    def __eq__(self, lain):
        return self.no_hp == lain.no_hp

    def __str__(self):
        return f"{self.nama} ({self.no_hp})"

class ItemPesanan:
    """Satu baris pesanan. Dibuat oleh Transaksi, tidak berdiri sendiri."""

    def __init__(self, menu, jumlah):
        self.menu = menu      
        self.nama_menu = menu.nama
        self.harga_dasar = menu.harga_dasar
        self.tambahan = menu.rincian_tambahan()
        self.harga_satuan = menu.hitung_harga()
        self.jumlah = jumlah

    def subtotal(self):
        return self.harga_satuan * self.jumlah

    def cetak(self):
        print(baris(self.nama_menu, ""))
        print(baris("Harga dasar", rp(self.harga_dasar), indent=4))
        for ket, biaya in self.tambahan:
            print(baris("+ " + ket, rp(biaya), indent=4))
        print(baris(f"{rp(self.harga_satuan)} x {self.jumlah}", rp(self.subtotal()), indent=4))

class Transaksi:
    _jumlah_transaksi = 0

    def __init__(self, pelanggan):
        Transaksi._jumlah_transaksi += 1
        self.id = f"TRX-{Transaksi._jumlah_transaksi:03d}"
        self.pelanggan = pelanggan   
        self._items = []

    def tambah_item(self, menu, jumlah=1):
        self._items.append(ItemPesanan(menu, jumlah))

    def total(self):
        return sum(item.subtotal() for item in self._items)

    def cetak_struk(self):
        print("  ---------------- STRUK ----------------")
        print(f"  {self.id} - {self.pelanggan}")
        print("  ---------------------------------------")
        for item in self._items:
            item.cetak()
        print("  ---------------------------------------")
        print(baris("TOTAL BAYAR", rp(self.total())))
        print("  ---------------------------------------")

    def __len__(self):
        return len(self._items)

    def __lt__(self, lain):
        return self.total() < lain.total()

    def __str__(self):
        return f"{self.id} | {self.pelanggan.nama:<10} | {len(self)} item | {rp(self.total())}"

class Tunai:
    nama = "Tunai"

    def __init__(self, uang_diterima):
        self.uang_diterima = uang_diterima

    @classmethod
    def dari_input(cls):
        return cls(baca_int("Uang diterima: ", 0))

    def bayar(self, total):
        if self.uang_diterima < total:
            print(f"Uang kurang {rp(total - self.uang_diterima)}")
            return False
        print(f"Lunas, kembalian {rp(self.uang_diterima - total)}")
        return True

class QRIS:
    nama = "QRIS"

    def __init__(self, provider):
        self.provider = provider

    @classmethod
    def dari_input(cls):
        provider = input("Pembayaran lewat (GoPay/OVO/Dana/ShopeePay/Bank/dll): ").strip() or "QRIS"
        return cls(provider)

    def bayar(self, total):
        print(f"{rp(total)} dibayar lewat {self.provider}, lunas")
        return True

METODE_BAYAR = {"1": Tunai, "2": QRIS}

def proses_bayar(metode, total):
    return metode.bayar(total)

def lihat_menu(daftar):
    print("\n--- DAFTAR MENU ---")
    daftar.tampilkan()

def tambah_menu(daftar):
    print("\n--- TAMBAH MENU ---")
    nama = input("  Nama menu: ").strip()
    if not punya_huruf(nama):
        print("Nama menu huruf. ")
        return
    harga = baca_int("  Harga dasar (Rp): ")
    print("  Jenis: 1. Kopi  2. Non-Kopi  3. Blended")
    kelas = JENIS_MENU.get(input("  Pilih jenis: ").strip())
    if kelas is None:
        print("Jenis tidak dikenal.")
        return
    menu = kelas.dari_input(nama, harga)
    if daftar.tambah(menu):
        print(f"Menu '{menu.nama}' ditambahkan.")
    else:
        print(f"Menu '{nama}' sudah ada.")

def hapus_menu(daftar):
    print("\n--- HAPUS MENU ---")
    if len(daftar) == 0:
        print("(menu masih kosong)")
        return
    daftar.tampilkan()
    nomor = baca_int("  Nomor menu yang dihapus (0 = batal): ", 0)
    if nomor == 0:
        return
    if nomor > len(daftar):
        print("Nomor tidak ada.")
        return
    menu = daftar[nomor - 1]
    yakin = input(f"  Yakin hapus '{menu.nama}'? (y/n): ").strip().lower()
    if yakin != "y":
        print("Penghapusan dibatalkan.")
        return
    daftar.hapus(nomor)
    print(f"Menu '{menu.nama}' dihapus dari daftar.")

def buat_transaksi(daftar, riwayat):
    print("\n--- BUAT TRANSAKSI ---")
    if len(daftar) == 0:
        print("Menu masih kosong, tambah menu dulu.")
        return
    nama = baca_nama()
    no_hp = baca_no_hp()
    transaksi = Transaksi(Pelanggan(nama, no_hp))

    while True:
        print()
        daftar.tampilkan()
        nomor = baca_int("  Pilih nomor menu (0 = selesai): ", 0)
        if nomor == 0:
            break
        if nomor > len(daftar):
            print("Nomor gak ada.")
            continue
        jumlah = baca_int("  Jumlah: ")
        transaksi.tambah_item(daftar[nomor - 1], jumlah)
        print(f"Ditambahkan. Total sementara {rp(transaksi.total())}")

    if len(transaksi) == 0:
        print("Gak ada item, transaksi dibatalkan.")
        return

    print()
    transaksi.cetak_struk()
    while True:
        print("Metode bayar: 1. Tunai  2. QRIS")
        kelas = METODE_BAYAR.get(input("  Pilih metode: ").strip())
        if kelas is None:
            print("Metode tidak dikenal.")
            continue
        metode = kelas.dari_input()
        if proses_bayar(metode, transaksi.total()):
            break
        if input("Coba lagi? (y/n): ").strip().lower() != "y":
            print("Transaksi dibatalkan.")
            return

    riwayat.append(transaksi)
    tampilkan_riwayat(riwayat)

def tampilkan_riwayat(riwayat):
    print("\n--- RIWAYAT TRANSAKSI HARI INI ---")
    for t in sorted(riwayat, reverse=True):   
        print(f"  {t}")
    pendapatan = sum(t.total() for t in riwayat)
    print(f"Total pendapatan: {rp(pendapatan)} dari {len(riwayat)} transaksi")

def cek_abstraksi():
    try:
        Menu("tes", 0)
    except TypeError as e:
        print(f"[Cek Abstraksi] TypeError: {e}")

def data_awal():
    daftar = DaftarMenu()
    daftar.tambah(Kopi("Americano", 18000))
    daftar.tambah(Kopi("Cafe Latte", 22000, shot=2))
    daftar.tambah(NonKopi("Matcha", 24000, ["boba"]))
    daftar.tambah(NonKopi("Strawberry Milk", 20000, ["Buah Strawberry"]))
    daftar.tambah(Blended("Choco Blended", 28000, ukuran_ml=450))
    return daftar

def main():
    cek_abstraksi()
    daftar = data_awal()
    riwayat = []

    while True:
        print("\n=========== COFFEE SHOP ===========")
        print("1. Lihat daftar menu")
        print("2. Tambah menu")
        print("3. Hapus menu")
        print("4. Buat transaksi")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "0":
            print("Terima kasih! Selamat Datang Kembali")
            break

        aksi = {
            "1": lambda: lihat_menu(daftar),
            "2": lambda: tambah_menu(daftar),
            "3": lambda: hapus_menu(daftar),
            "4": lambda: buat_transaksi(daftar, riwayat),
        }.get(pilihan)
        if aksi is None:
            print("Pilihan tidak valid.")
        else:
            aksi()

if __name__ == "__main__":
    main()