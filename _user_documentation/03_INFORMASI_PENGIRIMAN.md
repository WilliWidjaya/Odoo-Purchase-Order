# 🚚 Panduan Informasi Pengiriman (Freight & Shipping)

## Pengenalan

Bagian ini menjelaskan cara mengelola informasi pengiriman dan biaya freight dalam pesanan pembelian. Freight adalah biaya transportasi/pengiriman barang dari supplier ke tujuan Anda.

---

## Mengapa Freight Penting?

✅ **Alasan pentingnya:**
- Menghitung total biaya pembelian yang akurat
- Melacak biaya logistik per pesanan
- Mengetahui siapa pengangkut barang
- Mengidentifikasi container/shipment
- Pelaporan keuangan dan cost analysis
- Tracking barang hingga tiba

---

## 📌 Bagian A: INFORMASI LOGISTIK UMUM (General Logistics)

Sebelum menambah freight detail, isi informasi logistik umum:

### 1. Ship To (Tujuan Pengiriman)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Ship To** | Negara tujuan pengiriman | Indonesia | ⚠️ Opsional |

**Cara Isi:**
- Klik field Ship To
- Pilih negara tujuan
- Contoh: Indonesia, China, USA, dll

### 2. Pay To (Pembayaran ke)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Pay To** | Bank penerima pembayaran | Bank Mandiri | ⚠️ Opsional |

**Cara Isi:**
- Pilih dari daftar bank yang tersedia
- Atau masukkan manual jika tidak ada
- Ini adalah penerima pembayaran dari supplier

---

## 🚛 Bagian B: DETAIL PENGIRIMAN (Freight Details)

### Menambahkan Freight

1. Scroll ke tab **"Freight"** atau **"Pengiriman"**
2. Klik tombol **[+ Add Line]** untuk menambah biaya freight baru
3. Isi detail pengiriman

---

## 📋 Kolom-Kolom Freight

### 1. Express Code (Kode Ekspedisi)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Express Code** | Kode unik ekspedisi/kurir | EXP-001 | ⚠️ Opsional |

**Cara Isi:**
- Kode internal untuk ekspedisi/kurir
- Contoh: EXP-001 (untuk ekspedisi nomor 1)
- Gunakan untuk identifikasi yang konsisten

**Contoh Express Code:**
```
- CONT-2025-001 (untuk Container 1 tahun 2025)
- SHIP-MS-001 (untuk shipment via MS Vessel)
- AIR-GA-2025-001 (untuk Air cargo GA Airlines 2025)
```

### 2. Express Name (Nama Ekspedisi)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Express Name** | Nama lengkap ekspedisi/kurir | PT Semarang Cargo | ⚠️ Opsional |

**Cara Isi:**
- Nama perusahaan pengangkut/shipping company
- Contoh: PT Semarang Cargo, DHL, FedEx, UPS, dll

**Contoh Express Name:**
```
- PT Semarang Cargo (pengangkut lokal)
- Seatrade Shipping (pengangkut laut)
- Garuda Indonesia (maskapai penerbangan)
- Kereta Api Indonesia (KAI)
```

### 3. Remarks (Catatan)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Remarks** | Catatan tambahan tentang pengiriman | Door-to-door service | ⚠️ Opsional |

**Kegunaan:**
- Catatan khusus tentang pengiriman
- Instruksi khusus untuk kurir
- Kondisi atau persyaratan pengiriman

**Contoh Remarks:**
```
- "Door-to-door service ke gudang Cibitung"
- "Cold storage required"
- "Handle with care - Fragile items"
- "Insurance included"
- "Urgent delivery needed"
```

### 4. Tax Code (Kode Pajak)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Tax Code** | Kode pajak untuk freight | PPN-10 | ⚠️ Opsional |

**Cara Isi:**
- Jika ada pajak atas biaya pengiriman
- Contoh: PPN-10 (berarti ada PPN 10%)
- Konsultasikan dengan divisi Pajak/Finance

### 5. Gross Amount (Biaya Pengiriman)

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Gross Amount** | Total biaya pengiriman | Rp 5.000.000 | ✅ Ya (jika ada freight) |

**Cara Isi dan Tips:**
- Isi total biaya pengiriman
- Termasuk semua charge (handling, insurance, dll)
- Harus positif (≥ 0)

**Contoh Biaya Freight:**
```
Pengiriman Laut:
- Port handling: Rp 500.000
- Freight charge: Rp 3.000.000
- Insurance: Rp 500.000
- Bea cukai: Rp 1.000.000
Total Gross Amount: Rp 5.000.000

Pengiriman Udara:
- Air freight: Rp 10.000.000
- Handling: Rp 1.000.000
- Insurance: Rp 2.000.000
Total Gross Amount: Rp 13.000.000
```

---

## 📝 Contoh Pengisian Freight Lengkap

### Contoh 1: Pengiriman Kapal Laut

```
Express Code     : CONT-2025-001
Express Name     : PT Semarang Cargo
Remarks          : Door-to-door service, port bongkar Tanjung Perak
Tax Code         : PPN-10
Gross Amount     : Rp 5.000.000

Details terpisah bisa:
- Port handling fee: Rp 500.000
- Freight: Rp 3.000.000
- Insurance: Rp 500.000
- Customs: Rp 1.000.000
```

### Contoh 2: Pengiriman Udara

```
Express Code     : SHIP-GA-2025-001
Express Name     : Garuda Indonesia Cargo
Remarks          : Next day delivery, insurance included, urgent
Tax Code         : PPN-10
Gross Amount     : Rp 15.000.000

Details bisa termasuk:
- Air freight (kg rate): Rp 10.000.000
- Ground handling: Rp 2.000.000
- Insurance: Rp 2.000.000
- Misc charges: Rp 1.000.000
```

