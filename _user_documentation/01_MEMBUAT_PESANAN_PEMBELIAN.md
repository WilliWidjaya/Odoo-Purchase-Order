# 📝 Panduan Membuat Pesanan Pembelian (Purchase Order)

## Pengenalan

Halaman ini menjelaskan langkah demi langkah cara membuat pesanan pembelian baru di sistem. Ikuti panduan ini untuk membuat PO yang lengkap dan akurat.

---

## Memulai: Buat Pesanan Baru

### 1. Akses Formulir Pembuatan PO

```
Menu Utama → Pesanan Pembelian → Tombol [+ Create/Buat]
```

Anda akan melihat formulir kosong dengan beberapa tab:
- **Info Umum** (General Information)
- **Vendor** (Supplier Information)
- **Pembayaran** (Payment)
- **Item Pesanan** (Order Items)
- **Pengiriman** (Freight/Shipping)
- **Lampiran** (Attachments)

---

## 📋 Tab 1: INFORMASI UMUM (General Information)

### A. Nomor Pesanan (Purchase Order Number)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **PO Number** | Nomor unik untuk pesanan ini | PO-2025-001 | ✅ Ya |

**Cara Isi:**
- Gunakan format konsisten (contoh: PO-TAHUN-NOMOR URUT)
- Pastikan nomor tidak duplikat
- Beberapa sistem bisa auto-generate nomor

```
Contoh nomor PO yang baik:
- PO-2025-0001 (format: PO-TAHUN-NOMOR)
- PO/001/2025 (format: PO/NOMOR/TAHUN)
- POJAN-0001 (format: PO-BULAN-NOMOR)
```

### B. Nama Pesanan (Name)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Name** | Deskripsi singkat pesanan | Pembelian Kayu Jati | ✅ Ya |

**Cara Isi:**
- Berikan deskripsi jelas tentang apa yang dipesan
- Gunakan nama singkat (max 75 karakter)
- Contoh: "Pembelian Bahan Baku Produksi", "Import Spare Parts"

### C. Status Pesanan (Status)

| Field | Deskripsi | Pilihan | Wajib? |
|-------|-----------|---------|--------|
| **Status** | Status saat ini pesanan | Draft / Finalized | ✅ Ya |

**Penjelasan Status:**
- **Draft** = Pesanan masih dalam tahap persiapan, bisa diubah
- **Finalized** = Pesanan sudah final, pengiriman sedang diproses

---

## 👥 Tab 2: INFORMASI VENDOR (Vendor Information)

Informasi ini sangat penting karena menjadi tujuan pesanan Anda.

### A. Vendor/Supplier

| Field | Deskripsi | Wajib? |
|-------|-----------|--------|
| **Vendor** | Nama supplier yang dipilih dari daftar | ✅ Ya |

**Cara Isi:**
1. Klik field **Vendor**
2. Cari nama supplier (ketik namanya)
3. Pilih dari daftar yang muncul
4. Jika supplier belum ada, hubungi administrator untuk menambahnya

### B. Nomor Referensi Vendor (Vendor Ref. No)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Vendor Ref. No** | Nomor referensi dari pihak vendor | VND-ABC-2025-100 | ⚠️ Opsional |

**Cara Isi:**
- Isi jika vendor memberikan nomor referensi khusus
- Gunakan nomor yang diberikan supplier
- Contoh: Invoice number dari vendor, quotation number, dll

### C. Kontak Vendor (Contact Person)

| Field | Deskripsi | Wajib? |
|-------|-----------|--------|
| **Contact Person** | Orang yang bisa dihubungi di pihak vendor | ⚠️ Opsional |

**Cara Isi:**
1. Klik field **Contact Person**
2. Pilih kontak yang sudah terdaftar
3. Jika belum ada, hubungi IT untuk menambahnya
4. Berguna untuk komunikasi langsung dengan vendor

---

## 📅 Tab 3: TANGGAL-TANGGALAN (Dates)

### Penjelasan Setiap Tanggal

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Posting Date** | Tanggal pembuatan PO | 15 Jan 2025 | ✅ Ya |
| **Payment Date** | Tanggal pembayaran dilakukan | 25 Jan 2025 | ⚠️ Opsional |
| **Due Date** | Batas akhir pembayaran | 31 Jan 2025 | ⚠️ Opsional |
| **STA Date** | Tanggal barang sampai (Surat Tanda Awal) | 20 Jan 2025 | ⚠️ Opsional |

**Panduan Pengisian:**

```
Timeline Contoh:
┌─────────────────────────────────────────────┐
│  15 Jan          20 Jan          25 Jan    31 Jan
│ Posting Date     STA Date      Payment Date Due Date
│ (PO dibuat)    (Barang tiba)  (Bayar)     (Deadline)
└─────────────────────────────────────────────┘
```

**Tips:**
- **Posting Date** = Hari ini atau hari pertama pesanan dibuat
- **STA Date** = Biasanya lead time dari vendor (contoh: 5 hari)
- **Payment Date** = Kapan Anda akan bayar
- **Due Date** = Deadline terakhir pembayaran

---

## 💰 Tab 4: PEMBAYARAN (Payment Information)

### A. Kurs (Exchange Rate)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Rate** | Kurs tukar yang digunakan | 15,500 (IDR/USD) | ⚠️ Opsional |

