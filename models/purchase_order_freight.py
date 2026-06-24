from odoo import api, fields, models, exceptions

class PurchaseOrderFreight(models.Model):
    _name = "purchase_order_freight"
    _description = "Purchase Order Freight"

    purchase_order_id = fields.Many2one('purchase_order')
    express_id = fields.Char(string = "Express Code")
    expense_name = fields.Char(string = "Express Name")
    remarks = fields.Text(string = "Remarks")
    tax_code = fields.Char(string = "Tax Code")
    gross_amount = fields.Float(string = "Gross Amount")
    

