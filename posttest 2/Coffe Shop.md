Nama  : Rafalia Khanza Taufik 
NIM   : 2509106104 
Kelas : C1 25
Posttest 2 PBO

Sistem Pendataan Transaksi dan Menu Minuman pada Coffe Shop = AA Coffe

1. Deskripsi Program Masih lanjutan program AA Coffe yang kemarin, tapi sekarang class-nya udah ada pewarisan (inheritance) dan relasi antar class (asosiasi, agregasi, komposisi). Jadinya ada 11 class:

Class Fungsi Menu -> parent buat menu minuman (nama, harga, kategori, stok) MenuCoffee -> anak Menu, ada extra shot MenuNonCoffee -> anak Menu, ada tingkat manis Pelanggan -> parent pelanggan biasa (nama, no hp, saldo) PelangganMember -> anak Pelanggan, dapat diskon + poin PelangganVIP -> anak PelangganMember, juga mewarisi LayananDelivery LayananDelivery -> tambahan fitur antar pesanan Karyawan -> parent karyawan, anaknya Kasir dan Barista ItemPesanan -> satu baris pesanan (menu + jumlah) Transaksi -> catat pesanan, hitung total, proses bayar CoffeeShop -> nampung daftar menu dan karyawan

2. Alur Singkat Program pelanggan top up -> pesan lewat Transaksi -> kasir proses bayar -> stok berkurang, saldo kepotong (udah diskon + pajak) -> member dapat poin, poinnya bisa ditukar jadi saldo.

3. Relasi Antar Class

**Pewarisan**

- Hierarchical : Menu -> MenuCoffee & MenuNonCoffee, Karyawan -> Kasir & Barista
- Multilevel : Pelanggan -> PelangganMember -> PelangganVIP
- Multiple : PelangganVIP mewarisi PelangganMember dan LayananDelivery (urutan MRO: PelangganVIP, PelangganMember, Pelanggan, LayananDelivery, object)

**Relasi lain**

- Komposisi => Transaksi terdiri dari ItemPesanan, objeknya dibuat langsung di dalam tambah_item()
- Agregasi => CoffeeShop memiliki Menu dan Karyawan, dibuat di luar terus dititipin ke toko. Kalau toko dihapus, menu sama karyawannya tetap ada
- Asosiasi => Kasir make Transaksi lewat parameter di layani_pembayaran(), Transaksi juga make objek Pelanggan

4. **Struktur Class**

=====Class Menu=====

**Atribut Class**

- nama_coffee_shop, total_menu_terdaftar, kategori_valid

**Atribut Instance**

- nama_minuman, kategori => public
- __harga => private, lewat property harga
- _stok => protected (biar bisa dipakai anaknya), lewat property stok 

**Method**

- Instance Method => hitung_harga(), tampilkan_info(), kurangi_stok(jumlah)
- Class Method => dari_dict(cls, data), ubah_nama_toko(cls, nama_baru)
- Static Method => validasi_kategori(kategori)

**Property**

- harga => setter nolak kalau 0 atau kurang
- stok => setter nolak kalau negatif

=====Class MenuCoffee=====

- Atribut class : biaya_extra_shot (Rp5.000 per shot)
- Atribut instance : extra_shot
- Manggil super().init() buat ngisi atribut punya Menu
- Override : hitung_harga() (harga + biaya shot), tampilkan_info(), dari_dict()

=====Class MenuNonCoffee=====

- Atribut instance : tingkat_manis
- Method baru : atur_manis(persen), harus 0 sampai 100
- Override : tampilkan_info()

=====Class Pelanggan=====

**Atribut Class**

- total_pelanggan, minimal_topup, diskon_persen (0 buat pelanggan biasa)

**Atribut Instance**

- nama, no_hp => public
- _saldo => protected, lewat property saldo (setter nolak negatif)

**Method**

- Instance Method => top_up(jumlah), dapat_poin(total), info()
- Class Method => daftar_baru(cls, data)
- Static Method => validasi_no_hp(no_hp)

=====Class PelangganMember=====

