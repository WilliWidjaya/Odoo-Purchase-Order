# 🔧 DOKUMENTASI TEKNIS LANJUTAN - API & IMPLEMENTATION REFERENCE

**Purchase Order PT Module - Technical Implementation Guide**

---

## 1. Model API Reference

### 1.1 PurchaseOrder Model - Complete Reference

```python
from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _name = "purchase_order"
    _description = "Purchase Order"
    _order = "posting_date DESC, po_number DESC"
```

#### Instance Methods

##### A. Template Report Methods

```python
def template_create_receiving_report(self):
    """
    Generate Receiving Report as PDF using Jinja2 template
    
    Flow:
    1. Get module path using __file__
    2. Load template from templates/ directory
    3. Render template with PO data
    4. Convert HTML to PDF using WeasyPrint
    5. Save to Downloads folder
    6. Open in default browser
    
    Parameters:
        self: PurchaseOrder record instance
        
    Return:
        None (Opens PDF in browser)
        
    Output File:
        /home/laptop-it/Downloads/example_receiving.pdf
        
    Dependencies:
        - Jinja2: For template rendering
        - WeasyPrint: For HTML to PDF conversion
        - webbrowser: For opening PDF
        
    Template Variables Passed:
        name (str): PO name
        po_number (str): PO number
        date (str): Current date in DD-MM-YYYY format
        purchase_data (list): List of purchase_order_content records
        sub_total (str): Formatted subtotal
        discount (str): Formatted discount amount
        total (str): Formatted total after discount
        tax (str): Formatted tax amount
        grand_total (str): Formatted grand total
        remarks (str): PO remarks
        pi_no (str): PI number (empty)
        cont_awb_no (str): AWB number
        eta_jkt (date): STA date
        dated (date): Due date
        vendor_name (str): Vendor name
        vendor_location (str): Vendor location
        
    Stylesheet:
        - File: templates/po_style.scss
        - Format: SCSS (compiled to CSS by WeasyPrint)
        
    Error Handling:
        - FileNotFoundError: Jika template tidak ditemukan
        - weasyprint.CSS.CSSError: Jika ada error di CSS
        - IOError: Jika folder Downloads tidak dapat diakses
        
    Example Usage:
        po = self.env['purchase_order'].browse(1)
        po.template_create_receiving_report()
    """
    early_path = __file__
    def_filepath = str(Path(early_path).resolve().parent.parent)
    
    env = Environment(
        loader=FileSystemLoader(def_filepath + '/templates'),
        autoescape=select_autoescape()
    )
    template = env.get_template("template_receiving_report.html")
    
    template_render = template.render(
        name=self.name,
        po_number=self.po_number,
        date=self.grab_current_date(),
        purchase_data=self.grab_purchase_content(),
        sub_total=f"{round(self.total_before_disc,2):,.2f}",
        discount=f"{round(self.discounted_value,2):,.2f}",
        total=f"{round(self.discount_amount,2):,.2f}",
        tax=f"{round(self.taxed_amount,2):,.2f}",
        grand_total=f"{round(self.total_amount,2):,.2f}",
        remarks=self.remarks,
        pi_no="",
        cont_awb_no=self.ad_awb,
        eta_jkt=self.sta_date,
        dated=self.due_date,
        vendor_name=self.grab_vendor_name(),
        vendor_location=self.grab_vendor_location()
    )
    
    template_html = HTML(string=template_render)
    po_css = CSS(def_filepath + '/templates/po_style.scss')
    template_html.write_pdf(
        '/home/laptop-it/Downloads/example_receiving.pdf',
        stylesheets=[po_css]
    )
    webbrowser.open('/home/laptop-it/Downloads/example_receiving.pdf')


def template_create_purchase_report(self):
    """
    Generate Purchase Order Report as PDF using Jinja2 template
    
    Similar to template_create_receiving_report but uses different template
    
    Output File:
        /home/laptop-it/Downloads/example_purchasing.pdf
        
    Template File:
        templates/template_purchase_order.html
    """
    # Same structure as template_create_receiving_report
    # But uses template_purchase_order.html instead
    pass
```

