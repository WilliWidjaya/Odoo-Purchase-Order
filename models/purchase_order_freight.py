from odoo import api, fields, models, exceptions

class PurchaseOrderFreight(models.Model):
    _name = "purchase_order_freight"
    _description = "Purchase Order Freight"

    purchase_order_id = fields.Many2one('purchase_order')
    express_id = fields.Many2one('po_express')
    express_name = fields.Char(string = "Express Name")
    remarks = fields.Text(string = "Remarks")
    tax_code = fields.Char(string = "Tax Code")
    gross_amount = fields.Float(string = "Gross Amount")
    

    @api.onchange('express_id')
    def on_express_change(self):
        for i in self:
            if i.express_id.express_name != "" or i.express_id.express_name != False:
                i.express_name = i.express_id.express_name
            if i.express_id.tax_code != "" or i.express_id.tax_code != False:
                i.tax_code = i.express_id.tax_code