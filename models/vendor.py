from odoo import fields, models

class PoVendor(models.Model):
    _name = "po_vendor"
    _description = "Purchase Order Vendor"

    name = fields.Char()
    location = fields.Text()

