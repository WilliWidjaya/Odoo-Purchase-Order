# 🚀 PANDUAN DEPLOYMENT & KONFIGURASI

**Purchase Order PT Module - Deployment, Installation, dan Configuration Guide**

---

## 1. Pre-Deployment Checklist

### 1.1 System Requirements

#### Hardware
- **Processor**: Intel i5 / Ryzen 5 minimum (modern CPU preferred)
- **RAM**: 8GB minimum (16GB recommended for production)
- **Storage**: 50GB SSD minimum (fast I/O critical for database)
- **Network**: 1Gbps connection (for business operations)

#### Software Stack
```
Operating System:
  ✓ Ubuntu 20.04 LTS / 22.04 LTS (recommended)
  ✓ Debian 11/12
  ✓ CentOS/RHEL 8+
  ✓ macOS 12+

Database:
  ✓ PostgreSQL 14+ (12+ minimum)
  
Python:
  ✓ Python 3.10+ (3.11 recommended)
  ✓ pip package manager
  
Web Server:
  ✓ Nginx or Apache2 (for reverse proxy)
```

### 1.2 Odoo Instance Pre-requisites

```bash
# Verify Odoo installation
$ odoo --version
# Expected output: odoo.py: 18.0 (or higher)

# Verify Python version
$ python3 --version
# Expected: Python 3.10.x or higher

# Verify PostgreSQL
$ psql --version
# Expected: psql 12+ (PostgreSQL version)

# Verify database connection
$ psql -U postgres -h localhost -c "SELECT version();"
# Should return PostgreSQL version info
```

### 1.3 Module Dependencies Check

```bash
# Required Python packages (verify installed)
$ pip list | grep -E "Jinja2|WeasyPrint|reportlab|Odoo"

# Expected output:
Jinja2                 3.0.0+
Odoo                   18.0.0+
WeasyPrint             60.0+
reportlab              4.0+
psycopg2-binary        2.9+
```

---

## 2. Installation Steps

### 2.1 Phase 1: Prepare Environment

#### Step 1.1: Install System Dependencies

```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libpq-dev \
    git

# For WeasyPrint (PDF generation)
sudo apt-get install -y \
    python3-cffi \
    python3-brotli \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpango-cairo-1.0-0 \
    libgdk-pixbuf2.0-0

# Verify installation
cairo-config --version
pkg-config --modversion pango
```

#### Step 1.2: Create Python Virtual Environment

```bash
# Navigate to project directory
cd /home/laptop-it/odoo18

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate environment
source venv/bin/activate
# or for Windows: venv\Scripts\activate

# Verify activation (should show prompt with (venv))
which python  # Should show path with venv/bin
```

#### Step 1.3: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install Odoo + dependencies
pip install odoo>=18.0

# Install specific packages for this module
pip install Jinja2>=3.0 WeasyPrint>=60.0 reportlab>=4.0

# Verify installation
pip list | grep -E "Odoo|Jinja2|WeasyPrint|reportlab"
```

### 2.2 Phase 2: Module Installation

#### Step 2.1: Copy Module to Addon Path

```bash
# Identify Odoo addon path
# Default locations:
# - /opt/odoo/addons
# - /home/user/odoo/addons
# - ~/.local/share/Odoo/addons

# Find your installation
$ find / -name "purchase_order" -type d 2>/dev/null
# or check odoo config file
$ grep addons_path ~/.odoorc
# or
$ grep addons_path /etc/odoo/odoo.conf

# Copy module to addon path
mkdir -p /path/to/odoo/addons
cp -r /home/laptop-it/odoo18/src/tutorials/purchase_order \
    /path/to/odoo/addons/

# Verify copy
ls -la /path/to/odoo/addons/purchase_order/
# Should show: __init__.py, __manifest__.py, models/, views/, etc.
```

#### Step 2.2: Set Permissions

```bash
# Ensure Odoo user can read the files
cd /path/to/odoo/addons/purchase_order

# Set owner to odoo user (if using system-wide Odoo)
sudo chown -R odoo:odoo /path/to/odoo/addons/purchase_order

# Or if using local development
chmod -R 755 /path/to/odoo/addons/purchase_order

