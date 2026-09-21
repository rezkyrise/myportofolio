Nama    : M. Rezky Syahputra
NPM     : 2506614006
Kelas   : PBP D

Deklarasi AI: Saya menggunakan Gemini untuk membantu menyesuaikan struktur HTML semantik, meminta solusi bug tata letak gambar, dan memberikan umpan balik tata bahasa untuk deskripsi bio dan poin-poin pengalaman.

### Tugas 1
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