Nama  : Rafalia Khanza Taufik
NIM   : 2509106104
Kelas : C1 
Posttest 1 PBO

Sistem Pendataan Transaksi dan Menu Minuman pada Coffe Shop = AA Coffe

1. Deskripsi Program
Program ini mensimulasikan sistem pendataan menu minuman dan transaksi pada sebuah coffe shop bernama AA Coffe. Ada 3 class utama yang saling berinteraksi lewat objek.

Class                 Fungsi
Menu        ->        Menyimpan data menu minuman: nama,harga, kategori, dan stok.
Pelanggan   ->        Menyimpan data pelanggan: nama, no hp, status member, dan saldo.
Transaksi   ->        Menggabungkan objek Pelanggan dan Menu untuk mencatat pesanan,
                      menghitung total + pajak, dan memproses pembayaran

2. Alur Singkat Program
pelanggan top up saldo -> pelanggan pesan menu lewat objek Transaksi -> stok menu otomatis berkurang -> saldo pelanggan otomatis terpotong sesuai total belanja (termasuk pajak).

3. Struktur Class

=====Class Menu=====

Atribut Class (dipakai bareng semua objek)
- nama_coffe_shop      => nama toko
- total_menu_terdaftar => counter, nambah otomatis tiap ada objek Menu baru
- kategori_valid       => list kategori yang diperbolehkan

Atribut Intance 
- nama_minuman, harga, kategori => public, bisa diakses langsung
- __stok                        => private, cuman bisa diubah lewat property stok

Method
- Instance Method => tampilkan_info(), kurangi_stok(jumlah)
- Class Method   => dari_dict(cls, data) (factory method dari dictionary), ubah_nama_toko 
                    (cls, nama_baru)
- Static Method  => validasi_kategori(kategori)

Property Stok
- Getter (@property)   => ambil nilai stok
- Setter (stok.setter) => tolak kalau nilainya negatif

=====Class Pelanggan=====

Atribut Class
- total_pelanggan => counter jumlah pelanggan terdaftar
- minimal_topup   => batas minimal nominal top up

Atribut Instance
- nama, no_hp, member => public
- __saldo             => private, cuman bisa diubah lewat property saldo

Method
- Instance Method => top_up(jumlah), jadi_member()
- Class Method    => daftar_baru(cls, data) (factory method dari dictionary)
- Static Method   => validasi_no_hp(no_hp)

Property
- Getter => ambil nilai saldo
- Setter => tolak kalau nilainya negatif

=====Class Transaksi=====

Atribut Class
- total_transaksi => counter jumlah transaksi yang pernah dibuat
- pajak_persen    => persentase pajak yang dikenakan ke tiap transaksi

Atribut Instanse
- pelanggan      => objek Pelanggan yang lagi belanja(public)
- daftar_item    => list pesanan berisi pasangan (objek Menu,jumlah) (public)
- __id_transaksi => private, dibuat otomatis pakai counter, cuman bisa dibaca lewat 
                    property id_transaksi (tidak ada setter karena id transaksi memang tidak boleh diubah dari luar)

Method
- Instance Method => tambah_item(menu, jumlah), hitung_total(), bayar(), struk()
- Class Method    => ubah_pajak(cls, persen_baru)
- Static Method   => hitung_pajak(subtotal)

4. Validasi Yang Diterapkan

Data                           Aturan                               Kalau dilanggar
stok(Menu)                     Tidak boleh negatif                  Dicetak pesan [gagal], nilai lama dipertahankan
saldo(Pelanggan)               Tidak boleh negatif                  Dicetak pesan [gagal], nilai lama dipertahankan
Nominal top up                 Minimal sesuai minimal_topup         Ditolak, saldo tidak berubah
Jumlah item transaksi          Minimal 1                            Ditolak
stok saat transaksi            Tidak boleh melebihi stok            Item tidak jadi ditambahkan
                               yang tersedia                       
saldo saat bayar               Harus cukup untuk total transaksi    Pembayaran ditolak

5. Panduan Pengujian (Main Code)

1.Class Menu
- Bikin 2 objek (kopi_susu langsung lewat konstruktor, matcha lewat classmethod dari_dict)
- Panggil instance method tampilkan_info()
- Panggil static method validasi_kategori() dengan input valid dan tidak valid
- Uji setter stok dengan nilai valid (25) dan tidak valid (-5)
- Panggil class method ubah_nama_toko() dan cek perubahannya berlaku ke semua objek

2.Class Pelanggan
- Bikin 2 objek (andi langsung, siti lewat classmethod daftar_baru)
- Panggil static method validasi_no_hp() dengan input valid dan tidak valid
- Uji top_up() dengan nominal valid dan di bawah minimal (tidak valid)
- Uji setter saldo langsung diisi angka negatif (harus ditolak)

3.Class Transaksi
- Bikin 2 objek transaksi untuk 2 pelanggan berbeda
- Tambah item pesanan yang valid dan yang melebihi stok (harus ditolak)
- Proses pembayaran dan cetak struk
- Panggil class method ubah_pajak() dan cek nilai pajak_persen berubah

Kalau dijalankan, outputnya akan menunjukkan kombinasi pesan [sukses] dan [gagal] yang membuktikan validasi di setter maupun di method lain berjalan sesuai aturan di atas.