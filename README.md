Nama    : M. Rezky Syahputra
NPM     : 2506614006
Kelas   : PBP D

Deklarasi AI: Saya menggunakan Gemini untuk membantu menyesuaikan struktur HTML semantik, meminta solusi bug tata letak gambar, dan memberikan umpan balik tata bahasa untuk deskripsi bio dan poin-poin pengalaman.

### Tugas 1
1. Ya, saya menggunakan elemen semantik HTML5 seperti <header>, <main>, <section>, <nav>, dan <footer> dalam membuat dokumen HTML. Hal tersebut membuat hirarki kode HTML menjadi rapi, bersih, dan mudah dikelola dibanding hanya menggunakan pembungkus <div> generik bertingkat. Selain itu, pengguna berkebutuhan khusus dapat dengan mudah menavigasi bagian utama portofolio. Namun, saya belum menggunakan <aside> dan <article> dalam dokumen HTML saya.

2. Salah satu tantangannya adalah ketika menyesuaikan pada bagian experience karena harus menjaga gambar dan deskripsi teks tetap sejajar dan tidak tumpang-tindih, sambil memastikan header (judul dan rentang tanggal) tetap membentang penuh dengan tanggal yang di bagian kanan atas.
Saat mengevaluasi elemen mana yang perlu diubah posisinya ketika berpindah dari tampilan desktop ke mobile, saya memprioritaskan keterbacaan teks dan kenyamanan alur scrolling pengguna. Melalui penerapan Media Query (@media (max-width: 600px)), struktur dua kolom pada .exp-body dan .hero-grid secara otomatis dilebur menjadi satu kolom vertikal. Foto dan teks yang tadinya sejajar di samping, otomatis turun berurutan ke bawah. Dengan begitu, pengguna di HP bisa membaca informasi dan scrolling dengan lebih nyaman.

3. Batasan utama yang saya rasakan pada web statis ini adalah kepraktisan dalam memperbarui isi portofolio. Meskipun konten di web saya saat ini belum terlalu banyak, setiap ada penambahan kecil—seperti menambah satu keterampilan atau merapikan deskripsi pengalaman—saya tetap harus mengedit file HTML secara manual. Web ini juga masih sebatas tampilan pasif, sehingga belum ada fitur interaktif bagi pengunjung. Karena batasan tersebut, pada iterasi selanjutnya saya ingin menghubungkan portofolio ini dengan database lewat Django ORM agar tambah/edit data bisa dilakukan lewat Django Admin tanpa sentuh kode HTML lagi. 