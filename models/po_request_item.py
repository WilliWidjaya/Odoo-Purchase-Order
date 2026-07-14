from odoo import api, fields, models

class PurchaseOrderRequestItem(models.Model):
    _name = "po_request_item"
    _description = "Purchase Order Request"

    # Item Information
    po_request_id = fields.Many2one('po_request')
    name = fields.Char()
    description = fields.Char()
    department = fields.Char()
    quantity = fields.Integer()
    estimated_price = fields.Float()

    