##### B. Data Getter Methods

```python
def grab_current_date(self):
    """
    Format posting_date to DD-MM-YYYY format
    
    Parameters:
        self: PurchaseOrder record
        
    Return:
        str: Date in DD-MM-YYYY format
        
    Example:
        "07-07-2024"
        
    Logic:
        1. Get self.posting_date (datetime.date object)
        2. Convert to string (YYYY-MM-DD format)
        3. Parse using strptime with "%Y-%m-%d" format
        4. Reformat using strftime with "%d-%m-%Y" format
        5. Return formatted string
    """
    date_str = str(self.posting_date)
    formatted_time = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    return formatted_time


def grab_purchase_content(self):
    """
    Get list of purchase order content (items)
    
    Return:
        RecordSet: List of purchase_order_content records linked to this PO
        
    Usage in Template:
        {% for item in purchase_data %}
            <tr>
                <td>{{ item.item_id }}</td>
                <td>{{ item.item_name }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.price }}</td>
            </tr>
        {% endfor %}
    """
    return self.purchase_contents


def grab_vendor_name(self):
    """
    Get vendor name from Many2one relation
    
    Return:
        str: Vendor name (self.vendor.name)
    """
    return self.vendor.name


def grab_vendor_location(self):
    """
    Get vendor location/address
    
    Return:
        str: Vendor location (self.vendor.street, city, etc)
    """
    # Implementation should get full address from res.partner
    return f"{self.vendor.street}, {self.vendor.city}, {self.vendor.zip}"
```

##### C. Action Buttons (Not Yet Implemented - Incomplete)

```python
def count_total(self):
    """
    Button action: Send
    Purpose: (Not documented in code)
    Status: INCOMPLETE - Method referenced but not implemented
    """
    pass

def create_purchase_order_report(self):
    """
    Button action: OLD PO
    Purpose: Create using old template format
    Status: INCOMPLETE - Method referenced but not implemented
    """
    pass

def create_receiving_report(self):
    """
    Button action: OLD RECEIVING
    Purpose: Create receiving report using old format
    Status: INCOMPLETE - Method referenced but not implemented
    """
    pass
```

#### Computed Fields (Need Implementation)

```python
# These fields are marked as computed but actual compute method is NOT defined
attachment_count = fields.Integer(
    string="attachment_count",
    compute="_compute_attachment_amount"
)

# TODO: Need to implement
@api.depends('att_attachment')
def _compute_attachment_amount(self):
    """
    Calculate number of attachments
    
    Should be implemented as:
    """
    for record in self:
        record.attachment_count = len(record.att_attachment)
```

---

### 1.2 PurchaseOrderContent Model - API Reference

```python
class PurchaseOrderContent(models.Model):
    _name = "purchase_order_content"
    _description = "Purchase Order Content"
    _order = "id ASC"
```

#### Computed Fields

```python
@api.depends('price', 'discount_percentage')
def _calculate_total(self):
    """
    Calculate total price after discount
    
    Logic:
        if discount_percentage > 0.0:
            total = price - ((discount_percentage / 100.0) * price)
        else:
            total = price
    
    Triggered when:
        - price field changes
        - discount_percentage field changes
        
    Recalculation:
        - Automatic on save
        - Automatic when referenced field changes
        
    Example Calculation:
        price = 100.0
        discount_percentage = 10.0
        discount_amount = (10.0 / 100.0) * 100.0 = 10.0
        total = 100.0 - 10.0 = 90.0
    """
    for i in self:
        if i.discount_percentage > 0.0:
            i.total = (i.price - ((i.discount_percentage/100.0) * i.price))
        else:
            i.total = i.price
```

---

## 2. Field Definitions Deep Dive

### 2.1 Field Types & Properties

