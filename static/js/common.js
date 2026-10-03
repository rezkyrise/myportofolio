// Membaca nilai cookie, dipakai untuk token CSRF
function getCookie(name) {
    const match = document.cookie.split(';').map(c => c.trim())
        .find(c => c.startsWith(name + '='));
    return match ? decodeURIComponent(match.substring(name.length + 1)) : null;
}

// Mengubah karakter khusus HTML menjadi entity agar ditampilkan sebagai teks
function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

// Mengirim toggle star lewat AJAX dan memperbarui tombol; mengembalikan hasil JSON atau null
async function toggleStar(form) {
    const button = form.querySelector('.button-star');
    button.disabled = true;
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Accept': 'application/json' },
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok) {
            showToast('Gagal memberi star', result.message || `Terjadi kesalahan (status ${response.status}).`, 'error');
            return null;
        }
        button.classList.toggle('is-starred', result.is_starred);
        button.querySelector('.star-label').textContent = result.is_starred ? 'Unstar' : 'Star';
        button.querySelector('.star-count').textContent = result.star_count;
        // Mengisi properti title tidak menafsirkan HTML, jadi aman tanpa escapeHtml
        button.title = result.star_count > 0
            ? `Dibintangi oleh ${result.starred_by_names}`
            : 'Jadilah yang pertama memberi star';
        return result;
    } catch (error) {
        console.error('Error toggling star:', error);
        showToast('Gagal memberi star', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
        return null;
    } finally {
        button.disabled = false;
    }
}