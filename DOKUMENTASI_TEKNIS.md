# 📋 DOKUMENTASI TEKNIS MODUL PURCHASE ORDER PT

**Odoo 18 - Purchase Order Management Module**

---

## 📑 DAFTAR ISI

1. [Informasi Umum](#informasi-umum)
2. [Struktur Modul](#struktur-modul)
3. [Model Data](#model-data)
4. [Konfigurasi Keamanan](#konfigurasi-keamanan)
5. [Interface Pengguna](#interface-pengguna)
6. [Fitur Utama](#fitur-utama)
7. [Dependency](#dependency)
8. [Instalasi & Konfigurasi](#instalasi--konfigurasi)

---

## 1. Informasi Umum

### Metadata Modul
| Properti | Nilai |
|----------|-------|
| **Nama Modul** | Purchase Order PT |
| **Versi** | 1.0 |
| **Penulis** | William Widjaya |
| **Framework** | Odoo 18 |
| **Tipe** | Aplikasi (Standalone) |
| **Database** | PostgreSQL |
| **Dependencies** | `base` |

### Deskripsi
Modul **Purchase Order PT** adalah aplikasi komprehensif untuk mengelola pesanan pembelian (purchase orders) dengan fitur lengkap termasuk:
- Manajemen data PO (Purchase Order)
- Tracking item/konten pembelian
- Manajemen biaya freight (pengiriman)
- Manajemen attachment dokumen
- Pembuatan report dalam format PDF

---

## 2. Struktur Modul

### 2.1 Struktur Folder

```
purchase_order/
├── __init__.py                          # Entry point modul
├── __manifest__.py                      # Metadata & konfigurasi
├── models/                              # Business logic layer
│   ├── __init__.py
│   ├── purchase_order.py                # Model utama PO
│   ├── purchase_order_content.py        # Model item/konten PO
│   ├── purchase_order_freight.py        # Model biaya pengiriman
│   └── purchase_order_attachment.py     # Model attachment file
├── views/                               # User interface layer
│   ├── po_menus.xml                     # Menu navigation
│   └── po_views.xml                     # Form & list views
├── security/                            # Access control
│   └── ir.model.access.csv              # Model access rules
├── templates/                           # Report templates
│   ├── template_purchase_order.html     # Template PO baru
│   ├── template_receiving_report.html   # Template receiving report baru
│   ├── old_purchase_order.html          # Template PO lama
│   ├── old_receiving_report.html        # Template receiving lama
│   ├── po_style.scss                    # Style report baru
│   └── old_po_style.scss                # Style report lama
└── static/                              # Asset statis
    └── src/
        ├── css/
        │   └── w3css.css                # W3.CSS Framework
        └── scss/
            └── stylesheet.scss          # Custom stylesheet
```

### 2.2 File Utama

| File | Fungsi |
|------|--------|
| `__manifest__.py` | Mendefinisikan metadata, menu, view, dan asset |
| `models/purchase_order.py` | Logika bisnis PO utama (perhitungan, report) |
| `models/purchase_order_content.py` | Logika item pembelian |
| `models/purchase_order_freight.py` | Logika biaya pengiriman |
| `models/purchase_order_attachment.py` | Logika manajemen file attachment |
| `views/po_views.xml` | Definisi form, list, dan kanban views |
| `views/po_menus.xml` | Struktur menu navigasi |
| `security/ir.model.access.csv` | Rule akses model berdasarkan group |

---

## 3. Model Data

### 3.1 Model: `purchase_order` (Tabel: purchase_order)

Model utama untuk menyimpan informasi Purchase Order.

#### Struktur Field

##### A. Identifikasi & Informasi Dasar
```python
po_number         : Text       # Nomor PO unik, minimal 5 karakter
name              : Char       # Nama PO (3-45 karakter), required
status            : Selection  # Draft / Finalized
remarks           : Text       # Catatan tambahan
```

##### B. Informasi Vendor
```python
vendor            : Many2one   # Relasi ke res.partner (required)
vendor_ref_no     : Text       # Nomor referensi vendor
contact_person    : Many2one   # Relasi ke res.partner (contact person)
```

##### C. Tanggal-Tanggal Penting
```python
posting_date      : Date       # Tanggal posting (required)
payment_date      : Date       # Tanggal pembayaran
due_date          : Date       # Tanggal jatuh tempo
sta_date          : Date       # Scheduled Time of Arrival
```

##### D. Finansial & Pembayaran
```python
rate              : Float      # Nilai tukar (>= 0)
payment_terms     : Selection  # Cash / Bank
discount_percentage : Float    # Diskon (0-100%)
tax               : Float      # PPH/PPN (0-100%)

# Calculated fields (readonly):
total_before_disc : Float      # Subtotal sebelum diskon
discounted_value  : Float      # Nilai diskon
discount_amount   : Float      # Total setelah diskon
taxed_amount      : Float      # Nilai yang dikenakan pajak
total_amount      : Float      # Total akhir (setelah diskon & pajak)
```

##### E. Relasi One2Many
```python
purchase_contents : One2many   # Ke purchase_order_content
purchase_freights : One2many   # Ke purchase_order_freight
att_attachment    : Many2many  # Ke ir.attachment
```

##### F. Logistik & Pengiriman
```python
ship_to           : Many2one   # Relasi ke res.country (tujuan pengiriman)
pay_to            : Many2one   # Relasi ke res.bank (penerima pembayaran)
```

##### G. Informasi Tambahan (Additional Information)
```python
ad_vessel_flight  : Text       # Nama kapal/penerbangan
ad_container      : Text       # Nomor container
ad_awb            : Text       # AWB No / BI No (dokumen pengiriman)
ad_pesawat        : Text       # Pesawat
ad_vendor_DO_no   : Text       # Nomor Delivery Order vendor
ad_no_tanggal_PIB : Text       # Nomor dan tanggal Pemberitahuan Impor Barang
ad_PIB_pesan      : Text       # PIB nomor pesan
ad_bank_name      : Text       # Nama bank
ad_pph            : Text       # Pajak penghasilan
ad_tgl_bbpcp      : Date       # Tanggal BBPCP (?)
ad_total_cf       : Float      # Total CF (Clearance Fee)
ad_NDPBM          : Text       # Nomor Identitas Produk Barang dan Jasa
ad_pi_date        : Date       # Tanggal PI (Proforma Invoice)
ad_tgl_invoice    : Date       # Tanggal Invoice
attachment_count  : Integer    # Computed: jumlah attachment
```

#### Constraints (SQL)

| Nama | Kondisi | Pesan Error |
|------|---------|-------------|
| check_po_code | po_number NOT NULL | PO number harus diisi |
| check_po_length | LENGTH(po_number) >= 5 | PO minimal 5-6 karakter |
| check_po_unique | UNIQUE(po_number) | PO number harus unik |
| check_rate | rate >= 0 | Rate harus >= 0 |
| check_tax | tax BETWEEN 0 AND 100 | Tax harus 0-100% |
| check_discount_percentage | discount_percentage BETWEEN 0 AND 100 | Diskon 0-100% |
| check_posting_date | posting_date NOT NULL | Posting date harus diisi |
| check_name_filled | name NOT NULL | Name harus diisi |
| check_name_length | LENGTH(name) BETWEEN 5 AND 45 | Name 5-45 karakter |
| check_vendor_filled | vendor NOT NULL | Vendor harus dipilih |

#### Method Utama

```python
def template_create_receiving_report(self):
    """
    Membuat report receiving dalam format PDF menggunakan template HTML
    - Menggunakan Jinja2 untuk rendering template
    - Menggunakan WeasyPrint untuk konversi HTML ke PDF
    - Output: /home/laptop-it/Downloads/example_receiving.pdf
    - Membuka file secara otomatis di browser
    """

def template_create_purchase_report(self):
    """
    Membuat report purchase order dalam format PDF menggunakan template HTML
    - Menggunakan Jinja2 untuk rendering template
    - Menggunakan WeasyPrint untuk konversi HTML ke PDF
    - Output: /home/laptop-it/Downloads/example_purchasing.pdf
    - Membuka file secara otomatis di browser
    """

def grab_current_date(self):
    """
    Mengambil tanggal posting dalam format DD-MM-YYYY
    Return: string tanggal terformat
    """

def grab_purchase_content(self):
    """
    Mengambil data item pembelian (purchase_contents)
    Return: list dari purchase_order_content records
    """

def grab_vendor_name(self):
    """
    Mengambil nama vendor
    Return: string nama vendor
    """

def grab_vendor_location(self):
    """
    Mengambil lokasi vendor
    Return: string lokasi vendor
    """

def count_total():
    """
    Button action untuk menghitung total (triggered dari UI)
    """

def create_purchase_order_report():
    """
    Button action untuk membuat report lama
    """

def create_receiving_report():
    """
    Button action untuk membuat receiving report lama
    """
```

---

### 3.2 Model: `purchase_order_content` (Tabel: purchase_order_content)

Model untuk menyimpan item-item yang dibeli dalam satu PO.

#### Struktur Field

##### A. Identifikasi & Relasi
```python
purchase_order_id : Many2one   # Relasi ke purchase_order (FK)
item_id           : Char       # Kode item (3-20 karakter, required)
item_name         : Char       # Nama item (3-75 karakter, required)
free_text         : Text       # Deskripsi bebas
```

##### B. Kuantitas
```python
quantity_consider : Integer    # Kuantitas yang dipertimbangkan
quantity          : Integer    # Kuantitas (>= 0, required)
quantity_packaging: Integer    # Kuantitas kemasan
quantity_real     : Integer    # Kuantitas PO asli
```

##### C. Unit Pengukuran (UOM)
```python
packaging_uom     : Char       # Satuan kemasan
uom               : Char       # Satuan dasar
```

##### D. Harga & Diskon
```python
price             : Float      # Harga satuan (> 0, required)
discount_percentage : Float    # Diskon (0-100%, required)
total             : Float      # Computed: harga setelah diskon
```

##### E. Pajak & Detail Khusus
```python
tax_code          : Char       # Kode pajak
taxline           : Char       # Baris pajak
rate              : Float      # Rate/kurs
total_after_discount : Float   # Total setelah diskon
gross_after_discount : Float   # Gross setelah diskon
```

##### F. Informasi Khusus
```python
pi_number         : Char       # Nomor PI (Proforma Invoice)
slaughterhouse    : Char       # Tempat pemotongan (khusus)
```

#### Constraints (SQL)

| Nama | Kondisi | Pesan Error |
|------|---------|-------------|
| poc_check_item_id_filled | item_id NOT NULL | Item ID harus diisi |
| poc_check_item_id_len | LENGTH(item_id) BETWEEN 3 AND 20 | Item ID 3-20 karakter |
| poc_check_item_name_filled | item_name NOT NULL | Item name harus diisi |
| poc_check_item_name_length | LENGTH(item_name) BETWEEN 3 AND 75 | Item name 3-75 karakter |
| poc_check_discount_percentage | discount_percentage BETWEEN 0 AND 100 | Diskon 0-100% |
| poc_check_quantity | quantity >= 0 | Quantity >= 0 |
| poc_check_price_filled | price > 0 | Price harus > 0 |
| poc_check_price_positive | price >= 0 | Price >= 0 |

#### Method Utama

```python
@api.depends('price', 'discount_percentage')
def _calculate_total(self):
    """
    Menghitung total harga setelah diskon
    Logic:
      - Jika discount_percentage > 0:
          total = price - (discount_percentage/100 * price)
      - Else:
          total = price
    """
```

---

### 3.3 Model: `purchase_order_freight` (Tabel: purchase_order_freight)

Model untuk menyimpan biaya pengiriman (freight costs) terkait PO.

#### Struktur Field

```python
purchase_order_id : Many2one   # Relasi ke purchase_order (FK)
express_id        : Char       # Kode kurir/express
expense_name      : Char       # Nama biaya pengiriman
remarks           : Text       # Catatan/keterangan
tax_code          : Char       # Kode pajak
gross_amount      : Float      # Total biaya bruto
```

#### Deskripsi Penggunaan
- Menyimpan berbagai jenis biaya pengiriman (shipping cost, insurance, etc)
- Dapat memiliki multiple freight records per PO
- Support untuk tax tracking

---

### 3.4 Model: `purchase_order_attachment` (Tabel: purchase_order_attachment)

Model untuk menyimpan file attachment terkait PO.

#### Struktur Field

```python
purchase_order_id : Many2one   # Relasi ke purchase_order (FK)
t_attachment      : Binary     # File binary (stored as attachment)
file_name         : Char       # Nama file
file_size         : Char       # Ukuran file
file_type         : Char       # Tipe file (note: field ini duplikat dari file_size)
```

#### Deskripsi
- Menyimpan dokumen tambahan: invoice, packing list, dll
- Menggunakan field Binary dengan `attachment=True` untuk storage efisien
- Support untuk multiple attachments per PO

---

## 4. Konfigurasi Keamanan

### 4.1 Access Control (ir.model.access.csv)

File: `security/ir.model.access.csv`

```csv
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
purchase_order.access_purchase_order,access_purchase_order,purchase_order.model_purchase_order,base.group_user,1,1,1,1
purchase_order.access_purchase_order_content,access_purchase_order_content,purchase_order.model_purchase_order_content,base.group_user,1,1,1,1
purchase_order.access_purchase_order_freight,access_purchase_order_freight,purchase_order.model_purchase_order_freight,base.group_user,1,1,1,1
purchase_order.access_purchase_order_attachment,access_purchase_order_attachment,purchase_order.model_purchase_order_attachment,base.group_user,1,1,1,1
```

### 4.2 Permission Matrix

| Model | Group | Read | Write | Create | Delete | Catatan |
|-------|-------|------|-------|--------|--------|---------|
| purchase_order | base.group_user | ✓ | ✓ | ✓ | ✓ | Full access untuk user |
| purchase_order_content | base.group_user | ✓ | ✓ | ✓ | ✓ | Full access untuk user |
| purchase_order_freight | base.group_user | ✓ | ✓ | ✓ | ✓ | Full access untuk user |
| purchase_order_attachment | base.group_user | ✓ | ✓ | ✓ | ✓ | Full access untuk user |

### 4.3 Security Best Practices
- Semua model dapat diakses oleh `base.group_user` (semua user yang terautentikasi)
- Untuk production, pertimbangkan membuat custom group dengan permission lebih spesifik
- Implementasikan field-level security jika ada data sensitif
- Audit log dapat diaktifkan di menu Settings > Audit Trails

---

## 5. Interface Pengguna

### 5.1 Menu Navigation

```
Purchase Order PT (Root Menu)
└── Pages
    └── Purchase Order List (po_list_action)
```

### 5.2 Views

#### A. List View - Purchase Order
**ID**: `po_attachment_list`
**Model**: `purchase_order`

| Kolom | Width | Tipe |
|-------|-------|------|
| po_number | 50px | Text |
| name | 50px | Char |
| due_date | 50px | Date |
| total_amount | 50px | Float |
| payment_terms | 50px | Selection |
| status | 50px | Selection |

#### B. List View - Purchase Order Content
**ID**: `po_content_view_list`
**Model**: `purchase_order_content`
**Mode**: Editable (bottom)

| Kolom | Width |
|-------|-------|
| item_id | 75px |
| item_name | 125px |
| free_text | 75px |
| quantity_consider | 75px |
| quantity_packaging | 75px |
| packaging_uom | 75px |
| quantity | 75px |
| uom | 75px |
| price | 75px |
| discount_percentage | 75px |
| total | 75px |
| tax_code | 75px |
| rate | 75px |
| total_after_discount | 75px |
| gross_after_discount | 75px |
| taxline | 75px |
| pi_number | 75px |
| slaughterhouse | 75px |
| quantity_real | 75px |

#### C. List View - Freight
**ID**: `po_freight_view_list`
**Model**: `purchase_order_freight`
**Mode**: Editable (bottom)

| Kolom |
|-------|
| purchase_order_id |
| express_id |
| expense_name |
| remarks |
| tax_code |
| gross_amount |

#### D. Form View - Purchase Order
**ID**: `po_form`
**Model**: `purchase_order`

##### Layout Header
```
┌─────────────────────────────────────────────┐
│ [Send] [Update]                             │
│ [OLD PO] [OLD RECEIVING]                    │
│ [Create Purchase Order Report (NEW)]        │
│ [Create Receiving Report (NEW)]             │
└─────────────────────────────────────────────┘
```

##### Sheet Structure - Grid Layout

**Bagian 1: Vendor Information**
- PO Number
- Vendor
- Name
- Contact Person
- Vendor Ref. No.

**Bagian 2: Dates**
- STA Date
- Posting Date
- Payment Date
- Due Date
- Rate

**Bagian 3: Financials**
- Discount (%)
- Tax
- Total Before Discount (readonly)
- Discount Amount (readonly)
- Total Amount (readonly)

**Bagian 4: Payment & Status**
- Payment Term
- Status
- Remarks (multi-line)

##### Notebook Pages

1. **Content Tab**
   - Field: purchase_contents (One2many)
   - Display: List editable inline

2. **Logistics Tab**
   - ship_to: Pilih negara tujuan
   - pay_to: Pilih bank penerima

3. **Freight Tab**
   - Field: purchase_freights (One2many)
   - Display: List editable inline

4. **Attachment Tab**
   - Field: att_attachment (Many2many)
   - Display: File browser

5. **Additional Tab**
   - Vessel/Flight
   - Container
   - AWB No/BI No
   - Pesawat
   - Vendor DO No
   - No dan tanggal PIB
   - PIB Nomor Pesan
   - Bank Name
   - PPH
   - Tanggal BBPCP
   - Total CF
   - NDPBM
   - PI Date
   - Tanggal Invoice

---

## 6. Fitur Utama

### 6.1 Perhitungan Finansial Otomatis

#### A. Total Sebelum Diskon
```python
total_before_disc = SUM(purchase_order_content.total)
```

#### B. Nilai Diskon
```python
discounted_value = total_before_disc * (discount_percentage / 100)
```

#### C. Total Setelah Diskon
```python
discount_amount = total_before_disc - discounted_value
```

#### D. Nilai yang Dikenakan Pajak
```python
taxed_amount = discount_amount * (tax / 100)
```

#### E. Total Akhir
```python
total_amount = discount_amount + taxed_amount
```

### 6.2 Pembuatan Report PDF

#### A. Report Receiving (Baru)
- **Trigger**: Button "Create Receiving Report (NEW)"
- **Action**: `template_create_receiving_report`
- **Output**: `/home/laptop-it/Downloads/example_receiving.pdf`
- **Template**: `templates/template_receiving_report.html`
- **Style**: `templates/po_style.scss`
- **Engine**: Jinja2 + WeasyPrint

#### B. Report Purchase Order (Baru)
- **Trigger**: Button "Create Purchase Order Report (NEW)"
- **Action**: `template_create_purchase_report`
- **Output**: `/home/laptop-it/Downloads/example_purchasing.pdf`
- **Template**: `templates/template_purchase_order.html`
- **Style**: `templates/po_style.scss`
- **Engine**: Jinja2 + WeasyPrint

#### C. Report Legacy (Lama)
- **Trigger**: Button "OLD PO" / "OLD RECEIVING"
- **Action**: `create_purchase_order_report` / `create_receiving_report`
- **Template**: `templates/old_purchase_order.html` / `templates/old_receiving_report.html`
- **Style**: `templates/old_po_style.scss`

### 6.3 Data Rendering untuk Report

Template menerima variable berikut:
```python
{
    'name': str,                           # Nama PO
    'po_number': str,                      # Nomor PO
    'date': str,                           # Tanggal (format DD-MM-YYYY)
    'purchase_data': list,                 # List item pembelian
    'sub_total': str,                      # Formatted dengan comma & 2 decimal
    'discount': str,                       # Formatted
    'total': str,                          # Formatted
    'tax': str,                            # Formatted
    'grand_total': str,                    # Formatted
    'remarks': str,                        # Catatan
    'pi_no': str,                          # PI number (kosong)
    'cont_awb_no': str,                    # AWB number
    'eta_jkt': date,                       # STA Date
    'dated': date,                         # Due Date
    'vendor_name': str,                    # Nama vendor
    'vendor_location': str                 # Lokasi vendor
}
```

---

## 7. Dependency

### 7.1 Dependencies Modul
```yaml
Base Module:
  - base: Core modul Odoo (untuk res.partner, res.country, res.bank, ir.attachment)
```

### 7.2 Python Dependencies
```
odoo>=18.0                  # Framework Odoo 18
psycopg2>=2.9              # PostgreSQL adapter
Jinja2>=3.0                # Template engine
WeasyPrint>=60.0           # HTML to PDF converter
reportlab>=4.0             # PDF generation (dependency of WeasyPrint)
```

### 7.3 External Resources Digunakan
```
- res.partner              # Untuk vendor & contact person
- res.country             # Untuk negara tujuan pengiriman
- res.bank                # Untuk bank penerima pembayaran
- ir.attachment           # Untuk file attachment
```

---

## 8. Instalasi & Konfigurasi

### 8.1 Pre-requisite

1. **Odoo 18 Installation**
   - Sudah terinstall dengan Python 3.10+
   - Database PostgreSQL berjalan

2. **Python Dependencies**
   ```bash
   pip install Jinja2>=3.0
   pip install WeasyPrint>=60.0
   pip install reportlab>=4.0
   ```

3. **System Libraries** (untuk WeasyPrint)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-cffi python3-brotli libffi-dev libcairo2 libpango-1.0-0 libpango-cairo-1.0-0 libgdk-pixbuf2.0-0

   # macOS
   brew install cairo pango gdk-pixbuf libffi

   # CentOS/RHEL
   sudo yum install python3-cffi cairo pango gdk-pixbuf libffi
   ```

### 8.2 Instalasi Modul

1. **Copy modul ke addon path**
   ```bash
   cp -r purchase_order /path/to/odoo/addons/
   ```

2. **Update apps list** (di Odoo UI)
   - Menu: Apps > Update Apps List
   - Tunggu proses selesai

3. **Install modul**
   - Menu: Apps > Apps
   - Search: "Purchase Order PT"
   - Klik: [Install]

### 8.3 Post-Installation Configuration

1. **Create Partners (Vendor)**
   - Menu: Contacts
   - Create new contact untuk vendor
   - Set address & payment info

2. **Create Bank Accounts**
   - Menu: Settings > Accounting > Bank Accounts
   - Add bank penerima pembayaran

3. **Configure Countries**
   - Data sudah ter-setup (dari base module)

4. **Set User Permissions**
   - Menu: Settings > Users & Companies > Users
   - Assign grup yang tepat untuk access PO

### 8.4 Testing Installation

```python
# Di Odoo shell:
from odoo import Command

# Test create PO
po = self.env['purchase_order'].create({
    'po_number': 'PO2024001',
    'name': 'Test Purchase Order',
    'posting_date': datetime.now().date(),
    'vendor': 1,  # res.partner ID
    'status': 'draft'
})

# Test create item
item = self.env['purchase_order_content'].create({
    'purchase_order_id': po.id,
    'item_id': 'ITEM001',
    'item_name': 'Test Item',
    'quantity': 10,
    'price': 100.0,
    'discount_percentage': 5.0
})

# Cek relasi
print(po.purchase_contents)  # Should show 1 item
```

---

## 9. Usage Guide untuk End User

### 9.1 Membuat Purchase Order Baru

1. Buka menu: **Purchase Order PT > Pages > Purchase Order**
2. Klik tombol **Create** (atau tekan Ctrl+K)
3. Isi form:
   - **PO Number**: Masukkan nomor unik (contoh: PO2024001)
   - **Vendor**: Pilih vendor dari dropdown
   - **Name**: Masukkan nama PO
   - **Posting Date**: Pilih tanggal posting
4. Isi tab **Dates** jika diperlukan
5. Isi tab **Content**: Tambah item pembelian
   - Klik **Create new entry**
   - Isi item details
6. Klik **Save**

### 9.2 Membuat Report PDF

1. Buka PO yang sudah dibuat
2. Pilih salah satu button report:
   - **Create Purchase Order Report (NEW)** → untuk report PO
   - **Create Receiving Report (NEW)** → untuk report receiving
3. File PDF otomatis dibuat di `/home/laptop-it/Downloads/`
4. File akan membuka di browser secara otomatis

### 9.3 Menambah Item Pembelian

1. Di tab **Content**, klik **Create new entry**
2. Isi fields:
   - Item Code, Item Name
   - Quantity, UOM, Price
   - Discount percentage (optional)
3. Total akan ter-hitung otomatis
4. Klik save (atau tekan Tab untuk move ke baris berikutnya)

### 9.4 Menambah Biaya Pengiriman (Freight)

1. Di tab **Freight**, klik **Create new entry**
2. Isi:
   - Express Code & Name
   - Gross Amount
   - Tax Code (optional)
3. Remarks dapat ditambahkan

---

## 10. Troubleshooting

### Masalah: WeasyPrint tidak ditemukan
**Solusi**:
```bash
pip install --upgrade WeasyPrint
# Jika masih error, install system dependencies
```

### Masalah: Report tidak keluar
**Solusi**:
- Cek console untuk error message
- Pastikan folder `/home/laptop-it/Downloads/` ada dan writable
- Cek permission direktori

### Masalah: Constraint error saat save
**Solusi**:
- Pastikan semua required fields sudah diisi
- Cek kembali format data (contoh: PO number minimal 5 karakter)
- Cek constraint message untuk detail error

### Masalah: Permission denied
**Solusi**:
- Cek user group di Settings > Users
- Ensure user ada di group yang punya access ke model
- Contact admin untuk tambah permission

---

## 11. Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                   │
│  (Views: Form, List, Kanban - XML based)               │
├─────────────────────────────────────────────────────────┤
│                     BUSINESS LOGIC                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  purchase_order                                   │  │
│  │  ├─ Financial calculations                       │  │
│  │  ├─ Report generation (Jinja2 + WeasyPrint)     │  │
│  │  └─ Data validation                             │  │
│  │                                                   │  │
│  │  purchase_order_content                          │  │
│  │  ├─ Price calculations                           │  │
│  │  └─ Discount computations                        │  │
│  │                                                   │  │
│  │  purchase_order_freight & attachment             │  │
│  │  └─ Data storage & relations                     │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                 DATABASE LAYER (PostgreSQL)             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ purchase_    │ │ purchase_    │ │ purchase_    │   │
│  │ order        │ │ order_       │ │ order_       │   │
│  │              │ │ content      │ │ freight      │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 12. Data Flow Diagram

```
User Input (Form)
       ↓
   Validation (SQL Constraints)
       ↓
   Save to Database
       ↓
   Compute Fields (_calculate_total, etc)
       ↓
   Display in UI
       ↓
   User clicks Report Button
       ↓
   Grab data (grab_current_date, grab_purchase_content, etc)
       ↓
   Jinja2 Template Rendering
       ↓
   WeasyPrint HTML → PDF
       ↓
   Save to Downloads folder
       ↓
   Open in Browser
```

---

## 13. Developer Notes

### 13.1 Extending the Module

Untuk menambah field baru:
```python
class PurchaseOrder(models.Model):
    _inherit = 'purchase_order'
    
    new_field = fields.Char(string="New Field")
```

Untuk override existing method:
```python
def template_create_purchase_report(self):
    # Custom logic
    super().template_create_purchase_report()
```

### 13.2 Adding Custom Buttons

```xml
<!-- di po_views.xml -->
<button type="object" string="My Action" name="my_custom_method"/>

# Dan di model:
def my_custom_method(self):
    # Custom logic
    pass
```

### 13.3 Computed Fields

```python
@api.depends('field1', 'field2')
def _compute_field3(self):
    for record in self:
        record.field3 = record.field1 + record.field2
```

---

## 14. Performance Considerations

1. **Database Indexes**: Fields seperti `po_number` dan `purchase_order_id` sudah unique/foreign key
2. **One2many Relations**: Dapat mempengaruhi performa jika banyak items
3. **PDF Generation**: WeasyPrint dapat lambat untuk large reports
4. **Report Caching**: Pertimbangkan untuk cache PDF jika diperlukan

---

## 15. Security Best Practices

1. ✓ Semua input divalidasi melalui constraints
2. ✓ Many2one relations enforce referential integrity
3. ⚠ TODO: Implementasi audit trail untuk tracking changes
4. ⚠ TODO: Encrypt sensitive data (bank info, etc)
5. ⚠ TODO: Implement advanced approval workflow

---

## Appendix A: Database Schema

### Table: purchase_order
```sql
CREATE TABLE purchase_order (
    id BIGINT PRIMARY KEY,
    po_number TEXT UNIQUE NOT NULL CHECK(LENGTH(po_number) >= 5),
    name VARCHAR(45) NOT NULL CHECK(LENGTH(name) BETWEEN 5 AND 45),
    vendor BIGINT NOT NULL,
    vendor_ref_no TEXT,
    contact_person BIGINT,
    posting_date DATE NOT NULL,
    payment_date DATE,
    due_date DATE,
    sta_date DATE,
    rate FLOAT CHECK(rate >= 0),
    payment_terms VARCHAR(20),
    total_before_disc FLOAT,
    discount_percentage FLOAT CHECK(discount_percentage BETWEEN 0 AND 100),
    discounted_value FLOAT,
    discount_amount FLOAT,
    tax FLOAT CHECK(tax BETWEEN 0 AND 100),
    taxed_amount FLOAT,
    total_amount FLOAT,
    status VARCHAR(20),
    remarks TEXT,
    ship_to BIGINT,
    pay_to BIGINT,
    ad_vessel_flight TEXT,
    ad_container TEXT,
    ad_awb TEXT,
    ad_pesawat TEXT,
    ad_vendor_DO_no TEXT,
    ad_no_tanggal_PIB TEXT,
    ad_PIB_pesan TEXT,
    ad_bank_name TEXT,
    ad_pph TEXT,
    ad_tgl_bbpcp DATE,
    ad_total_cf FLOAT,
    ad_NDPBM TEXT,
    ad_pi_date DATE,
    ad_tgl_invoice DATE,
    create_date DATETIME,
    write_date DATETIME,
    FOREIGN KEY (vendor) REFERENCES res_partner(id)
);
```

### Table: purchase_order_content
```sql
CREATE TABLE purchase_order_content (
    id BIGINT PRIMARY KEY,
    purchase_order_id BIGINT NOT NULL,
    item_id VARCHAR(20) NOT NULL CHECK(LENGTH(item_id) BETWEEN 3 AND 20),
    item_name VARCHAR(75) NOT NULL CHECK(LENGTH(item_name) BETWEEN 3 AND 75),
    free_text TEXT,
    quantity_consider INTEGER,
    quantity INTEGER CHECK(quantity >= 0),
    quantity_packaging INTEGER,
    quantity_real INTEGER,
    packaging_uom VARCHAR,
    uom VARCHAR,
    price FLOAT CHECK(price >= 0 AND price > 0),
    discount_percentage FLOAT CHECK(discount_percentage BETWEEN 0 AND 100),
    total FLOAT,
    tax_code VARCHAR,
    taxline VARCHAR,
    pi_number VARCHAR,
    slaughterhouse VARCHAR,
    rate FLOAT,
    total_after_discount FLOAT,
    gross_after_discount FLOAT,
    FOREIGN KEY (purchase_order_id) REFERENCES purchase_order(id)
);
```

---

**Dokumentasi Lengkap Purchase Order PT Module**  
*Odoo 18 Framework | Updated: 2024*

