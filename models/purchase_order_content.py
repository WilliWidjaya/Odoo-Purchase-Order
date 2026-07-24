from odoo import api, fields, models

class PurchaseOrderContent(models.Model):
    _name = "purchase_order_content"
    _description = "Purchase Order Content"

    # ============ Main Information
    purchase_order_id = fields.Many2one('purchase_order')
    item_id = fields.Many2one('po_item')
    item_name = fields.Char(string = "Item Name")
    free_text = fields.Text(string = "Free Text")

    # ============ Quantity
    quantity_consider = fields.Integer(string = "Consider Qty")
    quantity = fields.Integer(string = "Qty")
    quantity_packaging = fields.Integer(string = "Packaging QTY")
    quantity_real = fields.Integer(string = "Qty PO Asli")

    # ============ Unit of Measurement
    packaging_uom = fields.Char(string = "Packaging UOM")
    uom = fields.Char(string = "UOM")

    # ============ Price, Discount, Taxes.
    price = fields.Float(string = "Price")
    discount_percentage = fields.Float(string = "Discount (%)")
    total = fields.Float(string = "Total", compute = "_calculate_total")

    tax_code = fields.Char(string = "Tax Code")
    taxline = fields.Char(string = "Taxline")
    pi_number = fields.Char(string = "PI Number")
    slaughterhouse = fields.Char(string = "Slaughterhouse")
    
    rate = fields.Float(string = "Rate")
    total_after_discount = fields.Float(string = "Price after discount")
    gross_after_discount = fields.Float(string = "Gross after discount")

    _sql_constraints = [
        # Check if item ID is not null
        ('poc_check_item_id_filled', 'CHECK(item_id IS NOT NULL)', 'Please fill in the item ID.'),
        # Check if item name is filled or not.
        ('poc_check_item_name_filled', 'CHECK(item_name IS NOT NULL)', 'Please fill the item name.'),
        # Check item name length
        ('poc_check_item_name_length', 'CHECK(LENGTH(item_name) <= 75 AND LENGTH(item_name) >= 3)', 'Item name length must be at least 3 characters, and at most 75 characters.'),
        # Check if discount percentage is >= 0 and <= 100
        ('poc_check_discount_percentage', 'CHECK(discount_percentage >= 0 AND discount_percentage <= 100)', 'Discount Percentage must be valid (Between 0 and 100)'),
        # Check if quantity is >= 0
        ('poc_check_quantity', 'CHECK(quantity >= 0)', 'Quantity must not be negative (>= 0)'),
        # Check if price is filled by checking if its > 0
        ('poc_check_price_filled', 'CHECK(price > 0)', 'Please fill in a price above or greater than zero.'),
        # Check if price is in the negatives
        ('poc_check_price_positive', 'CHECK(price >= 0)', 'Prices must be positive. (>= 0)'),
    ]

    @api.onchange('item_id')
    def _onchange_item_id(self):
        for i in self:
            if i.item_id.item_desc != "" or i.item_id.item_desc != False:
                i.item_name = i.item_id.item_desc
            else: 
                i.item_name = ""
            if i.item_id.supplier_uom != "" or i.item_id.supplier_uom != False:
                i.packaging_uom = i.item_id.supplier_uom
            else:
                i.packaging_uom = ""
            if i.item_id.tax_code != "" or i.item_id.supplier_uom != False:
                i.tax_code = i.item_id.tax_code
            else:
                i.tax_code = ""

    @api.depends('price', 'discount_percentage')
    def _calculate_total(self):
        for i in self:
            if i.discount_percentage > 0.0:
                i.total = (i.price - ((i.discount_percentage/100.0) * i.price))
            else:
                i.total = i.price
