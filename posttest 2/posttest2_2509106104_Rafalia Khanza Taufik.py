class Menu:
    nama_coffee_shop = "AA Coffe"
    total_menu_terdaftar = 0
    kategori_valid = ["Coffee", "Non-Coffee", "Signature"]

    def __init__(self, nama_minuman, harga, kategori, stok):
        self.nama_minuman = nama_minuman
        self.kategori = kategori
        self.__harga = 0
        self._stok = 0
        self.harga = harga
        self.stok = stok
        Menu.total_menu_terdaftar += 1

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, harga_baru):
        if harga_baru <= 0:
            print(f'[gagal] Harga {self.nama_minuman} harus lebih dari 0')
            return
        self.__harga = harga_baru

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, stok_baru):
        if stok_baru < 0:
            print(f'[gagal] Stok {self.nama_minuman} tidak boleh negatif')
            return
        self._stok = stok_baru

    def hitung_harga(self):
        return self.__harga

    def tampilkan_info(self):
        print(f'{self.nama_minuman} ({self.kategori}) - Rp{self.hitung_harga():,} | Stok: {self._stok}')

    def kurangi_stok(self, jumlah):
        if jumlah > self._stok:
            print(f'[gagal] Stok {self.nama_minuman} tidak cukup, sisa {self._stok}')
            return False
        self._stok -= jumlah
        return True

    @classmethod
    def dari_dict(cls, data):
        return cls(data['nama'], data['harga'], data['kategori'], data['stok'])

    @classmethod
    def ubah_nama_toko(cls, nama_baru):
        if nama_baru.strip() == "":
            print('[gagal] Nama toko tidak boleh kosong')
            return
        cls.nama_coffee_shop = nama_baru

    @staticmethod
    def validasi_kategori(kategori):
        return kategori in Menu.kategori_valid


class MenuCoffee(Menu):
    biaya_extra_shot = 5000

    def __init__(self, nama_minuman, harga, stok, extra_shot=0):
        super().__init__(nama_minuman, harga, "Coffee", stok)
        self.extra_shot = extra_shot

    def hitung_harga(self):
        return super().hitung_harga() + self.extra_shot * MenuCoffee.biaya_extra_shot

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f'   extra shot: {self.extra_shot}')

    @classmethod
    def dari_dict(cls, data):
        return cls(data['nama'], data['harga'], data['stok'], data.get('extra_shot', 0))


class MenuNonCoffee(Menu):
    def __init__(self, nama_minuman, harga, stok, tingkat_manis=50):
        super().__init__(nama_minuman, harga, "Non-Coffee", stok)
        self.tingkat_manis = tingkat_manis

    def atur_manis(self, persen):
        if persen < 0 or persen > 100:
            print('[gagal] Tingkat manis harus 0 - 100')
            return
        self.tingkat_manis = persen

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f'   tingkat manis: {self.tingkat_manis}%')


class LayananDelivery:
    """Kemampuan tambahan (mixin), bukan jenis pelanggan."""

    def antar_pesanan(self, alamat):
        print(f'[delivery] Pesanan {self.nama} diantar ke {alamat}')


class Pelanggan:
    total_pelanggan = 0
    minimal_topup = 10000
    diskon_persen = 0

    def __init__(self, nama, no_hp):
        self.nama = nama
        self.no_hp = no_hp
        self._saldo = 0
        Pelanggan.total_pelanggan += 1

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, saldo_baru):
        if saldo_baru < 0:
            print(f'[gagal] Saldo {self.nama} tidak boleh negatif')
            return
        self._saldo = saldo_baru

    def top_up(self, jumlah):
        if jumlah < Pelanggan.minimal_topup:
            print(f'[gagal] Minimal top up Rp{Pelanggan.minimal_topup:,}')
            return
        self.saldo = self._saldo + jumlah
        print(f'[sukses] {self.nama} top up Rp{jumlah:,}, saldo sekarang Rp{self._saldo:,}')

    def dapat_poin(self, total):
        return 0

    def info(self):
        print(f'{self.nama} ({type(self).__name__}) | Saldo Rp{self._saldo:,} | Diskon {self.diskon_persen}%')

    @classmethod
    def daftar_baru(cls, data):
        return cls(data['nama'], data['no_hp'])

    @staticmethod
    def validasi_no_hp(no_hp):
        return no_hp.isdigit() and len(no_hp) >= 10


