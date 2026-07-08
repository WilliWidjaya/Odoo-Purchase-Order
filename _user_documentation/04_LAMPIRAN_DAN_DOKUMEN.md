# 📎 Panduan Lampiran dan Dokumen (Attachments)

## Pengenalan

Bagian ini menjelaskan cara menambahkan dan mengelola lampiran dokumen dalam pesanan pembelian. Lampiran adalah file pendukung seperti Invoice, Bill of Lading, Packing List, Certificate, dll.

---

## Mengapa Lampiran Penting?

✅ **Manfaat Lampiran:**
- 📄 Menyimpan bukti transaksi (Invoice, Receipt)
- 📦 Tracking pengiriman (BoL, Packing List)
- ✅ Verifikasi kualitas (Certificate, Test Report)
- 🔐 Compliance dan audit trail
- 📊 Dokumentasi lengkap per pesanan
- ⚖️ Referensi jika ada dispute/claim

---

## 📋 Jenis-Jenis Dokumen yang Bisa Dilampirkan

### Dokumen Transaksi
| Dokumen | Deskripsi | Contoh |
|---------|-----------|--------|
| **Quotation/Penawaran** | Penawaran harga dari supplier | Quotation dari PT XYZ |
| **Invoice** | Faktur pembayaran dari supplier | Invoice #INV-001-2025 |
| **PO Confirmation** | Konfirmasi pesanan dari supplier | Confirmed PO |
| **Receipt** | Bukti penerimaan barang | GRN-2025-001 |

### Dokumen Logistik
| Dokumen | Deskripsi | Contoh |
|---------|-----------|--------|
| **Bill of Lading (BoL)** | Dokumen pengiriman laut | Master B/L CONT-001 |
| **Air Waybill (AWB)** | Dokumen pengiriman udara | AWB GA-501 |
| **Packing List** | Daftar barang & packaging | Packing List PL-001 |
| **Shipping Document** | Dokumen pengiriman umum | Delivery Note |

### Dokumen Kualitas & Compliance
| Dokumen | Deskripsi | Contoh |
|---------|-----------|--------|
| **Certificate of Origin** | Sertifikat asal barang | CoO untuk import |
| **Quality Certificate** | Sertifikat kualitas | Test report, CoC |
| **Compliance Doc** | Dokumen kepatuhan | Safety cert, compliance letter |
| **Insurance Doc** | Bukti asuransi pengiriman | Insurance policy |

### Dokumen Lainnya
| Dokumen | Deskripsi | Contoh |
|---------|-----------|--------|
| **Specification Sheet** | Spek teknis barang | Product datasheet |
| **Technical Drawing** | Gambar teknis/blueprint | CAD drawing |
| **Email/Correspondence** | Email penting dari supplier | Supplier confirmation |
| **Photos** | Foto barang/packaging | Quality verification photos |

---

## ➕ Menambahkan Lampiran

### Metode 1: Upload File via Tab Lampiran

#### Langkah-Langkah:

1. **Buka Pesanan Pembelian**
   - Buka PO yang sudah ada atau buat PO baru
   
2. **Akses Tab Lampiran**
   - Scroll ke bawah
   - Cari tab **"Lampiran"** atau **"Attachments"**
   
3. **Tambah File Baru**
   - Klik tombol **[+ Tambah]** atau **[+ Add Attachment]**
   - Atau double-click area kosong

4. **Upload File**
   - Jendela file browser akan terbuka
   - Pilih file yang ingin di-upload
   - Klik **"Open"** atau **"Pilih"**

5. **Verifikasi File**
   - File akan tampil di tabel lampiran
   - Sistem otomatis catat nama file dan ukuran

---

## 📝 Informasi Lampiran

Setiap lampiran memiliki informasi berikut:

| Kolom | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Attachment** | File yang di-upload | invoice.pdf | ✅ Ya |
| **File Name** | Nama file | Inv-2025-001 | ⚠️ Opsional |
| **File Size** | Ukuran file | 2.5 MB | 🔄 Otomatis |
| **File Type** | Tipe file | PDF | 🔄 Otomatis |