- diskon_persen = 10 (nimpa punya parent)
- __poin private, lewat property poin. Setter-nya raise ValueError kalau negatif
- Override dapat_poin(): tiap belanja Rp10.000 dapat 1 poin
- Method baru tukar_poin(jumlah), 1 poin = Rp100

=====Class PelangganVIP=====

- diskon_persen = 20
- Override dapat_poin(): poinnya dobel
- Dapat antar_pesanan(alamat) dari LayananDelivery

=====Class Karyawan, Kasir, Barista=====

- Karyawan : nama, nip, posisi, property info_singkat
- Kasir : layani_pembayaran(transaksi), di dalamnya manggil transaksi.bayar()
- Barista : buat_minuman(menu)

=====Class ItemPesanan=====

- menu, jumlah, subtotal() (harganya dari hitung_harga() punya menu)

=====Class Transaksi=====

**Atribut Class**

- total_transaksi, pajak_persen, maksimal_item

**Atribut Instance**

- pelanggan, status => public
- _daftar_item => list isinya ItemPesanan
- __id_transaksi => private, dibuat otomatis, cuman bisa dibaca lewat property id_transaksi

**Method**

- Instance Method => jumlah_item(), tambah_item(menu, jumlah), hitung_total(), bayar(), struk()
- Class Method => ubah_pajak(cls, persen_baru)
- Static Method => hitung_pajak(subtotal, persen)

=====Class CoffeeShop=====

- nama, _menu, _karyawan
- Method : tambah_menu(), tambah_karyawan(), tampilkan_info()

5. Validasi Yang Diterapkan

Data Aturan Kalau dilanggar harga(Menu) Harus lebih dari 0 Dicetak [gagal], nilai lama dipertahankan stok(Menu) Tidak boleh negatif Dicetak [gagal], nilai lama dipertahankan tingkat_manis 0 sampai 100 Ditolak Nama toko Tidak boleh kosong Ditolak saldo(Pelanggan) Tidak boleh negatif Dicetak [gagal], nilai lama dipertahankan poin(PelangganMember) Tidak boleh negatif raise ValueError Nominal top up Minimal sesuai minimal_topup Ditolak Tukar poin Harus > 0 dan tidak lebih dari poin Ditolak Jumlah item transaksi Minimal 1, total maksimal 10 Ditolak Stok saat transaksi Tidak boleh melebihi stok Item tidak jadi ditambahkan Saldo saat bayar Harus cukup buat total transaksi Pembayaran ditolak Transaksi udah lunas Gak bisa tambah item / bayar lagi Ditolak Pajak Tidak boleh negatif Ditolak

6. Panduan Pengujian (Main Code)

7. Menu

- Bikin MenuCoffee (lewat konstruktor sama dari_dict) dan MenuNonCoffee
- Panggil tampilkan_info() buat lihat hasil override
- Uji setter stok, harga, dan atur_manis pakai nilai valid dan tidak valid
- Uji ubah_nama_toko() dan validasi_kategori()
- Cek isinstance() dan issubclass()

8. Pelanggan

- Bikin 1 Pelanggan, 1 PelangganMember (lewat daftar_baru), 1 PelangganVIP
- Uji top_up valid dan di bawah minimal, setter saldo negatif, setter poin negatif (kena ValueError)
- Bandingin diskon tiap jenis lewat info()
- Panggil antar_pesanan() dan print MRO PelangganVIP

9. Karyawan dan CoffeeShop

- Bikin Kasir dan Barista di luar, terus masukin ke CoffeeShop
- Hapus objek toko pakai del, habis itu cek menu sama karyawannya masih ada

10. Transaksi

- Bikin 3 transaksi buat 3 jenis pelanggan
- Tambah item yang valid, terus yang kelebihan stok dan jumlah 0 (harus ditolak)
- Bayar lewat Kasir, cetak struk, lihat poin yang didapat
- Uji tukar_poin, hitung_pajak, dan ubah_pajak

Kalau dijalankan, output-nya campuran pesan [sukses] dan [gagal], itu buktinya validasi jalan sesuai aturan di atas.