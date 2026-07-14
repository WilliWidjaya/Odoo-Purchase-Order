from odoo import api, fields, models

class PurchaseOrderRequest(models.Model):
    _name = "po_request"
    _description = "Purchase Order Request"

    #Form title
    name = fields.Char()

    # Item Information
    request_items = fields.One2many(comodel_name="po_request_item", inverse_name="po_request_id")

    # Document Request Information
    document_no = fields.Char()
    revision_no = fields.Integer()
    valid_date = fields.Date()

    # Company Information, Time and Date.
    affiliated_one = fields.Many2one('res.partner')
    affiliated_two = fields.Many2one('res.partner')
    # affiliated_three = fields.Many2one('res.partner') 
    # affiliated_four = fields.Many2one('res.partner')

    def do_nothing(self):
        return