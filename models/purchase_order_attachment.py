from odoo import fields, models

class PurchaseOrderAttachment(models.Model):
    _name = "purchase_order_attachment"
    _description = "Purchase Order Attachment"

    purchase_order_id = fields.Many2one('purchase_order')
    t_attachment = fields.Binary(string = "Attachment", attachment = True)

    file_name = fields.Char(string="File Name")
    file_Size = fields.Char(string="File Size")
    file_type = fields.Char(string="File Size")