### 1. Attachment (File Dokumen)

| Field | Deskripsi | Wajib? |
|-------|-----------|--------|
| **Attachment** | File yang di-upload (binary) | ✅ Ya |

**Tipe File yang Didukung:**
```
Dokumen: .pdf, .doc, .docx, .xls, .xlsx, .txt, .csv
Gambar: .jpg, .jpeg, .png, .gif, .bmp
Lainnya: .zip, .rar, .7z
```

**Batasan Ukuran:**
- Biasanya max 25-50 MB per file
- Untuk file besar, compress terlebih dahulu
- Atau hubungi admin jika perlu upload file besar

### 2. File Name (Nama File)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **File Name** | Nama deskriptif untuk file | Invoice Vendor XYZ | ⚠️ Opsional |

**Cara Isi:**
- Beri nama yang deskriptif
- Memudahkan pencarian nanti
- Contoh: "Invoice-PT-ABC-2025", "BoL-Container-001"

**Tips Penamaan File:**
```
❌ BURUK:
- "file1.pdf"
- "dokumen.pdf"
- "scan1.jpg"

✅ BAIK:
- "Invoice-PT-ABC-Jan-2025.pdf"
- "BoL-Container-CONT-001.pdf"
- "Quality-Certificate-Batch-A.pdf"
- "Packing-List-Shipment-001.pdf"
```

### 3. File Size (Ukuran File)

| Field | Deskripsi | Contoh | Sifat |
|-------|-----------|--------|-------|
| **File Size** | Ukuran file dalam MB/KB | 2.5 MB | 🔄 Otomatis |

**Otomatis terisi dari sistem**

### 4. File Type (Jenis File)

| Field | Deskripsi | Contoh | Sifat |
|-------|-----------|--------|-------|
| **File Type** | Ekstensi/jenis file | PDF | 🔄 Otomatis |

**Otomatis terisi dari sistem**

---

## 📊 Mengelola Lampiran

### Melihat File
1. Klik row lampiran di tabel
2. File akan preview atau download otomatis
3. Atau klik icon preview/eye jika tersedia

### Mengunduh File
1. Klik row lampiran
2. Klik tombol **[Download]** atau icon download
3. File akan tersimpan ke komputer Anda

### Menghapus Lampiran
1. Klik row lampiran yang ingin dihapus
2. Klik icon **Delete** (🗑️) atau **[Hapus]**
3. Konfirmasi penghapusan
4. File akan dihapus dari sistem

### Mengedit Nama File
1. Klik row lampiran
2. Edit field **"File Name"**
3. Klik Save
4. Nama akan diperbarui

---

## 📝 Contoh Pengisian Lampiran

### Scenario 1: Import Kayu dari China

```
Lampiran 1:
- Attachment: quotation_china_wood.pdf
- File Name: Quotation PT ABC China - Kayu Jati Grade A
- File Size: 1.2 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 2:
- Attachment: invoice_ABC_2025_001.pdf
- File Name: Invoice PT ABC - Inv #2025-001
- File Size: 0.8 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 3:
- Attachment: bol_container_TCLU123.pdf
- File Name: Bill of Lading - Container TCLU1234567
- File Size: 2.1 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 4:
- Attachment: packing_list_shipment_001.pdf
- File Name: Packing List - Shipment 001
- File Size: 0.5 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 5:
- Attachment: quality_certificate_batch_A.pdf
- File Name: Quality Certificate - Batch A
- File Size: 1.5 MB (otomatis)
- File Type: PDF (otomatis)
```

### Scenario 2: Pembelian Spare Parts Lokal

