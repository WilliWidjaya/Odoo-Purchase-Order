from odoo import fields, models

class PoItem(models.Model):
    _name = "po_item"
    _description = "Purchase Order Item"

    item_id = fields.Char()


    def _compute_display_name(self):
        return super()._compute_display_name()