```python
# Text Field (unbounded)
po_number = fields.Text(
    string="Purchase Order No",
    copy=False  # Not copied when duplicating record
)

# Char Field (bounded)
name = fields.Char(
    string="Name",
    size=45  # VARCHAR(45) in database
)

# Date Field
posting_date = fields.Date(
    string="Posting Date"
)

# Float Field
rate = fields.Float(
    string="Rate"
)

# Many2one Field (FK to other table)
vendor = fields.Many2one(
    'res.partner',  # Model name (string or tuple)
    # Implicit: store=True, readonly=False
    # Implicit: ondelete='set null'
)

# Many2one with explicit params
contact_person = fields.Many2one(
    'res.partner',
    string="Contact Person",
    ondelete='cascade'  # Delete when related record deleted
)

# One2many Field (reverse of Many2one)
purchase_contents = fields.One2many(
    comodel_name="purchase_order_content",  # Target model
    inverse_name="purchase_order_id"  # Field name on target model
)

# Many2many Field
att_attachment = fields.Many2many(
    comodel_name="ir.attachment",
    # Creates junction table: purchase_order__ir_attachment
)

# Selection Field (ENUM-like)
status = fields.Selection(
    string="Status",
    selection=[
        ('draft', 'Draft'),
        ('finalized', 'Finalized')
    ],
    help="Tentukan Status Purchase Order"
)

# Computed Field (readonly, calculated on-the-fly)
total_before_disc = fields.Float(
    string="Total Before Disc.",
    compute="_calculate_total_before_discount"
    # readonly=True (implicit)
    # store=False (implicit, unless store=True added)
)

# Integer Field
quantity = fields.Integer(
    string="Qty"
)
```

### 2.2 Field Constraints & Validation

```python
# SQL Level Constraints
_sql_constraints = [
    # Format: (constraint_name, 'CHECK(condition)', 'error_message')
    
    # NOT NULL constraint
    ('check_po_code', 'CHECK(po_number IS NOT NULL)', 
     'You must fill the PO number.'),
    
    # Length constraint
    ('check_po_length', 'CHECK(LENGTH(po_number) >= 5)', 
     'PO must be longer than 5 or 6'),
    
    # Uniqueness constraint
    ('check_po_unique', 'UNIQUE(po_number)', 
     'PO number must be distinct or unique'),
    
    # Range constraint
    ('check_tax', 'CHECK(tax >= 0 AND tax <= 100)', 
     'The Tax Percentage must be reasonable.'),
    
    # Between constraint
    ('check_discount_percentage', 
     'CHECK(discount_percentage >= 0 AND discount_percentage <= 100)', 
     'Discount percentage must be between 0 and 100'),
]

# Python Level Constraints (Optional)
@api.constrains('discount_percentage')
def _check_discount(self):
    for record in self:
        if record.discount_percentage < 0 or record.discount_percentage > 100:
            raise ValidationError("Discount must be between 0-100%")
```

---

## 3. View Architecture

### 3.1 Form View Structure (XML)

```xml
<form string="Halaman Estate">
    <!-- Header dengan buttons -->
    <header>
        <button type="object" string="Send" name="count_total"/>
        <!-- type="object" = call method on model -->
        <!-- type="action" = execute action -->
    </header>
    
    <!-- Main content area -->
    <sheet>
        <!-- Use CSS classes for styling -->
        <group class="format-grid">
            <group class="format-bg">
                <!-- Field dengan custom label -->
                <span class="o_form_label o_td_label">
                    <div class="o_form_label_override">PO Number</div>
                </span>
                <div>
                    <field class="input-box" name="po_number" 
                           placeholder="e.g. PO2244001"/>
                </div>
            </group>
        </group>
        
        <!-- Tabs untuk sections yang berbeda -->
        <notebook>
            <page string="Content">
                <!-- One2many field untuk relasi -->
                <field name="purchase_contents"/>
            </page>
            <page string="Logistics">
                <!-- Many2one fields -->
                <group>
                    <field name="ship_to" placeholder="Select location..."/>
                    <field name="pay_to" placeholder="Select bank..."/>
                </group>
            </page>
        </notebook>
    </sheet>
</form>
```

### 3.2 List View (editable)

