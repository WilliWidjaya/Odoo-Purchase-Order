# 💡 Tips dan Best Practices (Tips & Trik Penggunaan)

## Pengenalan

Bagian ini berisi kumpulan tips, trik, dan best practices untuk menggunakan modul Purchase Order secara optimal dan efisien.

---

## 🎯 TIPS UMUM

### 1. Perencanaan Sebelum Membuat PO

**✅ Lakukan Ini:**
```
Sebelum membuat PO, siapkan:
□ Daftar barang yang dibutuhkan (dengan spesifikasi detail)
□ Nomor PO yang akan digunakan
□ Data vendor (dari list yang terdaftar)
□ Harga dari supplier (quotation/penawaran)
□ Expected delivery date
□ Budget/allocation center
□ Contact person di vendor
```

**Manfaat:**
- Proses lebih cepat
- Data lebih akurat
- Mengurangi error

---

### 2. Gunakan Nomor PO yang Konsisten

**❌ JANGAN:**
```
PO-001, PO2025-01, P001, pojan2025, PO/JAN/001
(Tidak konsisten, sulit di-track)
```

**✅ LAKUKAN:**
```
Format 1: PO-2025-001, PO-2025-002, PO-2025-003
Format 2: PO/001/2025, PO/002/2025, PO/003/2025
Format 3: POJAN-0001, POFEB-0001, POMAR-0001

Pilih SATU format dan gunakan secara konsisten!
```

**Manfaat:**
- Mudah di-track dan di-cari
- Sistematis dan professional
- Mempermudah audit

---

### 3. Detail Item yang Jelas dan Spesifik

**❌ JANGAN:**
```
Item Code: KD-001
Item Name: Barang
Spesifikasi: Tidak ada

→ Tidak jelas apa yang dipesan
```

**✅ LAKUKAN:**
```
Item Code: KD-KAY-001
Item Name: Kayu Jati Grade A - 4x8x2 cm
Free Text: Proses palu manual, finishing halus, ori kayunya sehat

→ Supplier tahu persis apa yang harus dikirim
```

**Informasi yang Perlu Jelas:**
- Jenis/material barang
- Grade/kualitas
- Ukuran/dimensi (panjang x lebar x tinggi)
- Proses/treatment khusus
- Packaging requirement
- Warna atau tipe tertentu

---

## 💰 TIPS PEMBAYARAN & BIAYA

### 4. Verifikasi Harga Sebelum Save

**Proses Verifikasi:**
```
Langkah 1: Dapatkan Quotation dari supplier
Langkah 2: Bandingkan dengan harga sebelumnya (jika ada)
Langkah 3: Nego jika perlu (untuk quantity besar)
Langkah 4: Pastikan harga sudah agreed dan final
Langkah 5: Input ke sistem
Langkah 6: Double-check sebelum save
Langkah 7: Aproval dari manager/supervisor jika diperlukan
```

**Tips Harga:**
- Hubungi supplier untuk best quote
- Minta harga volume untuk quantity besar
- Perhatian ke "price include apa" (ex: sudah termasuk freight?)
- Jangan ubah harga setelah PO finalized

---

### 5. Hitung Total dengan Benar

**Formula Perhitungan yang Benar:**
```
UNTUK SETIAP ITEM:
Price Per Unit           : Rp 100.000
Quantity                 : 50 pcs
Subtotal                 : 100.000 × 50 = Rp 5.000.000
Diskon Item (5%)         : 5.000.000 × 5% = Rp 250.000
Total Setelah Diskon     : 5.000.000 - 250.000 = Rp 4.750.000

TOTAL PO:
Semua Item              : Rp 4.750.000 (contoh 1 item)
Diskon Level PO (jika ada) : minus X%
Subtotal               : Rp 4.750.000
Pajak (10%)            : 4.750.000 × 10% = Rp 475.000
Freight                : Rp 2.000.000
TOTAL AKHIR            : Rp 7.225.000
```

**Cara Verifikasi:**
1. Gunakan calculator terpisah
2. Double-check sebelum save
3. Minta approval dari Finance jika amount besar
4. Screenshot total untuk record

---

### 6. Diskon yang Efektif