**Cara Isi:**
- Isi jika ada transaksi mata uang asing (USD, EUR, dll)
- Gunakan kurs saat PO dibuat
- Contoh: Jika beli dari USA dengan USD, masukkan kurs USD hari itu

### B. Syarat Pembayaran (Payment Terms)

| Field | Deskripsi | Pilihan | Wajib? |
|-------|-----------|---------|--------|
| **Payment Terms** | Jenis pembayaran | Cash / Bank | ✅ Ya |

**Penjelasan:**
- **Cash** = Pembayaran tunai/COD
- **Bank** = Pembayaran melalui transfer bank
- Pilih sesuai kesepakatan dengan vendor

### C. Pajak (Tax)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Tax** | Persentase pajak yang dikenakan | 10 (berarti 10%) | ⚠️ Opsional |

**Cara Isi:**
- Isi dengan persentase pajak (0-100)
- Contoh: Jika ada PPN 10%, masukkan angka **10**
- Sistem akan otomatis menghitung jumlah pajak

### D. Diskon (Discount)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Discount Percentage** | Diskon dalam persentase | 5 (berarti 5%) | ⚠️ Opsional |

**Cara Isi:**
- Isi diskon yang diberikan vendor (0-100%)
- Contoh: Beli banyak dapat diskon 5%, masukkan **5**
- Sistem otomatis menghitung nilai diskon

---

## 📦 Tab 5: TOTAL DAN PERHITUNGAN

Bagian ini biasanya **otomatis** terisi berdasarkan item yang ditambahkan.

| Field | Deskripsi | Sifat |
|-------|-----------|-------|
| **Total Sebelum Diskon** | Jumlah semua item | 🔄 Otomatis |
| **Nilai Diskon** | Hasil perhitungan diskon | 🔄 Otomatis |
| **Total Setelah Diskon** | Subtotal - Diskon | 🔄 Otomatis |
| **Jumlah Pajak** | Hitungan dari tax % | 🔄 Otomatis |
| **TOTAL AKHIR** | Total keseluruhan | 🔄 Otomatis |

**Contoh Perhitungan:**
```
Total Item         : Rp 1.000.000
Diskon 5%          : Rp   50.000 -
Subtotal           : Rp   950.000
Pajak 10%          : Rp   95.000 +
TOTAL AKHIR        : Rp 1.045.000
```

---

## 🚚 Tab 6: INFORMASI LOGISTIK (Logistics)

| Field | Deskripsi | Wajib? |
|-------|-----------|--------|
| **Ship To** | Negara tujuan pengiriman | ⚠️ Opsional |
| **Pay To** | Bank penerima pembayaran | ⚠️ Opsional |

**Cara Isi:**
- **Ship To** = Pilih negara tujuan (contoh: Indonesia)
- **Pay To** = Pilih bank penerima (jika ada opsi)

---

## 💬 Informasi Tambahan (Additional Info)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Catatan** (Remarks) | Catatan tambahan atau spesial | Urgent shipment | ⚠️ Opsional |
| **Vessel/Flight** | Nama kapal atau penerbangan | MS Seatrade 001 | ⚠️ Opsional |
| **Container** | Nomor container pengiriman | CONT-2025-001 | ⚠️ Opsional |

---

## ✅ Langkah Menyimpan dan Finalisasi

### Menyimpan Sebagai Draft

1. Klik tombol **[Save]** atau **[Simpan]**
2. Pesanan disimpan dalam status **Draft**
3. Anda bisa kembali dan mengedit nanti

### Menyelesaikan/Finalisasi Pesanan

1. Setelah semua data lengkap, klik tombol **[Finalize]**
2. Status berubah menjadi **Finalized**
3. Pesanan siap dikirim ke vendor
4. Beberapa field tidak bisa diubah lagi

---

## ❌ Validasi dan Error

Jika ada error, periksa:

| Error | Penyebab | Solusi |
|-------|---------|--------|
| "Nomor PO sudah ada" | Nomor duplikat | Gunakan nomor lain |
| "Vendor belum dipilih" | Vendor kosong | Pilih vendor di field Vendor |
| "Tanggal tidak valid" | Format salah atau tanggal masa lalu | Gunakan tanggal yang benar |
| "Diskon > 100%" | Input diskon melebihi 100 | Perbaiki persentase diskon |

---

## 📝 Checklist Sebelum Finalisasi

Sebelum mengklik Finalize, pastikan:

- ✅ Nomor PO sudah benar dan unik
- ✅ Vendor sudah dipilih dengan benar
- ✅ Semua tanggal sudah terisi
- ✅ Payment Terms sudah dipilih
- ✅ Setidaknya 1 item sudah ditambahkan
- ✅ Diskon dan pajak sudah benar
- ✅ Total perhitungan sudah benar
- ✅ Lampiran dokumen (jika ada) sudah ditambahkan

---

## 🔗 Langkah Berikutnya

Setelah membuat PO dasar:
1. **Tambahkan Item** → Baca: 02_DETAIL_ITEM_PESANAN.md
2. **Tambahkan Freight** → Baca: 03_INFORMASI_PENGIRIMAN.md
3. **Lampirkan Dokumen** → Baca: 04_LAMPIRAN_DAN_DOKUMEN.md

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
