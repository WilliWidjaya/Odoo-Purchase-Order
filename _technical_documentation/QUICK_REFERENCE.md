# 📋 QUICK REFERENCE GUIDE - Purchase Order PT Module

**Odoo 18 Purchase Order Module - Quick Reference & Cheat Sheet**

---

## 1. Module Overview at a Glance

| Aspek | Detail |
|-------|--------|
| **Module Name** | Purchase Order PT |
| **Odoo Version** | 18.0+ |
| **Models** | 4 (purchase_order, purchase_order_content, purchase_order_freight, purchase_order_attachment) |
| **Dependencies** | base module only |
| **Features** | PO management, item tracking, freight costs, PDF reports |
| **Author** | William Widjaya |
| **Status** | v1.0 - Stable |

---

## 2. Quick Model Reference

### Model 1: purchase_order (Main Model)

```python
# Primary Key
po_number: Unique identifier (min 5 chars)

# Vendor Info
vendor: Many2one → res.partner
vendor_ref_no: Text
contact_person: Many2one → res.partner

# Important Dates
posting_date: Date (required)
payment_date: Date
due_date: Date
sta_date: Date (Scheduled Time of Arrival)

# Financial Fields
rate: Float (exchange rate)
discount_percentage: Float (0-100%)
tax: Float (0-100%)

# Computed Totals (readonly)
total_before_disc: Float
discount_amount: Float
total_amount: Float
taxed_amount: Float

# Status & Remarks
status: Selection (draft / finalized)
remarks: Text

# Relations
purchase_contents: One2many → purchase_order_content
purchase_freights: One2many → purchase_order_freight
att_attachment: Many2many → ir.attachment
```

### Model 2: purchase_order_content (Items)

```python
# Identification
purchase_order_id: FK to purchase_order
item_id: Char (3-20 chars, required)
item_name: Char (3-75 chars, required)

# Quantities
quantity: Integer (>= 0, required)
quantity_consider: Integer
quantity_packaging: Integer
quantity_real: Integer

# Units
uom: Char (unit of measurement)
packaging_uom: Char

# Pricing
price: Float (> 0, required)
discount_percentage: Float (0-100%)
total: Computed (price after discount)

# Tax & Extra
tax_code: Char
rate: Float
pi_number: Char
```

### Model 3: purchase_order_freight

```python
# Identification
purchase_order_id: FK to purchase_order
express_id: Char (shipping code)
expense_name: Char (shipping name)

# Amount
gross_amount: Float

# Tax
tax_code: Char

# Notes
remarks: Text
```

### Model 4: purchase_order_attachment

```python
# Identification
purchase_order_id: FK to purchase_order

# File
t_attachment: Binary (file content)
file_name: Char
file_size: Char (typo: duplicated from file_name field)
file_type: Char
```

---

## 3. Field Constraints Quick Reference

### Purchase Order Constraints

| Field | Constraint | Message |
|-------|-----------|---------|
| po_number | NOT NULL | Fill PO number |
| po_number | LEN >= 5 | Min 5 characters |
| po_number | UNIQUE | Must be unique |
| name | NOT NULL | Fill name |
| name | 5-45 chars | Length check |
| vendor | NOT NULL | Select vendor |
| posting_date | NOT NULL | Fill posting date |
| rate | >= 0 | No negative |
| tax | 0-100% | Range check |
| discount_percentage | 0-100% | Range check |

### Item Constraints

| Field | Constraint |
|-------|-----------|
| item_id | NOT NULL, 3-20 chars |
| item_name | NOT NULL, 3-75 chars |
| price | > 0 (required) |
| quantity | >= 0 |
| discount_percentage | 0-100% |

---

## 4. Common SQL Queries

```sql
-- List all POs
SELECT id, po_number, name, status, total_amount 
FROM purchase_order 
ORDER BY posting_date DESC;

-- Find POs by vendor
SELECT * FROM purchase_order 
WHERE vendor = 15 
ORDER BY posting_date DESC;

-- POs in draft status
SELECT id, po_number, total_amount 
FROM purchase_order 
WHERE status = 'draft';

-- Total amount by vendor
SELECT vendor, SUM(total_amount) as total
FROM purchase_order 
GROUP BY vendor;

-- Items in specific PO
SELECT * FROM purchase_order_content 
WHERE purchase_order_id = 1;

-- Items with discount
SELECT item_id, item_name, price, discount_percentage, total
FROM purchase_order_content 
WHERE discount_percentage > 0;

-- Total freight costs
SELECT purchase_order_id, SUM(gross_amount) as total_freight
FROM purchase_order_freight 
GROUP BY purchase_order_id;
```