**Tipe Diskon:**
```
1. Diskon Item (Quantity Discount)
   - Jika beli 50+ pcs, dapat diskon 5%
   - Input di field "Discount %" per item

2. Diskon PO (Pembelian Keseluruhan)
   - Jika total PO > Rp 10juta, dapat diskon 3%
   - Input di field "Discount Percentage" di bagian Payment

3. Diskon Musiman
   - Tanya supplier tentang seasonal discount
   - Promo bulan tertentu

4. Diskon Early Payment
   - Jika bayar cepat (ex: 7 hari), dapat diskon 2%
   - Catat sebagai "Term: 2/7 Net 30"
```

**Tips Maksimalkan Diskon:**
- Beli dalam quantity besar untuk dapat volume discount
- Koordinasi dengan dept lain untuk consolidate order
- Negosiasi payment term untuk early payment discount
- Cek promo supplier sebelum order

---

## 📦 TIPS ITEM DAN QUANTITY

### 7. Quantity yang Tepat

**❌ JANGAN:**
```
Order terlalu banyak → Inventory tergantung lama
Order terlalu sedikit → Kena biaya freight tinggi, harus order lagi
```

**✅ LAKUKAN:**
```
Hitung dengan formula:
Kebutuhan 3 bulan + Safety Stock 20% = Total Order

Contoh:
- Kebutuhan per bulan: 100 pcs
- Kebutuhan 3 bulan: 300 pcs
- Safety stock (20%): 60 pcs
- Total order: 360 pcs (round up)

Tujuan:
✓ Efisien biaya freight
✓ Tidak over stock
✓ Memenuhi kebutuhan operasional
```

---

### 8. UOM (Unit of Measurement) yang Konsisten

**Penting untuk Tracking:**
```
JANGAN CAMPUR UOM:
❌ Item 1: 50 PCS
❌ Item 2: 5 BOX (tidak tahu isi berapa)
❌ Item 3: 2 PALLET

GUNAKAN YANG KONSISTEN:
✅ Item 1: 50 PCS
✅ Item 2: 50 PCS (jika 10 PCS per BOX)
✅ Item 3: 50 PCS (jika 25 PCS per pallet)

Atau di "Packaging UOM" catat:
- Item 1: 50 PCS (Packaging: BOX isi 10)
- Item 2: Sama
- Item 3: Sama
```

**Standar UOM:**
```
Panjang/Jarak:  M, CM, MM, INCH, FEET
Berat:          KG, TON, LB, GRAM
Volume:         M3, LITER, GALLON
Jumlah:         PCS, SET, PAIR, DOZEN, PACK
Wadah:          BOX, KARTON, DRUM, PALLET, CONTAINER
Waktu:          HOUR, DAY, MONTH, YEAR
```

---

## 🚚 TIPS PENGIRIMAN (FREIGHT)

### 9. Verifikasi Informasi Pengiriman

**Sebelum Finalize, Cek:**
```
□ Vessel/Flight number sudah benar
□ Container number sudah benar
□ Shipper/Express name sudah tepat
□ ETA (Estimated Time of Arrival) sudah tercatat
□ Freight cost sudah final
□ Insurance included atau tidak
□ Incoterm sudah clear (FOB, CIF, DDP, dll)
□ Tracking number sudah tercatat
```

---

### 10. Jenis Pengiriman vs Cost

**Pilih yang Tepat:**
```
PENGIRIMAN LAUT:
Pro:  Biaya lebih murah, capacity besar
Cons: Waktu lebih lama (20-30 hari), delay possible
Best for: Non-urgent, bulk order, dari/ke port

PENGIRIMAN UDARA:
Pro:  Cepat (1-3 hari), reliable
Cons: Biaya mahal, volume terbatas, berat terbatas
Best for: Urgent, high-value items, limited weight

PENGIRIMAN DARAT (Lokal):
Pro:  Cepat, biaya terjangkau, flexible
Cons: Berat terbatas, tidak untuk jarak jauh
Best for: Lokal dalam negeri, medium distance

PENGIRIMAN KOMBINASI (Multi-modal):
Pro:  Optimal cost & time
Cons: Lebih complicated, koordinasi lebih banyak
Best for: Import besar dengan timeline flexible
```

**Contoh Pilihan:**
```
Scenario 1: Barang urgent, value Rp 1juta
→ Pilih: AIR CARGO (cepat, value justify cost)

Scenario 2: Kayu Jati, quantity 20 ton, tidak urgent
→ Pilih: LAUT (bulk, harga murah)

Scenario 3: Spare parts, dari supplier Jakarta ke Bandung
→ Pilih: TRUCK DARAT (murah, cepat, dekat)

Scenario 4: Import machinery dari China, quantity besar, timeline 2 bulan
→ Pilih: LAUT + TRUCK DARAT (cost optimal)
```

