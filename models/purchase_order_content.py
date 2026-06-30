from odoo import api, fields, models, exceptions

class PurchaseOrderContent(models.Model):
    _name = "purchase_order_content"
    _description = "Purchase Order Content"

    purchase_order_id = fields.Many2one('purchase_order')
    item_id = fields.Char(string = "Item Code")
    item_name = fields.Char(string = "Item Name")
    free_text = fields.Text(string = "Free Text")

    quantity_consider = fields.Integer(string = "Consider Qty")
    quantity = fields.Integer(string = "Qty")
    quantity_packaging = fields.Integer(string = "Packaging QTY")
    quantity_real = fields.Integer(string = "Qty PO Asli")

    packaging_uom = fields.Char(string = "Packaging")
    uom = fields.Char(string = "uom")

    price = fields.Float(string = "Price")
    discount_percentage = fields.Float(string = "Discount (%)")
    total = fields.Float(string = "Total", compute = "_calculate_total")

    tax_code = fields.Char(string = "Tax Code")
    taxline = fields.Char(string = "Taxline")
    # warehouse??? = fields.Text(string = "Warehouse")
    pi_number = fields.Char(string = "PI Number")
    slaughterhouse = fields.Char(string = "Slaughterhouse")
    
    rate = fields.Float(string = "Rate")
    total_after_discount = fields.Float(string = "Price after discount")
    gross_after_discount = fields.Float(string = "Gross after discount")

    # linestat = fields.Text(string = "Linestat")
    # DocEntry Something yang gua belom terlalu tau apaan, maybe when I get a clear view of it.

    @api.depends('price', 'discount_percentage')
    def _calculate_total(self):
        for i in self:
            if i.discount_percentage > 0.0:
                i.total = (i.price - ((i.discount_percentage/100.0) * i.price))
            else:
                i.total = i.price