### Contoh 3: Pengiriman Darat

```
Express Code     : TRUCK-001-2025
Express Name     : PT Sumitra Transport
Remarks          : Kirim ke gudang Bekasi, alamat: Jl. Merdeka 100
Tax Code         : PPN-10
Gross Amount     : Rp 2.000.000

Details bisa:
- Transport: Rp 1.500.000
- Handling: Rp 300.000
- Misc: Rp 200.000
```

---

## 🏗️ Bagian C: INFORMASI VESSEL & CONTAINER

Untuk pengiriman laut/kapal, isi informasi tambahan:

| Field | Deskripsi | Contoh | Wajib? |
|-------|-----------|--------|--------|
| **Vessel/Flight** | Nama kapal atau penerbangan | MS Seatrade Cendrawasih | ⚠️ Opsional |
| **Container** | Nomor container pengiriman | CONT-2025-0001 | ⚠️ Opsional |

**Cara Isi:**

**Vessel/Flight:**
- Untuk pengiriman laut: Nama kapal (contoh: MS Seatrade, Evergreen)
- Untuk pengiriman udara: Nomor penerbangan (contoh: GA-501, MH-007)
- Untuk pengiriman darat: Nomor armada (contoh: TRUCK-001)

**Container:**
- Nomor container untuk pengiriman laut
- Format biasanya: 4 huruf + 6 angka (contoh: TCLU1234567)
- Untuk udara: nomor Air Waybill (AWB)

**Contoh:**
```
Pengiriman Laut:
Vessel      : MS Seatrade Cendrawasih
Container   : TCLU1234567

Pengiriman Udara:
Flight      : GA-501
Container   : AWB 001-1234567890

Pengiriman Darat:
Vehicle     : TRUCK-JAK-001
Container   : RESI-001-2025
```

---

## 💰 Perhitungan Freight dalam Total

Freight biaya ditambahkan ke total keseluruhan pesanan:

```
Contoh Perhitungan:
┌─────────────────────────────────────┐
│ Total Item           : Rp 1.000.000 │
│ Diskon Item (5%)     : Rp   50.000 -│
│ Subtotal             : Rp   950.000 │
│ Pajak Item (10%)     : Rp   95.000 +│
│ Subtotal 2           : Rp 1.045.000 │
│                                     │
│ + FREIGHT:                          │
│ Pengiriman Laut      : Rp 5.000.000 │
│ Pajak Freight (10%)  : Rp   500.000 │
│                                     │
│ TOTAL AKHIR          : Rp 6.545.000 │
└─────────────────────────────────────┘
```

---

## 🔄 Mengelola Freight

### Menambah Freight Baru
1. Klik **[+ Add Line]** di tab Freight
2. Isi detail pengiriman
3. Klik Save

### Mengedit Freight
1. Klik baris freight yang ingin diubah
2. Edit field yang perlu diubah
3. Klik Save

### Menghapus Freight
1. Klik baris freight
2. Klik icon Delete (🗑️)
3. Konfirmasi penghapusan

---

## 📊 Multiple Freight (Banyak Freight)

Anda bisa menambah lebih dari 1 freight dalam 1 pesanan:

**Contoh: PO dengan 2 shipment berbeda**
```
Freight 1: Pengiriman Container 1 via Laut
- Express: PT Semarang Cargo
- Gross Amount: Rp 5.000.000

Freight 2: Pengiriman Container 2 via Laut
- Express: PT Semarang Cargo
- Gross Amount: Rp 5.000.000

Total Freight: Rp 10.000.000
```

---

## 📍 Tracking Shipment

Setelah pesanan finalized, gunakan informasi freight untuk:
- ✅ Tracking shipment via kurir
- ✅ Koordinasi dengan gudang penerima
- ✅ Persiapan untuk customs clearance
- ✅ Verifikasi kehadiran barang
- ✅ Claims jika ada kerusakan

**Info yang dibutuhkan untuk tracking:**
- Express Code / Nomor Tracking
- Vessel/Flight Number
- Container Number
- Estimasi tiba

---

## ⚠️ Validasi Freight

Jika ada error saat pengisian:

| Error | Penyebab | Solusi |
|-------|---------|--------|
| "Gross Amount harus > 0" | Biaya 0 atau negatif | Isi biaya yang benar |
| "Express Name tidak valid" | Nama ekspedisi tidak terdaftar | Pilih dari daftar atau daftar baru |
| "Tax Code tidak valid" | Kode pajak salah | Pilih kode pajak yang benar |

---

## 💡 Tips Pengiriman

### ✅ Praktik Terbaik:
- ✅ Catat semua nomor tracking sebelum finalize
- ✅ Komunikasikan dengan warehouse penerima
- ✅ Pastikan informasi vessel/container akurat
- ✅ Perhatikan lead time pengiriman
- ✅ Cek asuransi pengiriman jika diperlukan

### ❌ Yang Perlu Dihindari:
- ❌ Jangan ubah freight info setelah finalized
- ❌ Jangan lupakan biaya handling/misc
- ❌ Jangan lupa pajak atas freight
- ❌ Jangan gunakan nama ekspedisi yang tidak jelas

---

## 🔗 Langkah Berikutnya

1. **Lampirkan Dokumen** → Baca: 04_LAMPIRAN_DAN_DOKUMEN.md
2. **Finalisasi Pesanan** → Kembali ke: 01_MEMBUAT_PESANAN_PEMBELIAN.md
3. **Tips & Best Practices** → Baca: 05_TIPS_DAN_BEST_PRACTICES.md

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