---

## 📎 TIPS LAMPIRAN DOKUMEN

### 11. Dokumentasi Lengkap untuk Audit

**Dokumen WAJIB Ada:**
```
Untuk SEMUA PO:
□ Quotation dari supplier
□ PO Confirmation dari supplier

Untuk Import (Pengiriman Luar):
□ Invoice
□ Bill of Lading (BoL)
□ Packing List
□ Certificate of Origin (CoO)

Untuk Compliance:
□ Quality Certificate
□ Test Report (jika ada)
□ Insurance Document (jika ada)

Untuk Dispute Resolution:
□ Email/chat confirmation dengan supplier
□ Proof of payment
□ Photos (jika ada damage)
□ Claim document
```

---

### 12. Penamaan File yang Baik

**❌ BURUK:**
```
file.pdf
scan.pdf
doc1.pdf
invoice.pdf (tidak tahu dari siapa, bulan apa?)
```

**✅ BAIK:**
```
Quotation-PT-ABC-Jan-2025.pdf
Invoice-PT-ABC-INV-2025-001.pdf
BoL-Container-TCLU1234567.pdf
Packing-List-Shipment-001.pdf
Quality-Cert-Batch-A-2025.pdf
Test-Report-Bearing-SKF-2025.pdf
```

**Template Penamaan:**
```
[DOCUMENT TYPE]-[SUPPLIER NAME]-[MONTH]-[YEAR].pdf

Contoh:
- Invoice-PT-ABC-Jan-2025.pdf
- Quote-PT-XYZ-Feb-2025.pdf
- BoL-Container-001-Jan-2025.pdf
```

---

## ✅ TIPS WORKFLOW YANG EFISIEN

### 13. Checklist Sebelum Finalize

**Print dan Gunakan Checklist Ini:**
```
SEBELUM KLIK "FINALIZE":

INFORMASI DASAR:
□ PO Number sudah unik dan tidak duplikat
□ Nama PO sudah deskriptif
□ Vendor sudah dipilih (jangan kosong)
□ Status sudah set ke "Finalized"

TANGGAL & PEMBAYARAN:
□ Posting date sudah correct (hari ini atau hari order)
□ Due date sudah correct (batas pembayaran)
□ STA Date sudah correct (estimasi barang tiba)
□ Payment Terms sudah dipilih (Cash/Bank)
□ Diskon dan pajak sudah correct

ITEM:
□ Minimum 1 item sudah ditambahkan
□ Setiap item punya Item Code (3-20 karakter)
□ Setiap item punya Item Name (3-75 karakter)
□ Quantity sudah correct (positif, bukan 0)
□ Price sudah diverifikasi dari supplier
□ Diskon sudah correct (0-100%)

TOTAL:
□ Total perhitungan sudah di-verify
□ Amount sesuai dengan quotation supplier
□ Sudah di-approve oleh manager (jika diperlukan)

FREIGHT:
□ Freight info sudah lengkap (jika ada pengiriman)
□ Vessel/Container number sudah tercatat
□ Freight cost sudah final

LAMPIRAN:
□ Quotation dari supplier sudah dilampirkan
□ PO Confirmation sudah dilampirkan (jika ada)
□ Invoice sudah dilampirkan (jika sudah dapat)

LAINNYA:
□ Tidak ada error/warning di sistem
□ Semua field wajib sudah terisi
□ Sudah di-review oleh minimal 1 orang lain
```

---

### 14. Audit Trail dan Dokumentasi

**Simpan Evidence:**
```
Setelah PO Finalized:

1. PRINT atau SCREENSHOT:
   - Halaman PO utama (all tabs)
   - Total calculation
   - Attachment list

2. SAVE COPY:
   - Save ke local folder dengan nama:
     "PO-2025-001-VENDOR-ABC.pdf"
   - Backup ke server/cloud

3. CATAT DI SPREADSHEET:
   - PO Number
   - Vendor
   - Total Amount
   - ETA
   - Contact Person
   - Status pembayaran
   (Untuk tracking)
```

**Manfaat:**
- Jika ada issue nanti, bukti ada
- Audit lebih mudah
- Reconciliation lebih cepat

---

## ⚠️ TIPS MENGHINDARI ERROR

### 15. Error Umum dan Solusinya

