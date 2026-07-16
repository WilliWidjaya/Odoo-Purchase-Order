from odoo import fields, models

class ShippingLocation(models.Model):
    _name = "po_shipping_location"
    _description = "Purchase Order Shipping Location"

    name = fields.Text()
    
