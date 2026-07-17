from odoo import fields, models, api

class ShippingLocation(models.Model):
    _name = "po_shipping_location"
    _description = "Purchase Order Shipping Location"

    name = fields.Char(compute = "change_display_name")
    shipping_location = fields.Text()
    
    @api.depends('shipping_location')
    def change_display_name(self):
        for i in self:
            i.name = str(i.shipping_location)