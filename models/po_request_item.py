from odoo import api, fields, models

class PurchaseOrderRequestItem(models.Model):
    _name = "po_request_item"
    _description = "Purchase Order Request"

    # Item Information
    po_request_id = fields.Many2one('po_request')

    # Item Basic Information
    item_id = fields.Many2one('po_item')
    description = fields.Char()

    department = fields.Char()
    quantity = fields.Integer()
    estimated_price = fields.Float()

    @api.onchange('item_id')
    def change_display_name(self):
        for i in self:
            i.description = i.item_id.item_desc
    