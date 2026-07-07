# 📊 PANDUAN BISNIS & WORKFLOW - Purchase Order PT Module

**Business Logic, Workflows, dan Use Cases**

---

## 1. Business Logic Overview

### 1.1 Purchase Order Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    PO LIFECYCLE FLOW                            │
└─────────────────────────────────────────────────────────────────┘

    ┌────────────────────────┐
    │   1. Create PO         │ (status = draft)
    │                        │
    │ Isi data vendor,       │
    │ tanggal, dll           │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 2. Add Items/Content   │
    │                        │
    │ Tambah item pembelian  │
    │ Total otomatis hitung  │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 3. Add Freight Costs   │
    │ (Optional)             │
    │                        │
    │ Tambah biaya pengiriman│
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 4. Attach Documents    │
    │ (Optional)             │
    │                        │
    │ Upload invoice, etc    │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 5. Click [Update]      │
    │                        │
    │ Validate & calculate   │
    │ total amounts          │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 6. Generate Reports    │
    │                        │
    │ Create PDF (PO/Receiving)
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 7. Finalize PO         │
    │                        │
    │ Change status to       │
    │ "Finalized"            │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ 8. Send to Vendor      │
    │                        │
    │ Email/Print PO        │
    │ Track receiving        │
    └────────────────────────┘
```

### 1.2 Status State Machine

```python
"""
Status Transitions:
    draft → finalized  (Forward transition)
    finalized → draft  (Backward transition - untuk revisi)
    
No automatic transitions - harus manual melalui UI
"""

STATUSES = {
    'draft': {
        'description': 'Purchase Order dalam draft/pengerjaan',
        'editable': True,      # Semua field dapat diubah
        'can_transition_to': ['finalized', 'draft'],
        'can_delete': True,    # Dapat dihapus
    },
    'finalized': {
        'description': 'Purchase Order sudah final/locked',
        'editable': False,     # Tidak dapat diubah (ideally)
        'can_transition_to': ['draft'],
        'can_delete': False,   # Tidak dapat dihapus
    }
}
```

---

## 2. Financial Calculation Logic

### 2.1 Single Item Calculation

```
Item Example:
    Item ID: ITEM001
    Item Name: Raw Material
    Quantity: 100 unit
    UOM: kg
    Price: Rp 1.000/unit
    Discount: 5%

Step-by-step:
    1. Line Total = Price × Quantity
       = Rp 1.000 × 100 = Rp 100.000

    2. Discount Amount = Line Total × (Discount % / 100)
       = Rp 100.000 × (5 / 100) = Rp 5.000

    3. Line Total After Discount = Line Total - Discount Amount
       = Rp 100.000 - Rp 5.000 = Rp 95.000

Result: Rp 95.000 (displayed in 'total' field)
```

### 2.2 Purchase Order Total Calculation

```
Given:
    Item 1: Rp 95.000 (after discount)
    Item 2: Rp 190.000 (after discount)
    Freight 1: Rp 50.000
    Freight 2: Rp 25.000

Step 1: Calculate subtotal from items
    total_before_disc = 95.000 + 190.000 = Rp 285.000

Step 2: Apply PO-level discount
    discount_percentage = 10%
    discounted_value = Rp 285.000 × (10 / 100) = Rp 28.500
    discount_amount = Rp 285.000 - Rp 28.500 = Rp 256.500

Step 3: Add freight costs
    Note: Freight biasanya ditambahkan SEBELUM tax calculation
    subtotal_with_freight = Rp 256.500 + Rp 50.000 + Rp 25.000 
                          = Rp 331.500

    Actually, in current model, freight tidak ter-included dalam
    perhitungan total_amount. Ini mungkin bug atau feature?

Step 4: Apply tax
    tax = 10%
    taxed_amount = Rp 256.500 × (10 / 100) = Rp 25.650

Step 5: Calculate final total
    total_amount = Rp 256.500 + Rp 25.650 = Rp 282.150

Final Result:
    Sub Total:           Rp 285.000
    Discount:            Rp 28.500
    Total After Disc:    Rp 256.500
    Tax (10%):           Rp 25.650
    ─────────────────────────────
    GRAND TOTAL:         Rp 282.150