```
Lampiran 1:
- Attachment: quotation_spare_parts.pdf
- File Name: Quotation Supplier Lokal - Bearing SKF
- File Size: 0.8 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 2:
- Attachment: invoice_sp_2025_020.pdf
- File Name: Invoice Spare Parts - Inv #2025-020
- File Size: 0.6 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 3:
- Attachment: delivery_note_021.pdf
- File Name: Delivery Note - DN #021
- File Size: 0.4 MB (otomatis)
- File Type: PDF (otomatis)

Lampiran 4:
- Attachment: test_report_bearing.pdf
- File Name: Test Report - Bearing SKF 6204-2Z
- File Size: 1.2 MB (otomatis)
- File Type: PDF (otomatis)
```

---

## 🔍 Melacak Lampiran

### Jumlah Lampiran

| Field | Deskripsi | Contoh | Sifat |
|-------|-----------|--------|-------|
| **Attachment Count** | Jumlah total file yang dilampirkan | 5 | 🔄 Otomatis |

**Fitur:**
- Sistem otomatis menghitung jumlah file
- Tampil di bagian atas atau di field khusus
- Memudahkan audit: cek berapa banyak dokumen per PO

---

## 📋 Dokumen yang WAJIB Dilampirkan

Berdasarkan jenis transaksi, dokumen berikut sebaiknya dilampirkan:

### Untuk Semua PO:
- ✅ Quotation/Penawaran dari supplier
- ✅ PO Confirmation (jika ada)

### Untuk Import/Pengiriman Luar:
- ✅ Invoice dari supplier
- ✅ Bill of Lading (BoL)
- ✅ Packing List
- ✅ Certificate of Origin (jika ada)

### Untuk Compliance:
- ✅ Quality Certificate/Test Report
- ✅ Insurance Document
- ✅ Safety Certificate (jika produk tertentu)

### Untuk Claim/Dispute:
- ✅ Email correspondence
- ✅ Photos of damage (jika ada kerusakan)
- ✅ Proof of damage report

---

## 💡 Tips Manajemen Dokumen

### ✅ Praktik Terbaik:
- ✅ Upload dokumen sebelum finalisasi PO
- ✅ Gunakan nama file yang deskriptif
- ✅ Organize dokumen sesuai jenis
- ✅ Simpan dokumen original di arsip fisik
- ✅ Backup dokumen penting secara berkala

### ❌ Yang Perlu Dihindari:
- ❌ Jangan upload file yang sudah expired
- ❌ Jangan gunakan nama file yang tidak jelas
- ❌ Jangan upload file dengan virus
- ❌ Jangan hapus dokumen penting setelah finalize
- ❌ Jangan percaya hanya pada file digital (backup fisik juga)

---

## 🔐 Keamanan dan Backup Dokumen

### Backup Dokumen:
- 📁 Sistem biasanya auto-backup dokumen
- 💾 Tanya admin tentang backup schedule
- 🗂️ Simpan copy di local server/NAS juga
- 📋 Cetak dokumen penting untuk arsip fisik

### Akses dan Keamanan:
- 🔒 Hanya pengguna authorized yang bisa akses
- 🔐 Jangan share password akun Anda
- 📝 Audit trail tersimpan (siapa upload, kapan)

---

## ⚠️ Troubleshooting

| Masalah | Penyebab | Solusi |
|--------|---------|--------|
| File tidak bisa di-upload | File terlalu besar | Compress file atau contact admin |
| Upload terputus | Koneksi internet lemah | Coba lagi dengan koneksi lebih baik |
| File tidak tampil | Error sistem | Refresh halaman atau login ulang |
| File tidak bisa di-download | File sudah dihapus | Hubungi admin untuk recovery |
| File corrupted | Error saat upload | Upload ulang file yang baru |

---

## 🔗 Langkah Berikutnya

1. **Tips & Best Practices** → Baca: 05_TIPS_DAN_BEST_PRACTICES.md
2. **Referensi Cepat** → Baca: 06_REFERENSI_CEPAT.md
3. **Finalisasi Pesanan** → Kembali ke: 01_MEMBUAT_PESANAN_PEMBELIAN.md

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
