from odoo import fields, models, api

class PoItem(models.Model):
    _name = "po_item"
    _description = "Purchase Order Item"

    name = fields.Char(compute = "change_display_name") # Ini bakal di hide dari user.

    item_code = fields.Char()
    item_desc = fields.Char() # Juga disebut sebagai item name.

    # Value-value opsional yang dapat di set, yang akan dimasukkan ke dalam table
    supplier_uom = fields.Char()
    tax_code = fields.Char()

    @api.depends('item_code')
    def change_display_name(self):
        for i in self:
            i.name = i.item_code

