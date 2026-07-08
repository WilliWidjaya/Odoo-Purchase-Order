# 📋 Panduan Memulai - Modul Pesanan Pembelian (Purchase Order)

## Selamat Datang! 👋

Dokumentasi ini dirancang untuk membantu Anda menggunakan modul **Pesanan Pembelian (Purchase Order)** di sistem Odoo 18. Modul ini memungkinkan Anda mengelola semua aspek pembelian, dari pembuatan pesanan hingga pelacakan pengiriman.

---

## Apa Itu Pesanan Pembelian?

Pesanan Pembelian (PO) adalah dokumen formal yang digunakan untuk:
- ✅ Memesan barang/jasa dari supplier/vendor
- ✅ Menentukan jumlah, harga, dan syarat pembayaran
- ✅ Melacak riwayat pembelian
- ✅ Mengelola pengiriman barang
- ✅ Menyimpan dokumen pendukung (Invoice, Bill of Lading, dll)

---

## Fitur Utama Modul

### 1. **Pesanan Pembelian (Purchase Order)**
   - Membuat dan mengelola pesanan pembelian
   - Melacak status pesanan (Draft/Finalized)
   - Menyimpan informasi vendor dan pembayaran

### 2. **Detail Item**
   - Menambahkan item/barang yang dipesan
   - Menentukan kuantitas dan harga
   - Menghitung diskon dan pajak otomatis

### 3. **Informasi Pengiriman (Freight)**
   - Mencatat biaya pengiriman
   - Menunjuk ekspedisi/kurir
   - Melacak nomor container dan vessel

### 4. **Lampiran Dokumen**
   - Menyimpan file pendukung (Invoice, BoL, Packing List, dll)
   - Mengorganisir dokumen per pesanan

---

## Alur Kerja Umum

```
1. BUAT PESANAN
   ↓
2. ISI INFORMASI VENDOR
   ↓
3. TAMBAHKAN ITEM YANG DIPESAN
   ↓
4. ISI BIAYA PENGIRIMAN (jika ada)
   ↓
5. LAMPIRKAN DOKUMEN PENDUKUNG
   ↓
6. FINALISASI PESANAN
   ↓
7. PANTAU STATUS PENGIRIMAN
```

---

## Memulai Langkah Demi Langkah

### Langkah 1: Akses Modul
1. Login ke sistem Odoo 18
2. Cari menu **"Purchase Order PT"** atau **"Pesanan Pembelian"** di menu utama
3. Klik untuk membuka modul

### Langkah 2: Buat Pesanan Baru
1. Klik tombol **"Create"** atau **"+ Buat"**
2. Isi formulir dengan informasi dasar

### Langkah 3: Simpan dan Selesaikan
1. Klik **"Save"** untuk menyimpan draft
2. Klik **"Finalize"** untuk menyelesaikan pesanan

---

## Bagian-Bagian Utama Formulir

| Bagian | Fungsi | Wajib Diisi |
|--------|--------|------------|
| **Info Umum** | Nomor PO, nama, status | ✅ Ya |
| **Info Vendor** | Supplier dan kontak | ✅ Ya |
| **Tanggal** | Posting date, due date, dll | ✅ Ya |
| **Pembayaran** | Syarat, kurs, pajak | ✅ Ya |
| **Item** | Barang yang dipesan | ✅ Ya |
| **Pengiriman** | Biaya freight, tujuan | ⚠️ Opsional |
| **Lampiran** | File pendukung | ⚠️ Opsional |

---

## Tips Awal

✨ **Tips Berguna:**
- Simpan draft pesanan sebelum menambahkan item
- Gunakan item code yang konsisten untuk kemudahan tracking
- Perhatikan due date agar tidak melewatkan deadline pembayaran
- Lampirkan invoice dan BoL sebelum finalisasi

⚠️ **Perhatian Penting:**
- Setelah pesanan difinalisasi, beberapa field tidak bisa diubah
- Pastikan data vendor sudah benar sebelum menyimpan
- Double-check perhitungan pajak dan diskon

---

## Navigasi Dokumentasi

Panduan lengkap ini terdiri dari:

1. **00_PANDUAN_MEMULAI.md** ← Anda di sini (Pengenalan umum)
2. **01_MEMBUAT_PESANAN_PEMBELIAN.md** - Panduan detail membuat PO
3. **02_DETAIL_ITEM_PESANAN.md** - Menambah dan mengelola item
4. **03_INFORMASI_PENGIRIMAN.md** - Detail fitur pengiriman
5. **04_LAMPIRAN_DAN_DOKUMEN.md** - Mengelola dokumen pendukung
6. **05_TIPS_DAN_BEST_PRACTICES.md** - Tips dan trik penggunaan
7. **06_REFERENSI_CEPAT.md** - Daftar singkat semua field

---

## Bantuan Lebih Lanjut

Jika Anda memiliki pertanyaan:
- 📖 Lihat dokumentasi lengkap di bagian berikutnya
- 🔍 Cari di bagian **Referensi Cepat**
- 💬 Hubungi tim IT atau administrator Anda

**Selamat menggunakan modul Pesanan Pembelian! 🎉**

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
*Versi: 1.0 | Tanggal: 2026*
