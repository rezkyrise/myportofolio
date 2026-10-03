- Nama    : M. Rezky Syahputra
- NPM     : 2506614006
- Kelas   : PBP D

### Cara menjalankan
 
```bash
git clone <url-repositori>
cd myportofolio
python -m venv env
env\Scripts\activate            # Windows. macOS/Linux: source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Tugas 1
Deklarasi AI: Saya menggunakan Gemini untuk membantu menyesuaikan struktur HTML semantik, meminta solusi bug tata letak gambar, dan memberikan umpan balik tata bahasa untuk deskripsi bio dan poin-poin pengalaman.

1. Ya, saya menggunakan elemen semantik HTML5 seperti header, main, section, nav, dan footer dalam membuat dokumen HTML. Hal tersebut membuat hirarki kode HTML menjadi rapi, bersih, dan mudah dikelola dibanding hanya menggunakan pembungkus div generik bertingkat. Selain itu, pengguna berkebutuhan khusus dapat dengan mudah menavigasi bagian utama portofolio. Namun, saya belum menggunakan aside dan article dalam dokumen HTML saya.

2. Salah satu tantangannya adalah ketika menyesuaikan pada bagian experience karena harus menjaga gambar dan deskripsi teks tetap sejajar dan tidak tumpang-tindih, sambil memastikan header (judul dan rentang tanggal) tetap membentang penuh dengan tanggal yang di bagian kanan atas.
Saat mengevaluasi elemen mana yang perlu diubah posisinya ketika berpindah dari tampilan desktop ke mobile, saya memprioritaskan keterbacaan teks dan kenyamanan alur scrolling pengguna. Melalui penerapan Media Query (@media (max-width: 600px)), struktur dua kolom pada .exp-body dan .hero-grid secara otomatis dilebur menjadi satu kolom vertikal. Foto dan teks yang tadinya sejajar di samping, otomatis turun berurutan ke bawah. Dengan begitu, pengguna di HP bisa membaca informasi dan scrolling dengan lebih nyaman.

3. Batasan utama yang saya rasakan pada web statis ini adalah kepraktisan dalam memperbarui isi portofolio. Meskipun konten di web saya saat ini belum terlalu banyak, setiap ada penambahan kecil—seperti menambah satu keterampilan atau merapikan deskripsi pengalaman—saya tetap harus mengedit file HTML secara manual. Web ini juga masih sebatas tampilan pasif, sehingga belum ada fitur interaktif bagi pengunjung. Karena batasan tersebut, pada iterasi selanjutnya saya ingin menghubungkan portofolio ini dengan database lewat Django ORM agar tambah/edit data bisa dilakukan lewat Django Admin tanpa sentuh kode HTML lagi. 


### Tugas 2
Deklarasi AI: 
Dalam pengerjaan tugas ini, saya menggunakan bantuan Claude AI untuk:
Membantu menyusun ulang tampilan (styling CSS) pada halaman Experience dan Skill serta membantu memahami lebih dalam terkait penggunaan MVT
Seluruh kode yang dihasilkan telah saya pahami, uji jalankan sendiri (python manage.py test, python manage.py runserver), dan sesuaikan dengan kebutuhan proyek saya. 

1. Ketika user membuka URL halaman portofolio baru di browser, terjadi pengiriman request HTTP GET ke server. Permintaan ini pertama kali diterima oleh urls.py tingkat proyek, lalu meneruskan alur URL tersebut ke urls.py tingkat aplikasi menggunakan fungsi include(). Selanjutnya, urls.py aplikasi mencocokkan path URL yang spesifik dan mengarahkannya ke fungsi view yang sesuai. Setelah dipanggil, views.py bertindak sebagai pengendali logika yang meminta data portofolio dari models.py. Model bertindak sebagai penghubung ke database SQL yang mengambil data melalui kueri Django ORM lalu mengembalikannya ke view dalam bentuk objek Python. View kemudian membungkus data tersebut ke dalam sebuah context dictionary dan memanggil fungsi render() untuk menyuntikkan data ke dalam berkas template HTML menggunakan Django Template Language (DTL). Terakhir, Django menghasilkan HTML lengkap dari hasil penggabungan template + data, lalu mengembalikannya sebagai response ke browser. Browser menerima HTML tersebut dan menampilkannya sebagai halaman web yang dilihat pengguna.

2. Apabila data ditulis langsung di HTML template, setiap kali ada penambahan, pengubahan, atau penghapusan satu data, file HTML harus diedit secara manual, lalu deploy ulang seluruh aplikasi. Dengan menyimpan data di model (database), kita dapat menambah/ubah/hapus data lewat halaman admin Django (/admin/) atau sistem CRUD tanpa menyentuh atau merusak kode HTML. Data yang sama bisa dipakai di banyak tempat tanpa perlu menyalin-nyalin teks yang sama di banyak file HTML. Selain itu, pengembangannya juga jadi lebih mudah karena kode HTML cukup ditulis sekali menggunakan perulangan DTL (contoh: {% for item in portfolios %}).

3. Makemigrations berfungsi membuat rencana perubahan (file migrasi) berdasarkan perbedaan models.py sekarang dengan riwayat migrasi sebelumnya. Ini tidak mengubah database, cuma menghasilkan file Python yang berisi instruksi "apa yang harus diubah", sedangkan migrate benar-benar menerapkan rencana perubahan dari file migrasi tersebut ke database (misalnya membuat tabel baru, menambah kolom, dll).
Contoh: Ketika menambahkan field organization ke model Experience yang sudah ada, hal ini juga menjalankan makemigrations (menghasilkan 0004_experience_organization.py) lalu migrate (menerapkannya, menambahkan kolom baru organization ke tabel Experience yang sudah ada).

### Tugas 3
Deklarasi AI: 
Dalam pengerjaan tugas ini, saya menggunakan bantuan Claude (Anthropic) untuk:
Membantu memahami dan mengadaptasi materi Tutorial 3 (yang menggunakan model Project) ke model portofolio saya sendiri (Skill dan Experience), membantu debugging saat menemui error (NameError, TemplateDoesNotExist, error validasi format tanggal pada DateField, dsb), serta membantu menyusun ulang CSS agar konsisten antara komponen Skill dan Experience.
Seluruh kode yang dihasilkan telah saya pahami, uji jalankan sendiri, dan disesuaikan dengan kebutuhan proyek saya. 

1. Jika membuat form HTML manual, kita harus menulis sendiri semua validasi dan menulis kode utk memasukkan data ke model dan menyimpan ke database. Adanya ModelForm memudahkan kita karena otomatis menghasilkan field, widget, dan validasi berdasarkan struktur model yang sudah kita definisikan sehingga tidak perlu menulis ulang validasi dan proses penyimpanan data ke database secara manual. Field seperti category dan proficiency yang punya choices di model otomatis dirender sebagai dropdown, dan form.save() langsung menangani proses insert maupun update ke database. 
{% csrf_token %} wajib ditambahkan untuk mencegah serangan Cross-Site Request Forgery, yaitu ketika situs jahat mengelabui browser korban untuk mengirim request ke aplikasi kita tanpa sepengetahuan korban. Token unik ini digenerate server dan dicocokkan saat form disubmit sehingga request yang tidak berasal dari form asli aplikasi kita akan ditolak.

2. JSON lebih disukai dibanding XML dalam pengembangan web modern karena strukturnya lebih ringkas dan tidak memerlukan tag pembuka-penutup seperti XML sehingga ukuran datanya lebih kecil dan lebih efisien dikirim melalui jaringan. Selain itu, JSON bisa langsung diparsing oleh frontend tanpa parser tambahan seperti yang dibutuhkan XML. JSON juga lebih mudah dibaca manusia dan lebih didukung secara luas oleh ekosistem web modern.

3. Ketika view seperti get_skill_json dipanggil, alurnya dimulai dari query ke database menggunakan Skill.objects.all() yang menghasilkan QuerySet berisi object-object Python. Karena HTTP hanya dapat mengirim data dalam bentuk teks atau bytes, object model Django tersebut perlu diubah dulu melalui proses serialization menggunakan serializers.serialize("json", skills) menjadi string berformat JSON, sebelum dibungkus ke dalam HttpResponse dan dikirim ke client. 
Proses serialization ini penting karena object Python tidak bisa langsung dikirim melalui jaringan sehingga perlu diubah dulu ke format JSON yang berupa teks agar bisa dikirim lewat HTTP dan dibaca oleh sistem apa pun, baik itu JavaScript, aplikasi mobile, maupun bahasa pemrograman lain.

### Tugas 4
Deklarasi AI: 
Dalam pengerjaan tugas ini, saya menggunakan Claude (Anthropic) untuk membantu menelusuri error yang saya temui, mengadaptasi skrip Selenium dari tutorial, dan mengecek kesesuaian pengerjaan kode saya dengan tutorial.

Strategi prompting. Saya memberi konteks terlebih dahulu, kemudian mengecek hasil adaptasi dari contoh tutorial ke model saya sendiri. Pekerjaan dipecah per fitur kecil (autentikasi, cookie, otorisasi, star), dan setiap langkah saya jalankan sebelum lanjut. Saat ada masalah, saya menempelkan kode, traceback, atau tangkapan layar yang relevan agar AI bekerja dari kondisi berkas saya yang sebenarnya, bukan dari asumsi.

Fitur di luar instruksi minimum
 
- Star diterapkan ke dua model.
- Badge peran (Owner / Editor / User) di navbar, disediakan lewat context processor.
- Halaman 403 kustom (`templates/403.html`) yang menampilkan peran pengguna saat ini.
- Skrip Selenium end-to-end (`test_e2e.py`).

### Tugas 5
Deklarasi AI: 
Dalam pengerjaan tugas ini, saya menggunakan Claude (Anthropic) untuk membantu menelusuri error yang saya temui, membantu memahami pola tutorial, dan mengecek kesesuaian pengerjaan kode saya dengan tutorial.

Strategi prompting. Saya memberi konteks terlebih dahulu, kemudian mengecek hasil adaptasi dari contoh tutorial ke model saya sendiri. Pekerjaan dipecah per fitur kecil (autentikasi, cookie, otorisasi, star), dan setiap langkah saya jalankan sebelum lanjut. Saat ada masalah, saya menempelkan kode, traceback, atau tangkapan layar yang relevan agar AI bekerja dari kondisi berkas saya yang sebenarnya, bukan dari asumsi.

Implementasi minggu ini:
- Daftar dimuat lewat `fetch()` dari endpoint JSON, dengan state loading, kosong, dan error
- Pencarian dengan debouncing 300 ms
- Modal tambah data, dikirim lewat AJAX (status 201, 400, 403) dengan CSRF
- Notifikasi toast untuk sukses dan gagal, termasuk pesan validasi server
- Perlindungan XSS: `escapeHtml` dan `strip_tags`

Fitur ekstra:
- Star tanpa reload halaman: tombol, jumlah, dan tooltip langsung diperbarui tanpa memuat ulang. Pencarian dan filter yang aktif tetap terjaga.

1. Debouncing adalah teknik menunda eksekusi sebuah fungsi sampai ada jeda waktu tertentu tanpa event baru. Selama event masih terus terjadi, timer sebelumnya dibatalkan dan dimulai lagi dari awal, sehingga fungsi hanya berjalan sekali setelah event berhenti. 
Pada fitur pencarian yang menggunakan AJAX, tanpa debouncing setiap ketikan memicu satu request ke server. Akibatnya beban server dan penggunaan bandwidth meningkat, dan daftar terus dirender ulang sehingga tampilan berkedip. Selain itu, respons dari request lama bisa tiba terlambat lalu menimpa hasil yang lebih baru.

2. `await` digunakan di dalam `async function` untuk menunggu sebuah Promise selesai diproses sebelum eksekusi lanjut ke baris berikutnya. Fungsi `fetch()` tidak langsung mengembalikan data, melainkan sebuah Promise yang baru terisi objek `Response` setelah server membalas. Dengan `await`, eksekusi fungsi dijeda pada baris itu sampai balasan diterima, lalu hasilnya dapat dipakai seperti nilai biasa. Prosesnya sendiri tetap asinkron, jadi browser tidak membeku dan bagian halaman lain tetap bisa berjalan selama menunggu.
Jika `await` tidak digunakan, variabel `response` hanya berisi Promise yang masih pending, bukan objek `Response`. Akibatnya `response.ok` bernilai `undefined` sehingga kode menganggap permintaan gagal, dan `response.json()` memunculkan error karena Promise tidak memiliki method tersebut. Baris-baris berikutnya juga langsung berjalan sebelum data tiba. Pada daftar Experience, misalnya, `forEach` akan dijalankan pada data yang belum ada, sehingga kartu tidak tampil atau halaman menampilkan kondisi error.

3. XSS (Cross-Site Scripting) adalah serangan ketika penyerang berhasil menyisipkan kode JavaScript miliknya ke halaman web, yang kemudian dijalankan di browser pengguna lain. Salah satu jenisnya adalah stored XSS, yaitu ketika kode berbahaya disimpan di database, lalu dijalankan setiap kali data itu ditampilkan, termasuk di browser pengunjung yang tidak login. Dampaknya serius karena kode yang tersisip berjalan di dalam halaman kita sendiri. Kode itu bisa membaca cookie `csrftoken` dan mengirim request atas nama korban sehingga perlindungan CSRF tidak lagi efektif.
Data yang ditampilkan lewat template Django relatif aman karena Django melakukan auto-escaping pada setiap `{{ variabel }}`. Karakter seperti `<` dan `>` diubah menjadi `&lt;` dan `&gt;`, sehingga browser menampilkannya sebagai teks biasa, bukan sebagai tag HTML. Pada AJAX, perlindungan itu hilang. Data JSON saya sisipkan sendiri ke dalam template literal, lalu dipasang ke halaman lewat `innerHTML`. Tidak ada lagi Django yang melakukan escaping sehingga browser menafsirkan setiap tag di dalam data sebagai HTML sungguhan. Contohnya, judul `<img src="x" onerror="alert('XSS!')">` akan menjalankan `alert` begitu gambar gagal dimuat.


