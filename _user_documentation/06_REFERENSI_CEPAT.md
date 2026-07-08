# ⚡ Referensi Cepat (Quick Reference)

## 🚀 Mulai Cepat dalam 3 Langkah

### Langkah 1: Buat PO Baru
```
Menu → Pesanan Pembelian → [+ Create] → Isi form dasar
```

### Langkah 2: Tambah Item
```
Scroll ke tab "Item" → [+ Add Line] → Isi detail barang
```

### Langkah 3: Finalize
```
Isi semua field required → [Finalize] → Done!
```

---

## 📋 DAFTAR FIELD PENTING

### Tab: Informasi Umum
```
PO Number           : Nomor unik pesanan
Name                : Deskripsi pesanan
Status              : Draft / Finalized
```

### Tab: Vendor
```
Vendor              : Pilih supplier
Vendor Ref. No      : Nomor referensi vendor
Contact Person      : Orang kontak di vendor
```

### Tab: Tanggal
```
Posting Date        : Tanggal PO dibuat (today)
Payment Date        : Tanggal pembayaran
Due Date            : Batas pembayaran
STA Date            : Estimasi barang tiba
```

### Tab: Pembayaran
```
Rate                : Kurs (jika transaksi forex)
Payment Terms       : Cash / Bank
Discount %          : Diskon keseluruhan
Tax                 : Persentase pajak
```

### Tab: Item (Purchase Order Content)
```
Item Code           : Kode 3-20 karakter (required)
Item Name           : Nama 3-75 karakter (required)
Free Text           : Deskripsi detail
Qty                 : Jumlah pesanan (required)
UOM                 : Satuan (PCS, KG, M3, dll)
Price               : Harga per unit (required)
Discount %          : Diskon per item
```

### Tab: Freight (Pengiriman)
```
Express Code        : Kode ekspedisi
Express Name        : Nama kurir/ekspedisi
Remarks             : Catatan pengiriman
Tax Code            : Kode pajak freight
Gross Amount        : Total biaya pengiriman
```

### Tab: Logistik
```
Ship To             : Negara tujuan
Pay To              : Bank penerima
Vessel/Flight       : Nama kapal/pesawat
Container           : Nomor container
```

### Tab: Lampiran (Attachment)
```
Attachment          : File dokumen (upload)
File Name           : Nama file yang jelas
File Size           : Otomatis
File Type           : Otomatis
```

---

## ✅ CHECKLIST FIELD WAJIB

Sebelum Finalize, pastikan ini sudah terisi:

```
WAJIB DIISI:
☑ PO Number
☑ Name/Deskripsi
☑ Vendor
☑ Posting Date
☑ Payment Terms
☑ Minimal 1 Item dengan:
  ☑ Item Code (3-20 char)
  ☑ Item Name (3-75 char)
  ☑ Quantity (> 0)
  ☑ Price (> 0)

PERLU DIISI (Tergantung):
□ Payment Date (jika sudah tahu)
□ Due Date (jika sudah tahu)
□ STA Date (jika sudah tahu)
□ Diskon (jika ada kesepakatan)
□ Tax (jika ada pajak)
□ Freight (jika ada biaya pengiriman)
□ Lampiran dokumen
```

---

## 🔢 PERHITUNGAN OTOMATIS

Sistem otomatis menghitung:

```
UNTUK SETIAP ITEM:
Total = Price - (Price × Discount%) 
Gross = Total × Qty

TOTAL PO:
SubTotal Item       = SUM(Gross semua item)
Total Setelah Disc  = SubTotal - (SubTotal × PO Disc%)
Jumlah Pajak        = Total × Tax%
TOTAL AKHIR         = Total + Pajak + Freight

ATTACHMENT COUNT:
Count = Jumlah file yang dilampirkan (otomatis)
```

---

## 📊 FORMAT CONTOH PENGISIAN

### Contoh Lengkap: PO Kayu Import

