from odoo import fields, models, api

class PoItem(models.Model):
    _name = "po_item"
    _description = "Purchase Order Item"

    name = fields.Char(compute = "change_display_name") # Ini bakal di hide dari user.

    item_code = fields.Char()
    item_desc = fields.Char() # Juga disebut sebagai item name.


    @api.depends('item_code')
    def change_display_name(self):
        self.name = self.item_code
