from odoo import api, fields, models, exceptions

class PurchaseOrderAttachment(models.Model):
    _name = "purchase_order_attachment"
    _description = "Purchase Order Attachment"

    purchase_order_id = fields.Many2one('purchase_order')
    t_attachment = fields.Binary(string = "Attachment", attachment = True)