```
UMUM:
- PO Number       : PO-2025-001
- Name            : Pembelian Kayu Jati Grade A dari China
- Status          : Draft (akan jadi Finalized)

VENDOR:
- Vendor          : PT ABC Wood Trading
- Vendor Ref No   : VND-ABC-2025-100
- Contact Person  : Mr. Chen

TANGGAL:
- Posting Date    : 2025-01-15
- Payment Date    : 2025-02-10
- Due Date        : 2025-02-28
- STA Date        : 2025-02-05

PEMBAYARAN:
- Rate            : 15,500 (USD/IDR)
- Payment Terms   : Bank (L/C)
- Discount %      : 5%
- Tax             : 10%

ITEM 1:
- Item Code       : KD-KAY-001
- Item Name       : Kayu Jati Grade A - 4x8x2cm (Proses Palu)
- Free Text       : Finishing halus, bersertifikat
- Qty             : 50
- UOM             : PCS
- Packaging UOM   : Karton
- Packaging Qty   : 10
- Price           : 2,000,000 (Per PCS)
- Discount %      : 5%
- Tax Code        : PPN-10

ITEM 2:
- Item Code       : KD-KAY-002
- Item Name       : Kayu Jati Grade B - 3x6x2cm
- Qty             : 100
- UOM             : PCS
- Price           : 1,500,000 (Per PCS)
- Discount %      : 3%

FREIGHT:
- Express Code    : CONT-2025-001
- Express Name    : PT Semarang Cargo
- Remarks         : FCL, Port bongkar Tanjung Perak
- Tax Code        : PPN-10
- Gross Amount    : Rp 25,000,000

LOGISTIK:
- Ship To         : Indonesia
- Vessel          : MS Seatrade Cendrawasih
- Container       : CONT2025001

LAMPIRAN:
- File 1: Quotation-PT-ABC-Jan-2025.pdf
- File 2: Invoice-PT-ABC-INV-2025-001.pdf
- File 3: BoL-Container-CONT2025001.pdf
```

---

## 🎯 KODE SINGKAT (Shortcuts/Tips)

### Pengetikan Cepat
```
Item Code Template:
KD-[JENIS]-[NOMOR]

Contoh:
KD-KAY-001  (Kayu no 1)
KD-BES-005  (Besi no 5)
KD-SPA-010  (Spare Parts no 10)
KD-PLI-015  (Plastik no 15)
```

### Standar UOM
```
Panjang:    M, CM, MM
Berat:      KG, TON, GRAM, LB
Volume:     M3, LITER, GALLON
Jumlah:     PCS, SET, PAIR, DOZEN
Wadah:      BOX, KARTON, DRUM, PALLET
```

### Standar Payment Terms
```
Cash           = Tunai
Bank           = Transfer bank
2/10 Net 30    = Diskon 2% jika bayar 10 hari, max 30 hari
Net 30         = Bayar dalam 30 hari (tanpa diskon)
COD            = Cash On Delivery
```

---

## 📞 BANTUAN CEPAT

### Error Umum & Solusi

| Error | Solusi |
|-------|--------|
| "Nomor PO ada" | Gunakan nomor lain |
| "Vendor required" | Pilih vendor di field |
| "Item Code 3-20 char" | Sesuaikan panjang kode |
| "Qty > 0" | Gunakan quantity positif |
| "Price > 0" | Masukkan harga yang benar |
| "Discount 0-100" | Perbaiki persentase |

### Kontak Support
```
Pertanyaan teknis sistem  : Tim IT / Admin
Pertanyaan purchase       : Manager Procurement
Pertanyaan keuangan       : Divisi Finance
Pertanyaan vendor         : Vendor Relations
```

---

## 🗂️ STRUKTUR FILE LAMPIRAN

### Penamaan Standar
```
[TIPE]-[VENDOR/DETAIL]-[BULAN]-[TAHUN].pdf

Contoh:
Quote-PT-ABC-Jan-2025.pdf
Invoice-PT-ABC-INV-2025-001.pdf
BoL-Container-TCLU123456-Jan-2025.pdf
Packing-List-Shipment-001-Jan-2025.pdf
Quality-Cert-Batch-A-Jan-2025.pdf
```

### Dokumen Minimum
```
HARUS ADA:
✓ Quotation dari supplier
✓ Invoice (setelah order)
✓ BoL atau delivery note
✓ Quality cert/test report

OPTIONAL:
□ Email confirmations
□ Photos
□ Tech specs
□ Compliance docs
```