```

### 2.3 Current Implementation Note

⚠️ **ISSUE**: Model saat ini tidak menghitung freight dalam total amount.

Field yang ada:
```python
total_before_disc          # Calculated dari purchase_contents total
discounted_value           # total_before_disc * discount%
discount_amount            # total_before_disc - discounted_value
taxed_amount              # discount_amount * tax%
total_amount              # discount_amount + taxed_amount
```

**Missing Calculation:**
```python
# Seharusnya:
total_amount = (discount_amount + freight_costs) + taxed_amount

# Tetapi saat ini freight tidak ter-include
```

**Rekomendasi**: 
- Tambah `freight_total` calculated field
- Update `total_amount` untuk include freight

---

## 3. Data Input Validation

### 3.1 Field-Level Validations

| Field | Rule | Error Message |
|-------|------|---------------|
| po_number | NOT NULL | You must fill the PO number |
| po_number | LENGTH >= 5 | PO must be longer than 5 or 6 |
| po_number | UNIQUE | PO number must be distinct |
| name | NOT NULL | Please fill in [name] |
| name | 5 ≤ LENGTH ≤ 45 | Name must be between 5-45 chars |
| vendor | NOT NULL | Please fill in a vendor |
| posting_date | NOT NULL | Please fill posting date |
| rate | >= 0 | Rate must be >= 0 |
| tax | 0 ≤ value ≤ 100 | Tax must be 0-100% |
| discount_percentage | 0 ≤ value ≤ 100 | Discount 0-100% |

### 3.2 Item-Level Validations

| Field | Rule | Error Message |
|-------|------|---------------|
| item_id | NOT NULL | Please fill item ID |
| item_id | 3 ≤ LENGTH ≤ 20 | Item ID 3-20 chars |
| item_name | NOT NULL | Please fill item name |
| item_name | 3 ≤ LENGTH ≤ 75 | Item name 3-75 chars |
| price | > 0 | Price must be > 0 |
| price | >= 0 | Price must be >= 0 |
| quantity | >= 0 | Quantity must >= 0 |
| discount_percentage | 0 ≤ value ≤ 100 | Discount 0-100% |

### 3.3 Validation Sequence (on Save)

```
1. Field Value Type Check (Odoo Framework)
   └─ e.g., float field receives non-numeric → TypeError

2. SQL Constraint Check (Database Level)
   └─ If any CHECK constraint fails → psycopg2.IntegrityError

3. Foreign Key Check (Database Level)
   └─ If related record doesn't exist → IntegrityError

4. Python Constrains (if implemented)
   └─ Custom validation logic
```

---

## 4. Common Business Scenarios

### Scenario 1: Standard Purchase Flow

**Situasi**: PT membeli material dari vendor, dengan diskon dan pajak

**Steps**:
1. Create PO
   ```
   PO Number: PO-2024-001
   Vendor: PT Supplier Jaya
   Posting Date: 2024-07-07
   Due Date: 2024-08-07
   Status: draft
   ```

2. Add items
   ```
   Item 1: Raw Material A
   - Qty: 1000 kg
   - Price: Rp 50.000/kg = Rp 50.000.000
   - Discount: 10% = Rp 5.000.000
   - Total: Rp 45.000.000
   
   Item 2: Raw Material B
   - Qty: 500 kg
   - Price: Rp 75.000/kg = Rp 37.500.000
   - Discount: 5% = Rp 1.875.000
   - Total: Rp 35.625.000
   ```

3. PO-level discount & tax
   ```
   Sub Total: Rp 80.625.000
   PO Discount: 2% = Rp 1.612.500
   After Discount: Rp 79.012.500
   Tax (10%): Rp 7.901.250
   TOTAL: Rp 86.913.750
   ```

4. Generate report PDF
5. Change status to Finalized
6. Send to vendor

---

### Scenario 2: International Purchase dengan Freight

**Situasi**: Impor dari negara lain, ada biaya pengiriman & dokumentasi

**Additional Fields Used**:
```
Ship To: China
Pay To: Bank BRI
Freight:
  - Ocean Freight: Rp 10.000.000
  - Insurance: Rp 2.000.000
  - Documentation: Rp 1.000.000