# Make files readable
chmod -R 644 /path/to/odoo/addons/purchase_order/*.py
chmod -R 644 /path/to/odoo/addons/purchase_order/views/*.xml
```

### 2.3 Phase 3: Odoo Configuration

#### Step 3.1: Configure Odoo

```ini
# Edit /etc/odoo/odoo.conf or ~/.odoorc

[options]
# Add purchase_order to addons path
addons_path = /path/to/odoo/addons,/path/to/other/addons

# Database configuration
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo_password
db_name = odoo_db

# Server configuration
host = 0.0.0.0
port = 8069
workers = 4
limit_memory_soft = 2147483648
limit_memory_hard = 2684354560

# Logger
log_level = info
log_file = /var/log/odoo/odoo.log

# Security
secure_admin_password = your_secure_password
```

#### Step 3.2: Restart Odoo Server

```bash
# If using systemd
sudo systemctl restart odoo

# If running locally
$ odoo -c ~/.odoorc &

# Verify server is running
$ curl http://localhost:8069/web/
# Should return HTML (Odoo web interface)

# Check logs
$ tail -f /var/log/odoo/odoo.log
```

### 2.4 Phase 4: Module Loading

#### Step 4.1: Update App List

```bash
# Via web interface:
1. Login to Odoo (http://localhost:8069)
2. Go to Apps menu
3. Click "Update Apps List" button
4. Wait for loading...

# Or via command line:
odoo -c ~/.odoorc -i purchase_order -d odoo_db

# Or via Python API:
from odoo import Command
env = Command()
env['ir.module.module'].update_list()
```

#### Step 4.2: Install Module

```
Via Web Interface:
  1. Apps > Apps
  2. Search: "Purchase Order PT"
  3. Click on module card
  4. Click [Install] button
  5. Wait for installation complete

Via Command Line:
  $ odoo -i purchase_order -d odoo_db -c ~/.odoorc

Via Python Console:
  >>> module = env['ir.module.module'].search([
  ...   ('name', '=', 'purchase_order')
  ... ])
  >>> module.button_immediate_install()
```

#### Step 4.3: Verify Installation

```bash
# Check if module appears in installed list
$ odoo shell -d odoo_db
>>> installed = self.env['ir.module.module'].search([
...   ('state', '=', 'installed')
... ])
>>> 'purchase_order' in [m.name for m in installed]
True

# Check if models are registered
>>> self.env['purchase_order']
<class 'purchase_order.models.purchase_order.PurchaseOrder'>

# List all models from module
>>> self.env.registry._module_models.get('purchase_order')
['purchase_order', 'purchase_order_content', ...]
```

---

## 3. Post-Installation Configuration

### 3.1 Initial Data Setup

#### Step 1: Create Vendors

```
Odoo Interface:
  1. Contacts app
  2. Create Partner
     - Name: Vendor Name
     - Email: vendor@email.com
     - Phone: +62-xxx-xxx-xxxx
     - Address:
       - Street
       - City
       - Zip Code
       - Country
     - Bank Account (if needed)
     - Payment Terms
  3. Save
```

#### Step 2: Create Bank Accounts

```
Odoo Interface:
  1. Settings > Accounting > Bank Accounts
  2. Create Bank Account
     - Account Owner: Company
     - Account Number
     - Bank Code
     - Bank Name
     - Currency
  3. Save
```

#### Step 3: Configure Countries

```
Odoo Interface:
  1. Settings > General Settings > Countries
  2. Data already pre-loaded from base module
  3. Can search by name in PO form
```

### 3.2 User Permissions Setup

#### Step 1: Create User Groups (Optional)

```python
# Via Odoo UI or programmatically
# Settings > Users > Groups

group_procurement = self.env['res.groups'].create({
    'name': 'Procurement Officers',
    'category_id': self.env.ref('base.module_category_sales').id,
})

group_finance = self.env['res.groups'].create({
    'name': 'Finance Officers',
    'category_id': self.env.ref('base.module_category_accounting').id,
})
```

#### Step 2: Assign User to Group

```
Odoo Interface:
  1. Settings > Users & Companies > Users
  2. Select user
  3. Add to Groups:
     - Procurement Officers
     - Finance Officers
  4. Save
```

#### Step 3: Verify Access

```bash
# Test access with different user
$ odoo shell -d odoo_db -u <user_login>

>>> # Try to access models
>>> self.env['purchase_order'].search_read([], limit=5)
# Should return data if user has permission

>>> # Check group membership
>>> self.env.user.groups_id
# Should show assigned groups
```

### 3.3 Storage & File Configuration

#### Step 1: Setup Downloads Folder

```bash
# Create downloads folder for reports
mkdir -p /home/laptop-it/Downloads

# Set permissions
chmod 755 /home/laptop-it/Downloads

# Verify write access
touch /home/laptop-it/Downloads/test.txt
# Should not show permission error
```

#### Step 2: Configure PDF Template Path

```python
# In purchase_order.py models

# Current (hardcoded):
output_path = '/home/laptop-it/Downloads/example_receiving.pdf'

# Better (configurable):
output_dir = self.env['ir.config_parameter'].get_param(
    'purchase_order.pdf_output_dir',
    '/home/laptop-it/Downloads'
)
output_path = f"{output_dir}/example_receiving.pdf"
```

---

## 4. Database Management

### 4.1 Backup Strategy

#### Backup Database

```bash
# Full database backup (with data)
pg_dump -U odoo odoo_db > odoo_db_backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U odoo odoo_db | gzip > odoo_db_backup_$(date +%Y%m%d).sql.gz

# Backup with custom format (faster)
pg_dump -U odoo -F custom odoo_db > odoo_db_backup_$(date +%Y%m%d).dump

# Verify backup
gzip -t odoo_db_backup_*.sql.gz  # Should return no error
file odoo_db_backup_*.dump       # Should show "pg_dump data"
```

#### Backup Odoo Files

```bash
# Backup module files
tar -czf purchase_order_backup_$(date +%Y%m%d).tar.gz \
  /path/to/odoo/addons/purchase_order/

# Backup attachment files
tar -czf odoo_attachments_$(date +%Y%m%d).tar.gz \
  /path/to/odoo/filestore/odoo_db/
```

### 4.2 Restore from Backup

```bash
# Restore database
psql -U odoo odoo_db < odoo_db_backup_20240707.sql

# Or from custom format
pg_restore -U odoo -d odoo_db odoo_db_backup_20240707.dump

# Restore module files
tar -xzf purchase_order_backup_20240707.tar.gz \
  -C /path/to/odoo/addons/
```

### 4.3 Database Maintenance

```bash
# Analyze & optimize database
VACUUM ANALYZE;

# Reindex all tables
REINDEX DATABASE odoo_db;

# Check database size
SELECT pg_size_pretty(pg_database_size('odoo_db'));

# Check specific table size
SELECT pg_size_pretty(pg_total_relation_size('purchase_order'));
```

---

## 5. Performance Optimization

### 5.1 Database Optimization

```sql
-- Add indexes for frequently queried fields
CREATE INDEX idx_po_posting_date ON purchase_order(posting_date DESC);
CREATE INDEX idx_po_vendor ON purchase_order(vendor);
CREATE INDEX idx_po_status ON purchase_order(status);
CREATE INDEX idx_poc_po_id ON purchase_order_content(purchase_order_id);

-- Monitor slow queries
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- 1 second
SELECT pg_reload_conf();

-- Check existing indexes
SELECT * FROM pg_indexes 
WHERE tablename = 'purchase_order';
```

### 5.2 Odoo Configuration Optimization

```ini
# odoo.conf

# Cache configuration
max_cron_threads = 2
cron_interval = 300

# Database pool
db_pool_size = 50

# Worker configuration
workers = 4  # (CPU count * 2) + 1
worker_class = gevent

# Memory limits
limit_memory_soft = 2147483648   # 2GB
limit_memory_hard = 2684354560   # 2.5GB

# Session storage
session_storage = db
```

### 5.3 Application-Level Optimization

```python
# In models:

# Use select_related for related records
def grab_vendor_name(self):
    # Good: Pre-fetch vendor data
    vendor = self.with_prefetch().vendor
    return vendor.name

# Cache computed results (if store=True)
@api.depends('purchase_contents')
def _calculate_total_before_discount(self):
    # Add store=True to cache result
    pass

# Batch operations
def create_multiple_pos(self, po_list):
    # Better than individual creates
    return self.env['purchase_order'].create(po_list)
```

---

## 6. Monitoring & Logging

### 6.1 Odoo Logging Configuration

```ini
# odoo.conf

# Log level: debug, info, warning, error, critical
log_level = info

# Log file
log_file = /var/log/odoo/odoo.log

# Logging format
logfile_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s

# Max log file size (in MB)
log_handler = :INFO
```

### 6.2 View Logs

```bash
# Real-time log monitoring
tail -f /var/log/odoo/odoo.log

# Follow specific module
tail -f /var/log/odoo/odoo.log | grep purchase_order

# Check error logs
grep ERROR /var/log/odoo/odoo.log

# Count errors
grep -c ERROR /var/log/odoo/odoo.log

# Get errors with timestamps
grep "ERROR\|WARNING" /var/log/odoo/odoo.log | head -20
```

### 6.3 System Monitoring

```bash
# Monitor CPU & Memory
top -u odoo

# Monitor disk usage
df -h
du -sh /path/to/odoo/addons/purchase_order/

# Monitor database connections
psql -U odoo -d odoo_db -c \
  "SELECT count(*) as connections FROM pg_stat_activity;"

# Monitor open files
lsof -p $(pgrep -f "odoo.*purchase_order")
```

---

## 7. Troubleshooting Deployment

### 7.1 Common Installation Issues

#### Issue 1: Module not appearing in Apps list

**Symptoms**: Module tidak muncul setelah install

**Solutions**:
```bash
# 1. Force update apps list
odoo -i purchase_order -d odoo_db --force

# 2. Check file permissions
ls -la /path/to/odoo/addons/purchase_order/
# Should show rwxr-xr-x permissions

# 3. Check manifest file
cat /path/to/odoo/addons/purchase_order/__manifest__.py
# Verify JSON syntax

# 4. Check Odoo log
tail -100 /var/log/odoo/odoo.log | grep -i error
```

#### Issue 2: WeasyPrint not found

**Symptoms**: PDF generation fails with "ModuleNotFoundError"

**Solutions**:
```bash
# 1. Verify installation
pip show WeasyPrint

# 2. Reinstall
pip install --upgrade --force-reinstall WeasyPrint>=60.0

# 3. Install system dependencies
sudo apt-get install libcairo2 libpango-1.0-0 libpango-cairo-1.0-0

# 4. Check Python path
python -c "import weasyprint; print(weasyprint.__file__)"
```

#### Issue 3: Permission denied on file

**Symptoms**: "Permission denied" when accessing module files

**Solutions**:
```bash
# Check file ownership
ls -la /path/to/odoo/addons/purchase_order/

# Fix permissions (if Odoo user owns files)
sudo chown -R odoo:odoo /path/to/odoo/addons/purchase_order/

# Or make readable for all users
chmod -R 755 /path/to/odoo/addons/purchase_order/
```

#### Issue 4: Database connection error

**Symptoms**: "Could not connect to PostgreSQL"

**Solutions**:
```bash
# 1. Check PostgreSQL running
sudo systemctl status postgresql

# 2. Test connection
psql -U odoo -h localhost -d odoo_db -c "SELECT 1;"

# 3. Check odoo config
cat ~/.odoorc | grep db_

# 4. Verify credentials
# In /etc/odoo/odoo.conf or ~/.odoorc:
# db_host = localhost
# db_port = 5432
# db_user = odoo
# db_password = your_password
```

### 7.2 Debug Mode

```bash
# Run Odoo in debug mode
odoo --dev=all -d odoo_db -c ~/.odoorc

# Enable Python debugger
odoo -c ~/.odoorc --debug

# Enable SQL debug logging
# In Python console:
>>> import logging
>>> logging.getLogger('odoo.sql_db').setLevel(logging.DEBUG)
```

---

## 8. Production Deployment

### 8.1 Production Checklist

```
[ ] Database backups automated and tested
[ ] Security group rules configured
[ ] SSL/TLS certificates installed
[ ] Odoo running behind reverse proxy (Nginx)
[ ] Systemd service configured
[ ] Monitoring & alerting set up
[ ] Log rotation configured
[ ] User permissions properly assigned
[ ] API rate limiting configured
[ ] Data retention policies defined
```

### 8.2 Systemd Service File

```ini
# /etc/systemd/system/odoo.service

[Unit]
Description=Odoo ERP
After=postgresql.service

[Service]
Type=simple
User=odoo
Group=odoo
WorkingDirectory=/opt/odoo
ExecStart=/opt/odoo/venv/bin/python /opt/odoo/bin/odoo \
    -c /etc/odoo/odoo.conf
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable odoo
sudo systemctl start odoo
sudo systemctl status odoo
```

### 8.3 Nginx Reverse Proxy Configuration

```nginx
# /etc/nginx/sites-available/odoo

upstream odoo {
    server localhost:8069;
}

server {
    listen 80;
    server_name your.domain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your.domain.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/your.domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your.domain.com/privkey.pem;
    
    # Proxy settings
    location / {
        proxy_pass http://odoo;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

---

## 9. Upgrade & Maintenance

### 9.1 Module Upgrade

```bash
# Upgrade existing module
odoo -u purchase_order -d odoo_db -c ~/.odoorc

# Or via web interface:
# Settings > Apps > Purchase Order PT > [Upgrade]

# Verify upgrade
# Settings > Modules > Search "purchase_order"
# Check version number
```

### 9.2 Regular Maintenance

```bash
# Weekly
- Backup database
- Check log files for errors
- Monitor database size

# Monthly
- Review user activity
- Optimize database (VACUUM)
- Update system packages
- Check disk space

# Quarterly
- Full system backup
- Security audit
- Performance review
- User training/support
```

---

## 10. Rollback Plan

### 10.1 Rollback Procedure

```bash
# If module causes issues after installation:

# Step 1: Stop Odoo
sudo systemctl stop odoo

# Step 2: Restore database backup
psql -U odoo odoo_db < odoo_db_backup_20240706.sql

# Step 3: Remove module files
rm -rf /path/to/odoo/addons/purchase_order/

# Step 4: Restart Odoo
sudo systemctl start odoo

# Step 5: Verify system
# Check web interface loads correctly
# Check other modules still work
```

---

**End of Deployment & Configuration Guide**

