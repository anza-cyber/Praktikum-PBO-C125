class Menu:
    nama_coffee_shop = "AA Coffe"
    total_menu_terdaftar = 0
    kategori_valid = ["Coffee", "Non-Coffee", "Signature"]

    def __init__(self, nama_minuman, harga, kategori, stok):
        self.nama_minuman = nama_minuman
        self.harga = harga 
        self.kategori = kategori
        self.__stok = stok
        Menu.total_menu_terdaftar += 1 

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, stok_baru):
        if stok_baru < 0:
            print(f'[gagal] Stok {self.nama_minuman} tidak boleh negatif')
            return
        self.__stok = stok_baru

    def tampilkan_info(self):
        print(f'{self.nama_minuman} ({self.kategori}) - Rp{self.harga:,} | Stok: {self.__stok}')

    def kurangi_stok(self, jumlah):
        if jumlah > self.__stok:
            print(f'[gagal] Stok {self.nama_minuman} tidak cukup, sisa {self.__stok}')
            return False
        self.__stok -= jumlah
        return True

    @classmethod
    def dari_dict(cls, data):
        """Membuat objek Menu dari dictionary"""
        return cls(data['nama'], data['harga'], data['kategori'], data['stok'])

    @classmethod
    def ubah_nama_toko(cls, nama_baru):
        cls.nama_coffee_shop = nama_baru

    @staticmethod
    def validasi_kategori(kategori):
        return kategori in Menu.kategori_valid


class Pelanggan:
    total_pelanggan = 0
    minimal_topup = 10000

    def __init__(self, nama, no_hp):
        self.nama = nama
        self.no_hp = no_hp
        self.member = False
        self.__saldo = 0
        Pelanggan.total_pelanggan += 1 

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo_baru):
        if saldo_baru < 0:
            print(f'[gagal] Saldo {self.nama} tidak boleh negatif')
            return
        self.__saldo = saldo_baru

    def top_up(self, jumlah):
        if jumlah < Pelanggan.minimal_topup:
            print(f'[gagal] Minimal top up Rp{Pelanggan.minimal_topup:,}')
            return
        self.saldo = self.__saldo + jumlah
        print(f'[sukses] {self.nama} top up Rp{jumlah:,} saldo sekarang Rp{self.__saldo:,}')

    def jadi_member(self):
        self.member = True
        print(f'{self.nama} selamat, sekarang sudah jadi member')

    @classmethod
    def daftar_baru(cls, data):
        return cls(data['nama'], data['no_hp'])

    @staticmethod
    def validasi_no_hp(no_hp):  
        return no_hp.isdigit() and len(no_hp) >= 10


class Transaksi:
    total_transaksi = 0
    pajak_persen = 10

    def __init__(self, pelanggan):
        self.pelanggan = pelanggan
        self.daftar_item = []
        Transaksi.total_transaksi += 1
        self.__id_transaksi = f'TRX-{Transaksi.total_transaksi:04d}'

    @property
    def id_transaksi(self):
        return self.__id_transaksi

    def tambah_item(self, menu, jumlah):
        if jumlah <= 0:
            print("[gagal] Jumlah pesanan minimal 1")
            return
        if not menu.kurangi_stok(jumlah):
            return
        self.daftar_item.append((menu, jumlah))
        print(f'[+] {jumlah}x {menu.nama_minuman} ditambahkan ke {self.__id_transaksi}')
 
    def hitung_total(self):
        subtotal = sum(menu.harga * jumlah for menu, jumlah in self.daftar_item)
        pajak = Transaksi.hitung_pajak(subtotal)
        return subtotal + pajak
 
    def bayar(self):
        total = self.hitung_total()
        if self.pelanggan.saldo < total:
            print(f'[gagal] Saldo {self.pelanggan.nama} tidak cukup buat bayar Rp{total:,.0f}')
            return False
        
        self.pelanggan.saldo = self.pelanggan.saldo - total
        print(f'[sukses] {self.pelanggan.nama} bayar Rp{total:,.0f} untuk {self.__id_transaksi}')
        return True
 
    def struk(self):
        print(f'\n===== STRUK {self.__id_transaksi} =====')
        print(f'Pelanggan : {self.pelanggan.nama}')
        for menu, jumlah in self.daftar_item:
            print(f'{jumlah}x {menu.nama_minuman} @Rp{menu.harga:,}')
        print(f'Total (sudah termasuk pajak {Transaksi.pajak_persen}%): Rp{self.hitung_total():,.0f}')
        print("=" * 32 + "\n")

    @classmethod
    def ubah_pajak(cls, persen_baru):
        """Ubah persentase pajak, berlaku buat semua transaksi ke depannya"""
        cls.pajak_persen = persen_baru
 
    @staticmethod
    def hitung_pajak(subtotal):
        return subtotal * Transaksi.pajak_persen / 100


if __name__ == "__main__":
    print("=== Testing Class Menu ===")
    kopi_susu = Menu("Kopi Susu Gula Aren", 18000, "Coffee", 20)
    matcha = Menu.dari_dict({"nama": "Matcha Latte", "harga": 22000, "kategori": "Non-Coffee", "stok": 15})
 
    kopi_susu.tampilkan_info()
    matcha.tampilkan_info()
 
    print("Total menu terdaftar :", Menu.total_menu_terdaftar)
    print("Validasi kategori 'Coffee' :", Menu.validasi_kategori("Coffee"))
    print("Validasi kategori 'Jus'    :", Menu.validasi_kategori("Jus"))
 
    print("\n-- Uji setter stok (valid & tidak valid) --")
    kopi_susu.stok = 25  
    print("Stok baru:", kopi_susu.stok)
    kopi_susu.stok = -5 
 
    print("\n-- Uji classmethod ubah_nama_toko --")
    Menu.ubah_nama_toko("Kopi Senja Coffee & Roastery")
    print("Nama toko sekarang:", Menu.nama_coffee_shop)
 
    print("\n=== Testing Class Pelanggan ===")
    andi = Pelanggan("Andi Saputra", "081234567890")
    siti = Pelanggan.daftar_baru({"nama": "Siti Aminah", "no_hp": "081298765432"})
 
    print("Total pelanggan terdaftar :", Pelanggan.total_pelanggan)
    print("Validasi no hp Andi   :", Pelanggan.validasi_no_hp(andi.no_hp))
    print("Validasi no hp ngasal :", Pelanggan.validasi_no_hp("abc123"))
 
    print("\n-- Uji top up (valid & tidak valid) --")
    andi.top_up(100000)
    andi.top_up(5000)     
    siti.top_up(100000)
    siti.jadi_member()
 
    print("\n=== Uji setter saldo langsung (tidak valid) ===")
    andi.saldo = -10000   
    print("Saldo Andi tetap:", andi.saldo)
 
    print('\n=== Testing Class Transaksi ===')
    trx1 = Transaksi(andi)
    trx1.tambah_item(kopi_susu, 2)
    trx1.tambah_item(matcha, 1)
    trx1.bayar()
    trx1.struk()
 
    trx2 = Transaksi(siti)
    trx2.tambah_item(matcha, 3)
    trx2.tambah_item(kopi_susu, 100)  
    trx2.bayar()
    trx2.struk()
 
    print("-- Uji classmethod ubah_pajak --")
    print("Pajak sebelum diubah :", Transaksi.pajak_persen, "%")
    Transaksi.ubah_pajak(11)
    print("Pajak sesudah diubah :", Transaksi.pajak_persen, "%")
 
    print("\nTotal transaksi yang sudah dibuat:", Transaksi.total_transaksi)