Additional Info:
  - Vessel/Flight: SEATRADE LINE
  - Container: CONT123456
  - AWB No: 1234567890
  - PI Date: 2024-06-01
  - STA Date: 2024-07-15
```

**Special Fields**:
```
PIB No: 07.03.2024.00123
PIB Date: 07-07-2024
Vendor DO No: DO-2024-456
PPH 23: 2%
NDPBM: 01234567
```

---

### Scenario 3: Purchase Order Revision

**Situasi**: Vendor meminta perubahan qty/harga setelah PO dikirim

**Process**:
1. Find existing PO (status: finalized)
2. Change status back to draft
3. Edit item quantities or prices
4. Recalculate totals
5. Generate updated report
6. Change status back to finalized

---

## 5. Report Generation Workflow

### 5.1 PDF Report Architecture

```
┌─────────────────────────────────────────────────────┐
│          DATA RETRIEVAL (from Database)             │
│                                                      │
│  PurchaseOrder                                      │
│  ├─ po_number, name, posting_date, etc             │
│  ├─ purchase_contents (items)                      │
│  ├─ purchase_freights (costs)                      │
│  └─ Calculated: total_before_disc, tax, etc       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│       DATA TRANSFORMATION & FORMATTING              │
│                                                      │
│  grab_current_date()        → "07-07-2024"         │
│  grab_purchase_content()    → List of items        │
│  grab_vendor_name()         → "PT Vendor Jaya"     │
│  Format numbers             → "Rp 1.000.000,00"    │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│      TEMPLATE RENDERING (Jinja2)                    │
│                                                      │
│  template_purchase_order.html                       │
│  OR                                                 │
│  template_receiving_report.html                    │
│                                                      │
│  Variables substituted into template                │
│  Output: HTML string                               │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│      PDF GENERATION (WeasyPrint)                    │
│                                                      │
│  HTML string                                        │
│  + po_style.scss (styling)                         │
│  → write_pdf()                                      │
│                                                      │
│  Output: PDF file                                  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│      FILE OUTPUT & DISPLAY                         │
│                                                      │
│  Save: /home/laptop-it/Downloads/example_*.pdf    │
│  Display: Open in default browser                 │
└─────────────────────────────────────────────────────┘
```

### 5.2 Report Template Variables

```html
<!-- In template_purchase_order.html -->
<h1>{{ po_number }}</h1>
<p>Name: {{ name }}</p>
<p>Date: {{ date }}</p>  <!-- DD-MM-YYYY format -->

