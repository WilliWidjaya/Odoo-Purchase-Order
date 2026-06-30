from odoo import api, fields, models, exceptions

class PurchaseOrderAttachment(models.Model):
    _name = "purchase_order_attachment"
    _description = "Purchase Order Attachment"

    purchase_order_id = fields.Many2one('purchase_order')
    t_attachment : fields.Binary = fields.Binary(string = "Attachment", attachment = True)

    file_name = fields.Char(string="File Name")


    # @api.onchange('t_attachment')
    # def on_attachment_changed(self):
    #     self.file_name = self.t_attachment