---

## 5. Python API Quick Commands

```python
# Create new PO
po = env['purchase_order'].create({
    'po_number': 'PO-2024-001',
    'name': 'Purchase Order Name',
    'posting_date': fields.Date.today(),
    'vendor': 1,  # partner ID
    'status': 'draft'
})

# Read single PO
po = env['purchase_order'].browse(1)
print(po.po_number, po.total_amount)

# Search POs
pos = env['purchase_order'].search([
    ('status', '=', 'draft'),
    ('posting_date', '>', '2024-01-01')
])

# Update PO
po.write({'status': 'finalized', 'remarks': 'Updated'})

# Delete PO
po.unlink()

# Add item to PO
item = env['purchase_order_content'].create({
    'purchase_order_id': po.id,
    'item_id': 'ITEM001',
    'item_name': 'Raw Material',
    'quantity': 100,
    'price': 50000.0
})

# Generate PDF report
po.template_create_purchase_report()

# Access related records
for item in po.purchase_contents:
    print(f"{item.item_name}: {item.total}")
```

---

## 6. Web Interface Navigation

### Menu Path
```
Main Menu → Purchase Order PT → Pages → Purchase Order
```

### Main Views Available
1. **List View**: Shows all POs in table format
2. **Form View**: Detailed PO entry/editing
3. **Kanban View**: (if configured) Visual board by status

### Form Tabs
```
┌─ Content         (Items purchased)
├─ Logistics       (Ship-to, Pay-to info)
├─ Freight         (Shipping costs)
├─ Attachment      (Document files)
└─ Additional      (Extra info for customs/shipping)
```

---

## 7. Report Generation

### Report Types

1. **Purchase Order Report (NEW)**
   - Button: "Create Purchase Order Report (NEW)"
   - Output: `/home/laptop-it/Downloads/example_purchasing.pdf`
   - Template: `template_purchase_order.html`

2. **Receiving Report (NEW)**
   - Button: "Create Receiving Report (NEW)"
   - Output: `/home/laptop-it/Downloads/example_receiving.pdf`
   - Template: `template_receiving_report.html`

3. **Old Format Reports**
   - Button: "OLD PO" or "OLD RECEIVING"
   - Uses: old template files

---

## 8. Financial Calculation Examples

### Example 1: Single Item

```
Item: 100 units @ Rp 10,000/unit
Discount: 5%

Calculation:
  Line Total = 100 × 10,000 = Rp 1,000,000
  Discount = 1,000,000 × 5% = Rp 50,000
  Result = 1,000,000 - 50,000 = Rp 950,000
```

### Example 2: Full PO

```
Items Total: Rp 1,000,000
PO Discount: 10% = Rp 100,000
After Discount: Rp 900,000
Tax (8%): Rp 72,000
TOTAL: Rp 972,000
```

---

## 9. Access Control Quick Reference

```csv
Model,Group,Create,Read,Write,Delete
purchase_order,user,✓,✓,✓,✓
purchase_order_content,user,✓,✓,✓,✓
purchase_order_freight,user,✓,✓,✓,✓
purchase_order_attachment,user,✓,✓,✓,✓
```

**Default Group**: `base.group_user` (all authenticated users)

---

## 10. Status Workflow

```
DRAFT              FINALIZED
  ↔────────────────↔

Draft Status:
  - Can edit all fields
  - Can add/delete items
  - Can delete PO
  - Can generate reports

Finalized Status:
  - Ideally read-only (recommend implementing)
  - Locked state for completed POs
  - Can revert to draft if needed
```

---

## 11. Installation Checklist (5 Minutes)

```bash
# Step 1: Copy module
cp -r purchase_order /path/to/odoo/addons/

# Step 2: Install dependencies
pip install Jinja2>=3.0 WeasyPrint>=60.0 reportlab>=4.0

# Step 3: Install system libs (Ubuntu/Debian)
sudo apt-get install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0

# Step 4: Restart Odoo
sudo systemctl restart odoo

# Step 5: Install module via UI
# Apps > Apps > Purchase Order PT > [Install]
```

---

## 12. File Structure