<!-- Item Table -->
<table>
  <thead>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Qty</th>
      <th>Price</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    {% for item in purchase_data %}
    <tr>
      <td>{{ item.item_id }}</td>
      <td>{{ item.item_name }}</td>
      <td>{{ item.quantity }}</td>
      <td>{{ item.price }}</td>
      <td>{{ item.total }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<!-- Totals -->
<div class="totals">
  <p>Sub Total: {{ sub_total }}</p>
  <p>Discount: {{ discount }}</p>
  <p>Total: {{ total }}</p>
  <p>Tax: {{ tax }}</p>
  <p>Grand Total: {{ grand_total }}</p>
</div>

<!-- Vendor Info -->
<p>Vendor: {{ vendor_name }}</p>
<p>Location: {{ vendor_location }}</p>

<!-- Shipping Info -->
<p>AWB No: {{ cont_awb_no }}</p>
<p>ETA: {{ eta_jkt }}</p>
<p>Due Date: {{ dated }}</p>
```

---

## 6. Integration Points

### 6.1 Dependencies dengan Modul Lain

```
purchase_order
    │
    ├─→ res.partner (Vendor & Contact)
    │   └─ Used for: Vendor lookup, contact info
    │
    ├─→ res.country (Shipping destination)
    │   └─ Used for: Ship-to country selection
    │
    ├─→ res.bank (Payment recipient)
    │   └─ Used for: Bank account selection
    │
    └─→ ir.attachment (File storage)
        └─ Used for: Document attachment storage
```

### 6.2 Data Exchange Points

| Modul | Data Exchange | Direction |
|-------|---------------|-----------|
| res.partner | Vendor master data | IN (read) |
| res.country | Country list | IN (read) |
| res.bank | Bank accounts | IN (read) |
| ir.attachment | Document files | BOTH (read/write) |
| Base module | User groups, permissions | IN (read) |

### 6.3 Potential Integration Scenarios

```python
# Scenario 1: Auto-create from Inventory Request
# (Future integration with purchase.order module)
def create_from_inventory_request(request_id):
    request = self.env['inventory.request'].browse(request_id)
    po = self.env['purchase_order'].create({
        'po_number': self._generate_po_number(),
        'name': request.name,
        'vendor': request.vendor.id,
        'posting_date': fields.Date.today(),
    })
    # Auto-add items from request
    for item in request.items:
        self.env['purchase_order_content'].create({
            'purchase_order_id': po.id,
            'item_id': item.item_id,
            'item_name': item.item_name,
            'quantity': item.quantity,
            'price': item.price,
        })
    return po

# Scenario 2: Auto-create Invoice from PO
def create_invoice_from_po(po_id):
    po = self.env['purchase_order'].browse(po_id)
    invoice_lines = []
    for item in po.purchase_contents:
        invoice_lines.append({
            'product_id': item.item_id,
            'quantity': item.quantity,
            'price_unit': item.price,
        })
    # Create invoice (requires account module)
    invoice = self.env['account.invoice'].create({
        'partner_id': po.vendor.id,
        'invoice_line_ids': invoice_lines,
    })
    return invoice
```

---

## 7. User Roles & Responsibilities

### 7.1 Role: Procurement Officer

**Permissions**: Create, Read, Write, Delete on all PO models

**Responsibilities**:
- Create Purchase Orders
- Add items & freight costs
- Set discount & tax
- Communicate with vendors
- Generate & send reports

**Typical Workflow**:
```
1. Receive material request from Production
2. Identify suitable vendor
3. Create PO in system
4. Add items & quantities
5. Set payment terms & dates
6. Generate PDF report
7. Send to vendor
8. Track delivery
9. Update status when received
```

### 7.2 Role: Finance Officer

**Permissions**: Read on all PO models, Write on financial fields only

**Responsibilities**:
- Review PO amounts
- Set appropriate tax rates
- Verify vendor bank accounts
- Track payment obligations

**Typical Workflow**:
```
1. Review pending POs
2. Verify discount & tax calculations
3. Approve payment terms
4. Set bank payment recipient
5. Generate financial reports
```

### 7.3 Role: Manager/Approver

**Permissions**: Read on all PO models

**Responsibilities**:
- Approve Purchase Orders
- Monitor spending
- Ensure vendor compliance
- Review reports

---

## 8. KPI & Metrics

### 8.1 Purchasing KPIs

```python
# KPI 1: Average PO Amount
avg_po_amount = SUM(total_amount) / COUNT(po)

# KPI 2: Average Lead Time
avg_lead_time = AVG(due_date - posting_date)

# KPI 3: On-time Delivery Rate
on_time = COUNT(WHERE delivery_date <= due_date) / COUNT(po)

# KPI 4: Discount Utilization
discount_savings = SUM(discounted_value)

# KPI 5: Vendor Performance
vendor_score = (on_time_rate * 0.4 + quality_score * 0.3 + 
                price_competitiveness * 0.3)
```

### 8.2 Dashboard Example

```
┌────────────────────────────────────────────────────┐
│         PURCHASE ORDER DASHBOARD                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  Total PO This Month: 25  |  Total Value: Rp 2B  │
│                                                    │
│  ┌──────────────────┐  ┌──────────────────┐      │
│  │ PO by Vendor     │  │ PO by Status     │      │
│  │ ────────────     │  │ ───────────      │      │
│  │ Vendor 1: 10 PO  │  │ Draft: 5         │      │
│  │ Vendor 2: 8 PO   │  │ Finalized: 20    │      │
│  │ Vendor 3: 7 PO   │  │                  │      │
│  └──────────────────┘  └──────────────────┘      │
│                                                    │
│  Average PO Value: Rp 80M                        │
│  Total Discount Received: Rp 150M                │
│  Average Lead Time: 15 days                      │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 9. Troubleshooting & Support

### 9.1 Common User Issues

**Issue**: "Save button tidak muncul"
```
Cause: Form masih dalam create mode
Solution: 
  - Isi semua required fields terlebih dahulu
  - Button akan muncul setelah field minimal terisi
```

**Issue**: "Tidak bisa edit field setelah Save"
```
Cause: Status adalah 'finalized'
Solution:
  - Change status ke 'draft' terlebih dahulu
  - Kemudian ubah field yang diinginkan
  - Change status kembali ke 'finalized'
```

**Issue**: "PDF tidak keluar / kosong"
```
Cause: 
  - WeasyPrint error
  - Template file tidak ditemukan
  - File path incorrect
Solution:
  - Check browser console untuk error
  - Verify template file exists
  - Check file permissions
```

### 9.2 System Administrator Actions

```python
# Admin action 1: Reset PO Status
po.write({'status': 'draft'})

# Admin action 2: Fix calculation
po._calculate_total_before_discount()

# Admin action 3: Bulk delete test data
draft_pos = self.env['purchase_order'].search([
    ('status', '=', 'draft'),
    ('posting_date', '<', '2024-01-01')
])
draft_pos.unlink()

# Admin action 4: Audit trail
po_audit = self.env['ir.model.data'].search([
    ('model', '=', 'purchase_order'),
    ('res_id', '=', po.id)
])
```

---

## 10. Best Practices

### 10.1 Data Entry

✅ **DO**:
- Use consistent PO numbering (e.g., PO-YYYY-MM-NNN)
- Set realistic due dates (not past dates)
- Always specify vendor before creating items
- Review total before finalizing

❌ **DON'T**:
- Use very long PO numbers (> 50 chars)
- Leave vendor field empty
- Set negative quantities
- Change po_number after finalization (duplicate key error)

### 10.2 Report Generation

✅ **DO**:
- Generate report before sending to vendor
- Check report for accuracy
- Verify all calculations
- Keep copies of generated PDFs

❌ **DON'T**:
- Generate report with incomplete data
- Modify PDF after generation
- Lose track of report versions

### 10.3 Vendor Management

✅ **DO**:
- Maintain accurate vendor contact info
- Keep vendor payment details updated
- Track vendor performance
- Regular vendor reviews

❌ **DON'T**:
- Use incomplete vendor master data
- Mix up similar vendor names
- Store sensitive data unencrypted

---

## Appendix: Sample Data

### Sample PO Record

```json
{
  "id": 1,
  "po_number": "PO-2024-001",
  "name": "Pembelian Material Baku",
  "vendor": 15,
  "vendor_ref_no": "SUP-2024-456",
  "contact_person": 22,
  "posting_date": "2024-07-07",
  "payment_date": "2024-07-14",
  "due_date": "2024-08-07",
  "sta_date": "2024-08-15",
  "rate": 15500.0,
  "payment_terms": "pay_bank",
  "discount_percentage": 5.0,
  "tax": 10.0,
  "total_before_disc": 500000000.0,
  "discounted_value": 25000000.0,
  "discount_amount": 475000000.0,
  "taxed_amount": 47500000.0,
  "total_amount": 522500000.0,
  "status": "finalized",
  "remarks": "Kirim sesuai jadwal yang disepakati",
  "ship_to": 44,
  "pay_to": 8,
  "ad_vessel_flight": "SEATRADE LINE",
  "ad_container": "CONT-123456",
  "ad_awb": "1234567890",
  "ad_pesawat": "GA-123",
  "ad_vendor_DO_no": "DO-2024-456",
  "ad_pi_date": "2024-06-01",
  "ad_tgl_invoice": "2024-07-01"
}
```

---

**End of Business Logic & Workflow Documentation**

