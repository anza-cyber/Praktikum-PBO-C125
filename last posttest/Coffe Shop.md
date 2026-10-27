# Sistem Pendataan Transaksi dan Menu Minuman pada Coffee Shop

Nama  : Rafalia Khanza Taufik
NIM   : 2509106104
Kelas : C25
Pottest Pemrograman Berorientasi Objek (PBO)

## Deskripsi Program

Program Python berbasis console untuk mengelola menu minuman dan mencatat transaksi di sebuah coffee shop. Menu dibagi menjadi tiga jenis (Kopi, Non-Kopi, Blended) yang masing-masing punya cara hitung harga sendiri. Setiap program dijalankan, ada satu baris pengecekan yang membuktikan bahwa abstract class tidak bisa dibuat objeknya.

Fitur:

1. Lihat daftar menu: -> menampilkan semua menu beserta jenis, harga akhir, dan keterangannya.
2. Tambah menu: -> kasir memasukkan nama, harga dasar, dan jenis menu. Data tambahan   (jumlah shot, topping, atau ukuran ml) ditanyakan sesuai jenisnya. Nama menu yang sudah ada (tidak peka huruf besar/kecil) ditolak.
3. Hapus menu: -> menghapus menu dari daftar berdasarkan nomor. Ada konfirmasi (y/n) sebelum dihapus, dan memasukkan 0 membatalkan penghapusan.
4. Buat transaksi: -> memasukkan data pelanggan, memilih menu dan jumlah (boleh beberapa menu dalam satu transaksi), mencetak struk yang memuat rincian harga (harga dasar, biaya topping/shot/ukuran, harga per gelas) beserta total bayar, lalu membayar dengan Tunai atau QRIS. Jika uang tunai kurang, kasir bisa mencoba lagi atau membatalkan transaksi. Setelah lunas, riwayat transaksi dan total pendapatan langsung ditampilkan.

Validasi input yang ada di program:

- Angka tidak boleh negatif atau berisi huruf (`baca_int()`).
- Nama pelanggan harus mengandung huruf (kosong = "Pelanggan"), nama menu dan nama topping juga harus mengandung huruf.
- No HP hanya angka (boleh diawali `+`, boleh ada `-` atau spasi di tengah), panjang 8-16 karakter. Kosong atau `0` berarti tidak ada (disimpan sebagai `-`).
- Jumlah shot minimal 1 dan ukuran Blended minimal 350 ml.

Cara menjalankan (butuh Python 3):

python main.py

File dalam folder ini:

| File | Isi |
|---|---|
| `main.py` | Kode program |
| `README.md` | Laporan ini |
| `class_diagram.png` | Gambar class diagram |
| `screenshot_*.png` | Screenshot output program |

## Aturan Harga Menu

Biaya tambahan di luar harga dasar dihitung oleh method `rincian_tambahan()` di tiap subclass. Harga akhir per gelas dihitung oleh `Menu.hitung_harga()` = harga dasar + jumlah semua biaya tambahan:

| Jenis (subclass) | Atribut unik | Biaya tambahan (`rincian_tambahan()`) |
|---|---|---|
| `Kopi` | `shot` | harga dasar + Rp5.000 untuk setiap tambahan shot (shot pertama sudah termasuk harga dasar) |
| `NonKopi` | `topping` (list) | harga dasar + Rp3.000 untuk setiap topping |
| `Blended` | `ukuran_ml` | harga dasar + Rp4.000 untuk setiap kelipatan 100 ml penuh di atas ukuran standar 350 ml (dibulatkan ke bawah, misalnya 399 ml belum kena biaya tambahan) |

Contoh: Choco Blended harga dasar Rp28.000 dengan ukuran 450 ml menjadi 28.000 + (450 − 350) ÷ 100 × 4.000 = Rp32.000.

Menu awal yang tersedia saat program dibuka:

| Menu | Jenis | Keterangan | Harga akhir |
|---|---|---|---|
| Americano | Kopi | 1 shot | Rp18.000 |
| Cafe Latte | Kopi | 2 shot | Rp27.000 |
| Matcha | Non-Kopi | topping boba | Rp27.000 |
| Strawberry Milk | Non-Kopi | topping Buah Strawberry | Rp23.000 |
| Choco Blended | Blended | 450 ml | Rp32.000 |

## Daftar Kelas

| Kelas | Peran |
|---|---|
| `Menu` | Abstract class untuk semua menu minuman |
| `Kopi`, `NonKopi`, `Blended` | Subclass `Menu` untuk tiap jenis minuman |
| `DaftarMenu` | Menampung kumpulan objek `Menu` (tambah, hapus, tampilkan) |
| `Pelanggan` | Data pelanggan (nama dan no HP) |
| `ItemPesanan` | Satu baris pesanan (menu, jumlah, subtotal) |
| `Transaksi` | Satu transaksi: pelanggan, daftar item, total, dan struk |
| `Tunai`, `QRIS` | Metode pembayaran, masing-masing punya method `bayar()` |

## 1. Class Diagram

![Class Diagram](class_diagram.png)

Keterangan simbol: panah segitiga kosong = pewarisan, panah terbuka = asosiasi, belah ketupat kosong = agregasi, belah ketupat penuh = komposisi. Tanda `#` untuk atribut protected, `-` untuk private, `+` untuk public, dan `*` di belakang method menandakan abstract method. Kelas `Tunai`, `QRIS`, dan fungsi pendukung tidak digambar supaya diagram tetap sederhana.

