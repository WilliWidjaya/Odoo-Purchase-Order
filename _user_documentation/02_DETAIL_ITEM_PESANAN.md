# 📦 Panduan Detail Item Pesanan (Purchase Order Content)

## Pengenalan

Bagian ini menjelaskan cara menambahkan item/barang yang akan dipesan dalam pesanan pembelian. Setiap item harus diisi dengan detail yang akurat agar proses pembelian berjalan lancar.

---

## Mengapa Detail Item Penting?

Detail item mencakup:
- ✅ Spesifikasi barang yang dipesan
- ✅ Jumlah dan satuan
- ✅ Harga per unit
- ✅ Diskon per item
- ✅ Pajak dan kode pajak
- ✅ Informasi tambahan (lokasi, warehouse, dll)

Detail yang akurat memastikan:
- 📊 Perhitungan biaya yang tepat
- 📋 Rekam jejak yang jelas
- ✔️ Kontrol kualitas dan kuantitas
- 📦 Pengelolaan inventory yang baik

---

## 📝 Menambahkan Item Pesanan

### Langkah 1: Akses Tab Item

1. Buat atau buka pesanan pembelian yang sudah ada
2. Scroll ke bawah → Tab **"Item Pesanan"** atau **"Purchase Order Content"**
3. Klik tombol **[+ Add Line]** atau **[+ Tambah Baris]**

Sebuah baris item baru akan muncul.

### Langkah 2: Isi Informasi Umum Item

---

## 📌 Bagian A: INFORMASI BARANG (Item Information)

### 1. Item Code (Kode Item)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Item Code** | Kode unik untuk barang ini | KD-001-KAYU | ✅ Ya |

**Cara Isi dan Tips:**
- Gunakan kode yang mudah dikenali
- Panjang: minimum 3 karakter, maksimal 20 karakter
- Format konsisten di seluruh sistem

**Contoh Format Kode:**
```
Format: KD-KATEGORI-NOMOR
- KD-KAY-001 → Kayu jenis 1
- KD-BES-005 → Besi jenis 5
- KD-PLI-010 → Plastik jenis 10

Atau:

Format: KATEGORI-NOMOR-TAHUN
- KAY-001-2025 → Kayu nomor 1 tahun 2025
```

### 2. Item Name (Nama Item)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Item Name** | Nama lengkap barang | Kayu Jati Grade A | ✅ Ya |

**Cara Isi dan Tips:**
- Nama harus deskriptif dan jelas
- Panjang: minimum 3, maksimal 75 karakter
- Sertakan spesifikasi penting (grade, ukuran, tipe)

**Contoh Nama Item yang Baik:**
```
❌ BURUK:
- "Barang"
- "Item 1"
- "Produk"

✅ BAIK:
- "Kayu Jati Grade A - Ukuran 4x8cm"
- "Besi Baja SS 304 - Diameter 10mm"
- "Plastik HDPE - Warna Bening"
```

### 3. Free Text (Teks Bebas)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Free Text** | Deskripsi/catatan tambahan | Proses palu, finishing halus | ⚠️ Opsional |

**Kegunaan:**
- Tambahkan detail spesifik barang
- Instruksi khusus untuk supplier
- Catatan tentang packaging
- Contoh: "Proses palu manual", "Finishing cat gloss"

---

## 📏 Bagian B: KUANTITAS (Quantity)

### 1. Quantity Consider (Pertimbangan Kuantitas)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Consider Qty** | Jumlah yang dipertimbangkan/planning | 100 | ⚠️ Opsional |

**Kegunaan:**
- Jumlah awal sebelum finalisasi
- Untuk keperluan planning
- Biasanya digunakan untuk internal tracking

### 2. Quantity (Kuantitas Pesanan)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Qty** | Jumlah barang yang dipesan | 50 | ✅ Ya |

**Cara Isi dan Tips:**
- Isi dengan jumlah aktual yang dipesan
- Harus angka positif (≥ 0)
- Contoh: 50 (tidak perlu "pcs" atau satuan di sini)

### 3. Quantity Packaging (Kuantitas Packaging)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Packaging QTY** | Jumlah per kemasan | 10 | ⚠️ Opsional |