```xml
<list string="Channel" editable="bottom">
    <!-- editable="bottom" = create rows at bottom -->
    <!-- editable="top" = create rows at top -->
    
    <control>
        <create name="custom_line" string="Create new entry.."/>
    </control>
    
    <!-- Columns dengan width -->
    <field name="item_id" width="75px"/>
    <field name="item_name" width="125px"/>
    
    <!-- Calculated fields displayed in list -->
    <field name="total" width="75px"/>
</list>
```

---

## 4. Security & Access Control

### 4.1 CSV Security File Format

```csv
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
purchase_order.access_purchase_order,access_purchase_order,purchase_order.model_purchase_order,base.group_user,1,1,1,1
```

**Field Explanation:**
- `id`: Unique identifier (format: module.name)
- `name`: User-friendly name
- `model_id/id`: Reference ke model (automatic: model_[model_name])
- `group_id/id`: User group yang mendapat akses
- `perm_read`: Read permission (1=yes, 0=no)
- `perm_write`: Write/Update permission
- `perm_create`: Create permission
- `perm_unlink`: Delete permission

### 4.2 Permission Groups

```python
# Groups defined in base module
base.group_user          # Regular users (authenticated)
base.group_admin         # Administrator
base.group_partner       # External users (portal)
base.group_no_one        # Nobody (used for disabled features)
```

---

## 5. PDF Generation Deep Dive

### 5.1 WeasyPrint Implementation

```python
from weasyprint import HTML, CSS
from pathlib import Path

# Load HTML from string
template_html = HTML(string=template_render)

# Load CSS from file
po_css = CSS('/path/to/po_style.scss')

# Generate PDF and save
template_html.write_pdf(
    output_path='/home/laptop-it/Downloads/example_receiving.pdf',
    stylesheets=[po_css],
    # Optional parameters:
    # uncompressed_pdf=False,
    # custom_metadata={'Author': 'Purchase Order Module'},
    # zoom=1.0
)
```

### 5.2 Jinja2 Template Engine

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Setup environment
env = Environment(
    loader=FileSystemLoader(template_directory),
    autoescape=select_autoescape()  # Auto-escape HTML special chars
)

# Load template
template = env.get_template("template_name.html")

# Render with context
rendered_html = template.render(
    variable1=value1,
    variable2=value2,
    # ... etc
)

# Template usage in HTML
# {{ variable }}                    - Output variable
# {% if condition %}...{% endif %} - Conditional
# {% for item in items %}...{% endfor %} - Loops
# {{ value|round(2) }}             - Filters (round to 2 decimals)
```

### 5.3 Template Data Flow

```
PurchaseOrder Record
    ↓
grab_current_date() → "07-07-2024"
grab_purchase_content() → [item1, item2, ...]
grab_vendor_name() → "PT Vendor Jaya"
... etc
    ↓
{variable: value, ...} Dictionary
    ↓
Jinja2 render(context_dict)
    ↓
HTML String
    ↓
WeasyPrint.HTML(string=html)
    ↓
CSS Stylesheet
    ↓
write_pdf(output_path)
    ↓
PDF File
```

---

## 6. Database Relations

### 6.1 Foreign Key Structure

```
purchase_order (Parent)
    │
    ├── [FK] vendor → res.partner.id
    ├── [FK] contact_person → res.partner.id
    ├── [FK] ship_to → res.country.id
    ├── [FK] pay_to → res.bank.id
    │
    ├── [One2Many] purchase_order_content (Child)
    │   └── [FK] purchase_order_id → purchase_order.id
    │
    ├── [One2Many] purchase_order_freight (Child)
    │   └── [FK] purchase_order_id → purchase_order.id
    │
    ├── [One2Many] purchase_order_attachment (Child)
    │   └── [FK] purchase_order_id → purchase_order.id
    │
    └── [Many2Many] ir.attachment (Junction Table)
        └── (Automatic junction table created)
```

### 6.2 Cascade & Delete Behavior

```python
# Default behavior (SET NULL)
vendor = fields.Many2one('res.partner')  # Jika vendor dihapus → null