**Asosiasi** (`Transaksi` → `Pelanggan` dan `ItemPesanan` → `Menu`): `Transaksi` menyimpan referensi ke objek `Pelanggan` (`self.pelanggan`) untuk mencatat siapa yang membeli, dan `ItemPesanan` menyimpan referensi ke `Menu` (`self.menu`). Keduanya hanya menunjuk ke objek yang sudah ada tanpa memiliki atau mengatur hidup-matinya, jadi hubungannya asosiasi.

**Agregasi** (`DaftarMenu` ◇— `Menu`): `DaftarMenu` menampung banyak `Menu` lewat method `tambah()`, tetapi objek `Menu` dibuat di luar lalu dimasukkan. Kalau sebuah menu dihapus dari daftar atau `DaftarMenu`-nya hilang, objek `Menu` tidak ikut hilang (misalnya tetap direferensikan oleh `ItemPesanan` di transaksi lama), jadi hubungannya agregasi, bukan komposisi.

**Komposisi** (`Transaksi` ◆— `ItemPesanan`): `ItemPesanan` dibuat langsung di dalam `Transaksi.tambah_item()` dan tidak punya arti di luar transaksinya. Kalau transaksi hilang, item pesanannya ikut hilang, jadi hubungannya komposisi.

## 2. Abstraksi

- **Abstract class:** `Menu(ABC)` dengan dua `@abstractmethod`, yaitu `rincian_tambahan()` dan `keterangan()`.
- **Subclass yang mengimplementasikan keduanya:** `Kopi`, `NonKopi`, dan `Blended`. Masing-masing memanggil `super().__init__(...)` dan punya atribut unik (`shot`, `topping`, `ukuran_ml`).
- **Method konkret:** `hitung_harga()` dan `tampilkan_info()` di `Menu`, dipakai bersama oleh semua subclass. Keduanya memanggil `rincian_tambahan()` dan `keterangan()` milik masing-masing subclass.
- **Atribut protected/private:** `_nama` (protected) dan `__harga_dasar` (private, diakses lewat property `harga_dasar`).
- **Bukti abstract class tidak bisa diinstansiasi:** fungsi `cek_abstraksi()` dijalankan otomatis saat program dibuka. Fungsi ini mencoba membuat `Menu("tes", 0)` di dalam `try-except TypeError`, dan hasilnya tampil di baris `[Cek Abstraksi]` pada screenshot menu utama.

## 3. Polimorfisme

- **Via pewarisan:** `rincian_tambahan()` dan `keterangan()` di-override oleh `Kopi`, `NonKopi`, dan `Blended` dengan perilaku berbeda (lihat tabel aturan harga di atas). Dipanggil lewat satu loop di `DaftarMenu.tampilkan()` yang berisi objek dari tiga subclass berbeda: `for i, m in enumerate(self._daftar, start=1): m.tampilkan_info()`.
- **Duck typing:** `Tunai` dan `QRIS` tidak punya hubungan pewarisan, tetapi sama-sama punya method `bayar()`. Keduanya dipanggil lewat satu fungsi yang sama, `proses_bayar(metode, total)`.
- **Operator overloading:** magic method yang dipakai langsung di program:
  - `Transaksi.__lt__`: dipakai `sorted()` untuk mengurutkan riwayat dari total terbesar.
  - `Transaksi.__len__`: jumlah item dalam transaksi, lewat `len(transaksi)`.
  - `Transaksi.__str__`: baris ringkasan transaksi di riwayat.
  - `DaftarMenu.__len__` dan `DaftarMenu.__getitem__`: `len(daftar)` dan `daftar[nomor - 1]` saat memilih menu.
  - `Pelanggan.__str__`: nama dan no HP di struk.
  - Magic method lain yang sudah didefinisikan tetapi belum dipanggil langsung di alur program: `Pelanggan.__eq__` (membandingkan pelanggan lewat no HP) dan `DaftarMenu.__iter__` (agar daftar menu bisa di-loop).
- **Tanpa anti-pattern:** tidak ada rantai `if/elif` yang mengecek `type()` atau string jenis untuk membedakan perilaku objek. Jenis menu dipilih lewat dictionary `JENIS_MENU`, jenis pembayaran lewat `METODE_BAYAR`, dan tiap kelas punya method `dari_input()` sendiri untuk menanyakan data tambahannya.

## 4. Screenshot Output

Menu utama, termasuk bukti abstract class tidak bisa diinstansiasi (baris `[Cek Abstraksi] TypeError: ...` di bagian atas):

1. Tampilan Awal Menu Coffe Shop.png
2. Tambah Menu.png
3. Hapus Menu.png
4. Buat Transaksi.png
5. Keluar.png

## 5. SOLID

- **OCP (Open/Closed):** jenis minuman baru cukup dibuat sebagai subclass `Menu` dan didaftarkan di `JENIS_MENU` (ditambah satu baris teks pilihan jenis di `tambah_menu()`). Kelas `DaftarMenu`, `ItemPesanan`, dan `Transaksi` tidak perlu diubah karena hanya memanggil `hitung_harga()`, `rincian_tambahan()`, dan `tampilkan_info()`.
- **DIP (Dependency Inversion):** `ItemPesanan` bergantung pada abstraksi `Menu`, bukan pada `Kopi`, `NonKopi`, atau `Blended` secara langsung. Selain itu `proses_bayar()` menerima objek pembayaran dari luar lewat parameter, jadi tidak terikat ke `Tunai` atau `QRIS` saja.