---

## 📈 METRIK TRACKING

Setelah PO Finalized, track:

```
□ PO Number
□ Vendor Name
□ Total Amount (Rp)
□ Order Date
□ ETA (Expected Delivery)
□ Status (Ordered/In Transit/Delivered)
□ Payment Status (Unpaid/Partial/Paid)
□ Notes/Issues
```

---

## 🔄 WORKFLOW DIAGRAM

```
START
  │
  ├─→ BUAT PO BARU
  │   (PO Number, Vendor, Basic Info)
  │
  ├─→ ISI ITEM DETAIL
  │   (Item Code, Name, Qty, Price)
  │
  ├─→ ISI PEMBAYARAN
  │   (Discount, Tax, Payment Terms)
  │
  ├─→ ISI PENGIRIMAN
  │   (Freight, Vessel, Container)
  │
  ├─→ LAMPIRKAN DOKUMEN
  │   (Quote, Invoice, BoL, etc)
  │
  ├─→ REVIEW & VERIFY
  │   (Check semua field, verifikasi total)
  │
  ├─→ APPROVAL (jika diperlukan)
  │   (Manager review & approval)
  │
  ├─→ FINALIZE
  │   (Status → Finalized)
  │
  ├─→ SEND TO VENDOR
  │   (Print atau email PO)
  │
  └─→ MONITOR STATUS
      (Track delivery, payment)
```

---

## 💾 TEMPLATE QUICK SAVE

Gunakan template ini untuk copy-paste:

```
PO NUMBER        : PO-[YYYY]-[NNN]
VENDOR           : [Pilih dari list]
POSTING DATE     : [Hari ini]
PAYMENT TERMS    : [Cash/Bank]
DUE DATE         : [Sesuai kesepakatan]

ITEM:
Item Code        : KD-[JENIS]-[NNN]
Item Name        : [Nama detail, min 3 char]
Qty              : [Angka positif]
UOM              : [PCS/KG/M3/etc]
Price            : [Harga per unit]
Discount %       : [0-100 jika ada]

FREIGHT:
Express Name     : [Nama kurir]
Gross Amount     : [Total biaya]
Vessel           : [Nama kapal/pesawat]
Container        : [Nomor container]

ATTACHMENT:
File 1           : [Quote dari vendor]
File 2           : [Invoice]
File 3           : [BoL/Delivery note]
```

---

## 🎓 SUMBER DAYA LENGKAP

Dokumentasi detail ada di:

| File | Topik |
|------|-------|
| 00_PANDUAN_MEMULAI.md | Pengenalan & alur kerja umum |
| 01_MEMBUAT_PESANAN_PEMBELIAN.md | Detail membuat PO |
| 02_DETAIL_ITEM_PESANAN.md | Mengelola item/barang |
| 03_INFORMASI_PENGIRIMAN.md | Freight & shipping |
| 04_LAMPIRAN_DAN_DOKUMEN.md | Attachment management |
| 05_TIPS_DAN_BEST_PRACTICES.md | Tips & trik penggunaan |
| 06_REFERENSI_CEPAT.md | Ini (quick reference) |

---

## 🎯 30 DETIK QUICK START

```
1. KLIK: Menu → Pesanan Pembelian → Create
2. ISI: PO Number, Name, Vendor, Posting Date
3. PILIH: Payment Terms
4. TAMBAH: Item (Code, Name, Qty, Price)
5. OPSIONAL: Freight, Lampiran
6. KLIK: Finalize
7. SELESAI!

Total waktu: ~5-10 menit per PO (dengan data ready)
```

---

## 📱 Akses Cepat

**Di Sistem:**
```
Search: "Purchase Order" 
atau 
Menu → Pesanan Pembelian PT
```

**Shortcut Keyboard (jika tersedia):**
```
Ctrl+S       = Save
Ctrl+D       = Delete
Ctrl+P       = Print
Tab          = Next field
Shift+Tab    = Previous field
```

---

*Dokumentasi ini dibuat untuk Odoo 18 - Purchase Order Module*
*Versi: 1.0 | Last Updated: 2026*