```
purchase_order/
├── __init__.py                              (1 line: from . import models)
├── __manifest__.py                          (dependencies, data files)
├── models/
│   ├── __init__.py                          (4 imports)
│   ├── purchase_order.py                    (~200 lines - main logic)
│   ├── purchase_order_content.py            (~80 lines - items)
│   ├── purchase_order_freight.py            (~15 lines - freight)
│   └── purchase_order_attachment.py         (~10 lines - attachments)
├── views/
│   ├── po_views.xml                         (~300 lines - form/list views)
│   └── po_menus.xml                         (~10 lines - menu structure)
├── security/
│   └── ir.model.access.csv                  (4 access rules)
├── templates/
│   ├── template_purchase_order.html         (HTML template)
│   ├── template_receiving_report.html       (HTML template)
│   ├── po_style.scss                        (New styling)
│   └── old_po_style.scss                    (Legacy styling)
└── static/
    └── src/
        ├── css/w3css.css                    (Framework)
        └── scss/stylesheet.scss             (Custom styles)
```

---

## 13. Common Error Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "PO number must be unique" | Duplicate po_number | Use unique identifier |
| "Please fill in a vendor" | Vendor field empty | Select vendor from list |
| "Price must be > 0" | Item price is 0 or negative | Enter positive price |
| "PDF not generated" | WeasyPrint missing | `pip install WeasyPrint` |
| "Field not found" | Database schema mismatch | Reinstall module |
| "Permission denied" | User not in group | Add user to group |

---

## 14. Useful Links & Resources

### Odoo Documentation
- [Odoo 18 Framework](https://www.odoo.com/documentation/18.0/)
- [ORM API Reference](https://www.odoo.com/documentation/18.0/developer/reference/orm.html)
- [Views & XML](https://www.odoo.com/documentation/18.0/developer/reference/addons/views.html)

### External Libraries
- [Jinja2 Template Docs](https://jinja.palletsprojects.com/)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Development Tools
- [DBeaver](https://dbeaver.io/) - Database IDE
- [Postman](https://www.postman.com/) - API Testing
- [VS Code Odoo Extensions](https://marketplace.visualstudio.com/items?itemName=trinhanhngoc.vscode-odoo)

---

## 15. Performance Tips

✅ **Do's**:
- Use computed fields for frequently accessed values
- Cache template renders if possible
- Batch create operations
- Index frequently searched fields
- Monitor database queries

❌ **Don'ts**:
- Don't create records in loops (use batch create)
- Don't fetch all records without limit
- Don't compute heavy calculations in loops
- Don't store large files uncompressed
- Don't log sensitive data

---

## 16. Security Best Practices

✅ **Do's**:
- Validate all input data
- Use parameterized SQL queries
- Restrict field access per role
- Audit sensitive operations
- Encrypt sensitive data

❌ **Don'ts**:
- Don't store passwords in code
- Don't disable security rules
- Don't trust user input
- Don't expose internal IDs
- Don't log sensitive information

---

## 17. Testing

### Unit Test Template

```python
from odoo.tests import TransactionCase

class TestPurchaseOrder(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.po_model = self.env['purchase_order']
    
    def test_create_po(self):
        po = self.po_model.create({
            'po_number': 'TEST001',
            'name': 'Test',
            'posting_date': fields.Date.today(),
            'vendor': 1,
        })
        self.assertEqual(po.po_number, 'TEST001')
```

---

## 18. Developer Quick Commands

```bash
# Start Odoo in debug mode
odoo --dev=all -d odoo_db

# Run specific module tests
odoo -m purchase_order -t odoo_db

# Access Odoo shell
odoo shell -d odoo_db

# Generate module manifest
grep -A 20 "'data'" __manifest__.py

# Check database schema
python manage.py dbshell  # (or use psql directly)

# View logs in real-time
journalctl -u odoo -f
```

---

## 19. Documentation Files Included

This module comes with 4 comprehensive documentation files:

1. **DOKUMENTASI_TEKNIS.md** (Main Documentation)
   - Complete module overview
   - All model definitions
   - View architecture
   - Security configuration

2. **DOKUMENTASI_API_REFERENCE.md** (Developer Reference)
   - API endpoints
   - Method signatures
   - Code examples
   - Database schema

3. **PANDUAN_BISNIS_WORKFLOW.md** (Business Guide)
   - Business logic
   - Financial calculations
   - Workflows & scenarios
   - Use cases

4. **PANDUAN_DEPLOYMENT_KONFIGURASI.md** (DevOps Guide)
   - Installation steps
   - Configuration
   - Troubleshooting
   - Performance tuning

---

## 20. Support & Contact

**For Issues**:
- Check documentation files first
- Review error logs in `/var/log/odoo/odoo.log`
- Search similar issues in Odoo community
- Contact module author

**For Customization**:
- Extend models using `_inherit`
- Override methods with `super()`
- Create custom modules as dependencies

---

**Quick Reference Guide - End**

*Last Updated: 2024 | Odoo 18 Framework*