**Error 1: "Nomor PO sudah ada"**
```
Penyebab: Nomor PO duplikat
Solusi: Cek PO yang sudah ada, gunakan nomor baru
Cara cek: Search di list PO, atau tanya admin
```

**Error 2: "Vendor belum dipilih"**
```
Penyebab: Field vendor kosong
Solusi: Klik field vendor, pilih dari list
Jika vendor tidak ada: Minta admin untuk tambah vendor baru
```

**Error 3: "Item Code harus 3-20 karakter"**
```
Penyebab: Kode item terlalu pendek atau terlalu panjang
Solusi: 
- Jika pendek: Tambahkan prefix (ex: "KD-" + nama)
- Jika panjang: Perpendek gunakan singkatan
```

**Error 4: "Diskon tidak boleh > 100%"**
```
Penyebab: Input diskon melebihi 100%
Solusi: Perbaiki persentase diskon (max 100%)
Contoh: Ganti 150 menjadi 15 (jika seharusnya 15%)
```

**Error 5: "Total perhitungan tidak sesuai"**
```
Penyebab: Ada item dengan harga/quantity yang salah
Solusi:
1. Check setiap item satu-satu
2. Verifikasi total dengan calculator
3. Cek quotation supplier
4. Perbaiki item yang error
5. Simpan ulang
```

---

## 🎓 TIPS TRAINING & KNOWLEDGE

### 16. Belajar dari Pengalaman

**Lakukan Ini:**
```
□ Review PO lama untuk understanding workflow
□ Tanya ke supervisor tentang best practice mereka
□ Dokumentasikan lesson learned
□ Share knowledge dengan team
□ Update process jika ada improvement
```

---

## 📊 TIPS REPORTING & ANALYSIS

### 17. Track PO Performance

**Buat Tracking:**
```
Per Bulan, catat:
- Total PO dibuat: X
- Total value: Rp Y
- Top vendor (by amount)
- Lead time rata-rata
- On-time delivery rate
- Supplier performance rating

Gunakan data untuk:
✓ Identify trend
✓ Negotiate better terms
✓ Supplier selection
✓ Budget planning
```

---

## 🔐 TIPS KEAMANAN & COMPLIANCE

### 18. Jaga Keamanan Data

**❌ JANGAN:**
```
□ Share login password
□ Print PO dan tinggal di meja
□ Email harga ke supplier tanpa enkripsi
□ Delete dokumen penting
□ Ubah data PO setelah finalize (tanpa approval)
```

**✅ LAKUKAN:**
```
□ Use strong password, change regularly
□ Lock computer saat meninggalkan
□ Keep sensitive data confidential
□ Backup dokumen penting
□ Follow approval process
□ Audit trail untuk semua changes
```

---

## 🎯 RINGKASAN TIPS KUNCI

| Aspek | Tips Kunci | Manfaat |
|--------|-----------|---------|
| **Perencanaan** | Persiapkan semua data sebelum PO | Proses lebih cepat, error berkurang |
| **Nomor PO** | Konsisten format | Mudah tracking, professional |
| **Detail Item** | Spesifik dan jelas | Supplier mengerti, barang sesuai |
| **Harga** | Verifikasi dari quotation | Akurat, menghindari overpay |
| **Quantity** | Hitung dengan formula | Efisien cost, tidak over/under stock |
| **Pengiriman** | Pilih mode yang tepat | Cost & time optimal |
| **Dokumen** | Lengkap dan terorganisir | Audit ready, proof ada |
| **Checklist** | Gunakan sebelum finalize | Error berkurang 90% |

---

## 📖 Dokumentasi Lengkap

Referensi lebih detail:
1. [00_PANDUAN_MEMULAI.md](00_PANDUAN_MEMULAI.md) - Pengenalan umum
2. [01_MEMBUAT_PESANAN_PEMBELIAN.md](01_MEMBUAT_PESANAN_PEMBELIAN.md) - Detail formulir
3. [02_DETAIL_ITEM_PESANAN.md](02_DETAIL_ITEM_PESANAN.md) - Item management
4. [03_INFORMASI_PENGIRIMAN.md](03_INFORMASI_PENGIRIMAN.md) - Freight management
5. [04_LAMPIRAN_DAN_DOKUMEN.md](04_LAMPIRAN_DAN_DOKUMEN.md) - Dokumen attachment
6. [06_REFERENSI_CEPAT.md](06_REFERENSI_CEPAT.md) - Quick reference

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