class PelangganMember(Pelanggan):
    diskon_persen = 10

    def __init__(self, nama, no_hp):
        super().__init__(nama, no_hp)
        self.__poin = 0

    @property
    def poin(self):
        return self.__poin

    @poin.setter
    def poin(self, poin_baru):
        if poin_baru < 0:
            raise ValueError('Poin tidak boleh negatif')
        self.__poin = poin_baru

    def dapat_poin(self, total):
        tambahan = int(total // 10000)
        self.poin = self.__poin + tambahan
        return tambahan

    def tukar_poin(self, jumlah):
        """1 poin = Rp100"""
        if jumlah <= 0 or jumlah > self.__poin:
            print(f'[gagal] Poin {self.nama} gak cukup (punya {self.__poin})')
            return
        self.poin = self.__poin - jumlah
        self.saldo = self._saldo + jumlah * 100
        print(f'[sukses] {self.nama} tukar {jumlah} poin jadi Rp{jumlah * 100:,}')


class PelangganVIP(PelangganMember, LayananDelivery):
    diskon_persen = 20

    def dapat_poin(self, total):
        return super().dapat_poin(total) + super().dapat_poin(total)


class Karyawan:
    def __init__(self, nama, nip, posisi):
        self.nama = nama
        self.nip = nip
        self.posisi = posisi

    @property
    def info_singkat(self):
        return f'{self.nama} ({self.posisi}) - NIP: {self.nip}'


class Kasir(Karyawan):
    def __init__(self, nama, nip):
        super().__init__(nama, nip, "Kasir")

    def layani_pembayaran(self, transaksi):
        print(f'[kasir] {self.nama} memproses {transaksi.id_transaksi}')
        return transaksi.bayar()


class Barista(Karyawan):
    def __init__(self, nama, nip):
        super().__init__(nama, nip, "Barista")

    def buat_minuman(self, menu):
        print(f'[barista] {self.nama} membuat {menu.nama_minuman}')


class ItemPesanan:
    """Gak ada artinya tanpa Transaksi, dibuat di dalam Transaksi."""

    def __init__(self, menu, jumlah):
        self.menu = menu
        self.jumlah = jumlah

    def subtotal(self):
        return self.menu.hitung_harga() * self.jumlah


class Transaksi:
    total_transaksi = 0
    pajak_persen = 10
    maksimal_item = 10

    def __init__(self, pelanggan):
        self.pelanggan = pelanggan
        self.status = "Belum Bayar"
        self._daftar_item = []
        Transaksi.total_transaksi += 1
        self.__id_transaksi = f'TRX-{Transaksi.total_transaksi:04d}'

    @property
    def id_transaksi(self):
        return self.__id_transaksi

    def jumlah_item(self):
        return sum(item.jumlah for item in self._daftar_item)

    def tambah_item(self, menu, jumlah):
        if self.status == "Lunas":
            print(f'[gagal] {self.__id_transaksi} sudah lunas')
            return
        if jumlah <= 0:
            print('[gagal] Jumlah pesanan minimal 1')
            return
        if self.jumlah_item() + jumlah > Transaksi.maksimal_item:
            print(f'[gagal] Maksimal {Transaksi.maksimal_item} item per transaksi')
            return
        sudah = sum(i.jumlah for i in self._daftar_item if i.menu is menu)
        if sudah + jumlah > menu.stok:
            print(f'[gagal] Stok {menu.nama_minuman} tidak cukup, sisa {menu.stok}')
            return
        self._daftar_item.append(ItemPesanan(menu, jumlah))
        print(f'[+] {jumlah}x {menu.nama_minuman} ditambahkan ke {self.__id_transaksi}')

    def hitung_total(self):
        subtotal = sum(item.subtotal() for item in self._daftar_item)
        subtotal -= subtotal * self.pelanggan.diskon_persen / 100
        return subtotal + Transaksi.hitung_pajak(subtotal, Transaksi.pajak_persen)

    def bayar(self):
        if self.status == "Lunas":
            print(f'[gagal] {self.__id_transaksi} sudah dibayar')
            return False
        if not self._daftar_item:
            print('[gagal] Belum ada item yang dipesan')
            return False
        total = self.hitung_total()
        if self.pelanggan.saldo < total:
            print(f'[gagal] Saldo {self.pelanggan.nama} tidak cukup buat bayar Rp{total:,.0f}')
            return False
        for item in self._daftar_item:
            item.menu.kurangi_stok(item.jumlah)
        self.pelanggan.saldo = self.pelanggan.saldo - total
        self.status = "Lunas"
        print(f'[sukses] {self.pelanggan.nama} bayar Rp{total:,.0f} untuk {self.__id_transaksi}')
        poin = self.pelanggan.dapat_poin(total)
        if poin:
            print(f'         +{poin} poin')
        return True

    def struk(self):
        print(f'\n===== STRUK {self.__id_transaksi} =====')
        print(f'Pelanggan : {self.pelanggan.nama} ({type(self.pelanggan).__name__})')
        for item in self._daftar_item:
            print(f'{item.jumlah}x {item.menu.nama_minuman} @Rp{item.menu.hitung_harga():,}')
        print(f'Diskon {self.pelanggan.diskon_persen}% | Pajak {Transaksi.pajak_persen}%')
        print(f'Total : Rp{self.hitung_total():,.0f} ({self.status})')
        print("=" * 32 + "\n")

    @classmethod
    def ubah_pajak(cls, persen_baru):
        if persen_baru < 0:
            print('[gagal] Pajak tidak boleh negatif')
            return
        cls.pajak_persen = persen_baru

    @staticmethod
    def hitung_pajak(subtotal, persen):
        return subtotal * persen / 100


class CoffeeShop:
    def __init__(self, nama):
        self.nama = nama
        self._menu = []
        self._karyawan = []

    def tambah_menu(self, menu):
        if isinstance(menu, Menu):
            self._menu.append(menu)
            print(f'[+] {menu.nama_minuman} masuk daftar menu {self.nama}')

    def tambah_karyawan(self, karyawan):
        if isinstance(karyawan, Karyawan):
            self._karyawan.append(karyawan)
            print(f'[+] {karyawan.nama} mulai bekerja di {self.nama}')

    def tampilkan_info(self):
        print(f'\n== {self.nama} ==')
        print(f'Menu ({len(self._menu)}):')
        for m in self._menu:
            print('  -', m.nama_minuman)
        print(f'Karyawan ({len(self._karyawan)}):')
        for k in self._karyawan:
            print('  -', k.info_singkat)


if __name__ == "__main__":
    print("=== Menu (hierarchical inheritance) ===")
    kopi_susu = MenuCoffee("Kopi Susu Gula Aren", 18000, 20, extra_shot=1)
    americano = MenuCoffee.dari_dict({"nama": "Americano", "harga": 15000, "stok": 10})
    matcha = MenuNonCoffee("Matcha Latte", 22000, 15, tingkat_manis=70)
    coklat = MenuNonCoffee("Coklat Dingin", 20000, 12)

    for m in (kopi_susu, americano, matcha, coklat):
        m.tampilkan_info()
    print("Total menu terdaftar :", Menu.total_menu_terdaftar)
    print("Validasi 'Coffee' / 'Jus':", Menu.validasi_kategori("Coffee"), Menu.validasi_kategori("Jus"))

    print("\n-- setter valid & tidak valid --")
    kopi_susu.stok = 25
    kopi_susu.stok = -5
    kopi_susu.harga = 0
    matcha.atur_manis(150)
    Menu.ubah_nama_toko("AA Coffe Samarinda")
    Menu.ubah_nama_toko("  ")
    print("Nama toko:", Menu.nama_coffee_shop)

    print("\n-- cek pewarisan --")
    print("isinstance(kopi_susu, Menu)       :", isinstance(kopi_susu, Menu))
    print("isinstance(matcha, MenuCoffee)    :", isinstance(matcha, MenuCoffee))
    print("issubclass(MenuNonCoffee, Menu)   :", issubclass(MenuNonCoffee, Menu))

    print("\n=== Pelanggan (multilevel + multiple inheritance) ===")
    andi = Pelanggan("Andi Saputra", "081234567890")
    siti = PelangganMember.daftar_baru({"nama": "Siti Aminah", "no_hp": "081298765432"})
    rafa = PelangganVIP("Rafa", "081377788899")

    print("Validasi no hp:", Pelanggan.validasi_no_hp(andi.no_hp), Pelanggan.validasi_no_hp("abc"))
    andi.top_up(100000)
    andi.top_up(5000)
    siti.top_up(150000)
    rafa.top_up(200000)
    andi.saldo = -1
    try:
        siti.poin = -3
    except ValueError as e:
        print(f'[gagal] {e}')
    for p in (andi, siti, rafa):
        p.info()
    rafa.antar_pesanan("Jl. Pramuka, Samarinda")
    print("MRO PelangganVIP:", [k.__name__ for k in PelangganVIP.mro()])

    print("\n=== Karyawan + Agregasi (CoffeeShop) ===")
    kasir = Kasir("Dewi", "EMP01")
    barista = Barista("Budi", "EMP02")
    toko = CoffeeShop("AA Coffe")
    for m in (kopi_susu, matcha):
        toko.tambah_menu(m)
    toko.tambah_karyawan(kasir)
    toko.tambah_karyawan(barista)
    toko.tampilkan_info()

    print("\n=== Transaksi (komposisi ItemPesanan + asosiasi Kasir) ===")
    trx1 = Transaksi(andi)
    trx1.tambah_item(kopi_susu, 2)
    trx1.tambah_item(matcha, 1)
    barista.buat_minuman(kopi_susu)
    kasir.layani_pembayaran(trx1)
    trx1.struk()

    trx2 = Transaksi(siti)
    trx2.tambah_item(matcha, 3)
    trx2.tambah_item(kopi_susu, 100)
    trx2.tambah_item(kopi_susu, 0)
    kasir.layani_pembayaran(trx2)
    trx2.struk()

    trx3 = Transaksi(rafa)
    trx3.tambah_item(coklat, 2)
    kasir.layani_pembayaran(trx3)
    trx3.struk()

    print("-- tukar poin --")
    print("Poin Siti:", siti.poin, "| Poin Rafa:", rafa.poin)
    siti.tukar_poin(2)
    siti.tukar_poin(999)

    print("\n-- static & class method --")
    print("Pajak Rp50.000 @10% :", Transaksi.hitung_pajak(50000, 10))
    Transaksi.ubah_pajak(11)
    print("Pajak sekarang:", Transaksi.pajak_persen, "%")
    Transaksi.ubah_pajak(-1)

    print("\n-- bukti agregasi: toko dihapus, menu & karyawan tetap ada --")
    del toko
    kopi_susu.tampilkan_info()
    print(kasir.info_singkat)
    print("Total transaksi:", Transaksi.total_transaksi)