# Explicit CASCADE
contact_person = fields.Many2one(
    'res.partner',
    ondelete='cascade'  # Jika contact_person dihapus → PO juga dihapus
)

# One2many dengan cascade
purchase_contents = fields.One2many(
    'purchase_order_content',
    'purchase_order_id',
    # Implikasi: Jika PO dihapus → semua purchase_contents dihapus
)
```

---

## 7. API Usage Examples

### 7.1 CRUD Operations

```python
# CREATE
po = self.env['purchase_order'].create({
    'po_number': 'PO2024001',
    'name': 'Pembelian Material',
    'posting_date': fields.Date.today(),
    'vendor': 1,  # res.partner ID
    'status': 'draft'
})

# READ (by ID)
po = self.env['purchase_order'].browse(1)
print(po.po_number)  # 'PO2024001'

# READ (Search)
pos = self.env['purchase_order'].search([
    ('status', '=', 'draft'),
    ('posting_date', '>=', '2024-01-01')
])
# Returns RecordSet

# UPDATE
po.write({
    'name': 'Updated Name',
    'status': 'finalized'
})

# DELETE
po.unlink()

# Batch operations
pos.write({'status': 'finalized'})  # Update all matching
pos.unlink()  # Delete all matching
```

### 7.2 Search & Domain

```python
# Search dengan domain
domain = [
    ('posting_date', '>', '2024-01-01'),
    ('total_amount', '>', 1000),
    ('status', '=', 'draft'),
    ('vendor', 'in', [1, 2, 3])  # OR condition
]
pos = self.env['purchase_order'].search(domain)

# Search dengan limit & offset
pos = self.env['purchase_order'].search(
    domain,
    limit=10,        # Ambil 10 record
    offset=20,       # Skip 20 record (untuk pagination)
    order='posting_date DESC'
)

# Count
count = self.env['purchase_order'].search_count(domain)
```

### 7.3 Accessing Related Records

```python
po = self.env['purchase_order'].browse(1)

# Access Many2one
vendor_name = po.vendor.name
vendor_email = po.vendor.email

# Access One2many
for item in po.purchase_contents:
    print(f"{item.item_name}: {item.quantity}")

# Access Many2many
for attachment in po.att_attachment:
    print(f"{attachment.name}: {attachment.file_size}")
```

### 7.4 Computed Field Access

```python
po = self.env['purchase_order'].browse(1)

# Accessing computed field triggers calculation
total = po.total_before_disc  # Calculated on access

# Manual trigger (useful in batch operations)
po._calculate_total_before_discount()
```

---

## 8. Common Errors & Solutions

### 8.1 Constraint Violations

```
ERROR: new row for relation "purchase_order" violates check constraint "check_po_length"

Solution:
    - po_number harus minimal 5 karakter
    - Cek input validation sebelum save

ERROR: duplicate key value violates unique constraint "check_po_unique"

Solution:
    - po_number harus unik
    - Gunakan unique ID generator atau timestamp
```

### 8.2 PDF Generation Errors

```
ModuleNotFoundError: No module named 'weasyprint'

Solution:
    pip install WeasyPrint>=60.0
    # System libs (Linux): cairo, pango, gdk-pixbuf, libffi

weasyprint.CSS.CSSError: Invalid CSS

Solution:
    - Validate SCSS syntax
    - Check for invalid CSS properties
    - Use standard CSS3 properties
```

### 8.3 Relation Errors

```
IntegrityError: (psycopg2.IntegrityError) insert or update on table 
"purchase_order" violates foreign key constraint "purchase_order_vendor_fkey"

Solution:
    - Vendor ID tidak ada di res.partner
    - Validate vendor record exists sebelum create
```

---

## 9. Performance Optimization

### 9.1 Query Optimization

```python
# BAD: N+1 query problem
pos = self.env['purchase_order'].search([])
for po in pos:
    print(po.vendor.name)  # Triggers separate query for each

# GOOD: Use select_related-like approach
pos = self.env['purchase_order'].search([])
pos_with_vendor = pos.with_prefetch()  # Pre-fetch relations
for po in pos_with_vendor:
    print(po.vendor.name)  # No additional query