**Kegunaan:**
- Jika barang dijual per kemasan
- Contoh: 50 pcs barang = 5 karton (5 packaging)
- Membantu menghitung jumlah palet/box

**Contoh Penggunaan:**
```
Pesanan: 50 pcs barang
Packaging: 10 pcs per karton
Maka: 50 ÷ 10 = 5 karton yang dipesan
```

### 4. Quantity Real (Kuantitas PO Asli)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Qty PO Asli** | Jumlah dari PO asli/original | 50 | ⚠️ Opsional |

**Kegunaan:**
- Tracking jika ada perubahan pesanan
- Menunjukkan jumlah original vs final
- Untuk audit trail (jejak perubahan)

---

## 🏭 Bagian C: SATUAN PENGUKURAN (Unit of Measurement)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Packaging UOM** | Satuan packaging | Karton | ⚠️ Opsional |
| **UOM** | Satuan pengukuran utama | PCS (Pieces) | ⚠️ Opsional |

**Contoh UOM (Unit of Measurement):**
```
- PCS = Pieces (Buah)
- KG = Kilogram (Berat)
- M = Meter (Panjang)
- M2 = Meter Persegi (Luas)
- M3 = Meter Kubik (Volume)
- SET = Set/Paket
- BOX = Kotak
- DRUM = Drum
- KARTON = Karton
```

**Cara Isi:**
- Tentukan satuan yang sesuai dengan barang
- Contoh: Kayu biasanya dalam M3 atau PCS
- Berat biasanya dalam KG
- Panjang/lebar dalam M

---

## 💵 Bagian D: HARGA DAN DISKON (Price & Discount)

### 1. Price (Harga per Unit)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Price** | Harga per unit barang | 100,000 | ✅ Ya |

**Cara Isi dan Tips:**
- Isi harga per unit (bukan total)
- Harus lebih besar dari 0
- Contoh: Jika 50 pcs @ Rp 100.000, masukkan 100,000

### 2. Discount Percentage (Diskon Persentase)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Discount (%)** | Diskon per item dalam % | 5 (berarti 5%) | ⚠️ Opsional |

**Cara Isi dan Tips:**
- Isi persentase diskon (0-100)
- Otomatis menghitung nilai diskon
- Contoh: 5 berarti 5% dari harga

**Contoh Perhitungan:**
```
Harga: Rp 100.000
Diskon: 5%
Nilai Diskon: Rp 100.000 × 5% = Rp 5.000
Harga Setelah Diskon: Rp 100.000 - Rp 5.000 = Rp 95.000
```

### 3. Total (Otomatis)

| Field | Deskripsi | Sifat |
|-------|-----------|-------|
| **Total** | Harga per unit setelah diskon | 🔄 Otomatis |

**Cara Kerja:**
- Sistem otomatis menghitung
- Formula: `Price - (Price × Discount%)`
- Tidak perlu diisi manual

---

## 💰 Bagian E: PAJAK (Tax)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Tax Code** | Kode pajak yang berlaku | PPN-10 | ⚠️ Opsional |
| **Taxline** | Baris/Referensi pajak | TL-001 | ⚠️ Opsional |

**Cara Isi:**
- Konsultasikan dengan divisi Pajak/Finance
- Contoh: PPN-10 untuk PPN 10%
- Gunakan kode yang sudah didefinisikan di sistem

---

## 🏭 Bagian F: INFORMASI PRODUKSI (Production Info)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **PI Number** | Nomor Packing List/Invoice | PI-2025-001 | ⚠️ Opsional |
| **Slaughterhouse** | Tempat produksi/pabrik | Pabrik X Jakarta | ⚠️ Opsional |
| **Rate** | Kurs/Rate untuk item ini | 15,500 | ⚠️ Opsional |

**Kegunaan:**
- **PI Number**: Reference ke dokumen Packing List
- **Slaughterhouse**: Lokasi asal barang (terutama untuk daging/food)
- **Rate**: Kurs jika berbeda per item

---

## 📊 Bagian G: PERHITUNGAN OTOMATIS

Bagian ini **tidak perlu** diisi manual - sistem menghitung otomatis:

| Field | Formula | Contoh |
|-------|---------|--------|
| **Total after Discount** | Price - (Price × Discount%) | Rp 95.000 |
| **Gross after Discount** | Total × Quantity | Rp 4.750.000 |

---

## ✅ Validasi Data Item

Sistem memiliki validasi otomatis. Jika ada error:

| Error | Penyebab | Solusi |
|-------|---------|--------|
| "Item Code wajib diisi" | Item Code kosong | Isi Item Code |
| "Item Code minimal 3 karakter" | Terlalu pendek | Gunakan nama lebih panjang |
| "Item Code maksimal 20 karakter" | Terlalu panjang | Perpendek menjadi max 20 karakter |
| "Item Name wajib diisi" | Item Name kosong | Isi nama item |
| "Item Name 3-75 karakter" | Nama terlalu pendek/panjang | Sesuaikan panjang nama |
| "Quantity tidak boleh negatif" | Qty < 0 | Gunakan angka positif |
| "Price harus > 0" | Harga 0 atau negatif | Isi harga yang benar |
| "Diskon 0-100" | Diskon > 100% | Perbaiki persentase diskon |

---

## 📝 Contoh Pengisian Item Lengkap

### Contoh 1: Pembelian Kayu
```
Item Code        : KD-KAY-001
Item Name        : Kayu Jati Grade A - 4x8cm
Free Text        : Proses palu, finishing halus
Consider Qty     : 100 (planning)
Qty              : 50
Packaging UOM    : Karton
Packaging QTY    : 10
UOM              : PCS
Price            : Rp 100.000 per PCS
Discount %       : 5%
Tax Code         : PPN-10
PI Number        : PI-2025-0001
```

### Contoh 2: Pembelian Spare Parts
```
Item Code        : KD-SPA-015
Item Name        : Bearing SKF 6204-2Z (20x47x14mm)
Free Text        : Kondisi baru, sealed bearing
Consider Qty     : 200
Qty              : 100
Packaging UOM    : Box
Packaging QTY    : 20
UOM              : PCS
Price            : Rp 50.000 per PCS
Discount %       : 10%
Tax Code         : PPN-10
Rate             : 15,500 (jika dari supplier USD)
```

---

## 🔄 Mengelola Item

### Menambah Item Baru
1. Klik **[+ Add Line]** di bawah tabel item
2. Isi seperti langkah-langkah di atas
3. Klik Save setelah selesai

### Mengedit Item
1. Klik baris item yang ingin diubah
2. Ubah field yang perlu diubah
3. Klik Save

### Menghapus Item
1. Klik baris item
2. Klik icon **Trash/Delete** (🗑️)
3. Konfirmasi penghapusan

---

## 💡 Tips dan Best Practices

### ✅ Lakukan Ini:
- ✅ Gunakan kode item yang konsisten di seluruh sistem
- ✅ Sertakan detail spesifikasi di nama item
- ✅ Double-check harga sebelum save
- ✅ Gunakan diskon item jika sesuai kesepakatan
- ✅ Catat PI Number dari supplier

### ❌ Jangan Lakukan Ini:
- ❌ Jangan ubah harga ketika pesanan sudah finalized
- ❌ Jangan gunakan nama item yang terlalu umum
- ❌ Jangan input quantity yang tidak sesuai kebutuhan
- ❌ Jangan lupa validasi semua field sebelum finalize

---

## 🎯 Checklist Sebelum Finalisasi

- ✅ Semua item sudah ditambahkan
- ✅ Item Code & Item Name sudah benar
- ✅ Quantity sudah sesuai pesanan
- ✅ Harga sudah dikonfirmasi
- ✅ Diskon sudah dikonfirmasi
- ✅ Tax Code sudah benar
- ✅ Total perhitungan sudah sesuai
- ✅ Tidak ada item dengan error

---

## 🔗 Langkah Berikutnya

1. **Tambahkan Freight/Pengiriman** → Baca: 03_INFORMASI_PENGIRIMAN.md
2. **Lampirkan Dokumen** → Baca: 04_LAMPIRAN_DAN_DOKUMEN.md
3. **Finalisasi Pesanan** → Kembali ke: 01_MEMBUAT_PESANAN_PEMBELIAN.md

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