```

### 9.2 Batch Operations

```python
# BAD: Individual saves
for po_data in po_list:
    self.env['purchase_order'].create(po_data)

# GOOD: Batch create
self.env['purchase_order'].create(po_list)
```

### 9.3 Computed Field Caching

```python
# Default: Computed fields not stored (calculated on access)
total_before_disc = fields.Float(
    string="Total Before Disc.",
    compute="_calculate_total_before_discount"
    # store=False (default)
)

# For frequently accessed fields: Store in database
total_before_disc = fields.Float(
    string="Total Before Disc.",
    compute="_calculate_total_before_discount",
    store=True  # Store hasil computed field
)
```

---

## 10. Testing Guide

### 10.1 Unit Test Example

```python
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestPurchaseOrder(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.po_model = self.env['purchase_order']
        self.partner_model = self.env['res.partner']
    
    def test_po_creation(self):
        """Test PO dapat dibuat dengan valid data"""
        po = self.po_model.create({
            'po_number': 'PO2024001',
            'name': 'Test PO',
            'posting_date': fields.Date.today(),
            'vendor': 1,
            'status': 'draft'
        })
        self.assertEqual(po.status, 'draft')
        self.assertEqual(po.po_number, 'PO2024001')
    
    def test_po_validation_short_number(self):
        """Test PO dengan nomor terlalu pendek ditolak"""
        with self.assertRaises(ValidationError):
            self.po_model.create({
                'po_number': 'PO',  # Terlalu pendek
                'name': 'Test',
                'posting_date': fields.Date.today(),
                'vendor': 1
            })
    
    def test_discount_calculation(self):
        """Test kalkulasi diskon item"""
        item = self.env['purchase_order_content'].create({
            'item_id': 'ITEM001',
            'item_name': 'Test Item',
            'quantity': 10,
            'price': 100.0,
            'discount_percentage': 10.0
        })
        # Expected: 100 - (10% of 100) = 90
        self.assertEqual(item.total, 90.0)
```

---

## 11. Manifest File Deep Dive

```python
{
    'name': 'Purchase Order PT',
    'version': '1.0',
    'author': 'William Widjaya',
    
    # Module Dependencies (loaded before this module)
    'depends': ['base'],
    
    # Data Files (XML files loaded during installation)
    'data': [
        'views/po_views.xml',      # View definitions
        'views/po_menus.xml',      # Menu structure
        'security/ir.model.access.csv',  # Access control
    ],
    
    # Asset Bundles (CSS/JS files)
    'assets': {
        # Frontend assets
        'web.assets_frontend': [
            'purchase_order/static/src/scss/stylesheet.scss',
            'purchase_order/static/src/**/*',  # All files
        ],
        # Backend assets
        'web.assets_backend': [
            'purchase_order/static/src/scss/stylesheet.scss',
            'purchase_order/static/src/**/*',
        ]
    },
    
    # Module type (True = standalone app, False = plugin)
    'application': True,
}
```

---

## Appendix: File References

| File | Lokasi | Fungsi |
|------|--------|--------|
| `__manifest__.py` | Root | Module metadata |
| `__init__.py` | Root | Package init |
| `__init__.py` | models/ | Import models |
| `purchase_order.py` | models/ | Main PO model |
| `purchase_order_content.py` | models/ | Item model |
| `purchase_order_freight.py` | models/ | Freight model |
| `purchase_order_attachment.py` | models/ | Attachment model |
| `po_views.xml` | views/ | View definitions |
| `po_menus.xml` | views/ | Menu structure |
| `ir.model.access.csv` | security/ | Access rules |
| `po_style.scss` | templates/ | New report style |
| `old_po_style.scss` | templates/ | Old report style |
| `template_purchase_order.html` | templates/ | New PO template |
| `template_receiving_report.html` | templates/ | New receiving template |
| `stylesheet.scss` | static/src/scss/ | Frontend style |
| `w3css.css` | static/src/css/ | W3.CSS framework |

---

**End of Technical Reference Document**

