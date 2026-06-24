from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _name = "purchase_order"
    _description = "Purchase Order"

    po_number = fields.Text(string = "Purchase Order No") # No Char

    # Vendor Information
    name = fields.Char(string = "Name")
    vendor = fields.Many2one('res.partner') # Nanti Isi
    vendor_ref_no = fields.Text(string = "Vendor Ref. No") # No Char
    contact_person = fields.Many2one('res.partner') # Nanti isi

    # Dates
    posting_date = fields.Date(string = "Posting Date")
    payment_date = fields.Date(string = "Payment Date")
    due_date = fields.Date(string = "Due Date")
    sta_date = fields.Date(string = "STA Date")

    # Payment Related
    rate = fields.Float(string = "Rate")
    payment_terms = fields.Selection(
        string = 'Payment Terms',
        selection = [('pay_cash', 'Cash'), ('pay_bank', 'Bank')],
        help = "Tentukan Payment Terms"
    )
    total_before_disc = fields.Float(string = "Total Before Disc.", compute = "_calculate_total_before_discount")
    discount_percentage = fields.Float(string = "Discount Percentage")
    discount_amount = fields.Float(string = "Discounted Amount", readonly = True)
    tax = fields.Float(string = "Tax")

    total_amount = fields.Float(string = "Total Amount", readonly = True)

    # etc.
    status = fields.Selection(
        string = "Status",
        selection=[('draft', 'Draft'), ['finalized', "Finalized"]],
        help = "Tentukan Status Purchase Order"
    )
    remarks = fields.Text()

    #Content tab
    # TODO : This produces errors when added
    purchase_contents = fields.One2many(comodel_name="purchase_order_content", inverse_name="purchase_order_id")

    #Logistics
    ship_to = fields.Many2one('res.country')
    pay_to = fields.Many2one('res.bank')

    # WADIDAAAAWWWWWWW
    # tarlim
    # charitas
    # gonzaga

    #Freight
    purchase_freights = fields.One2many(comodel_name="purchase_order_freight", inverse_name="purchase_order_id")

    #Attachment
    att_attachment = fields.Many2many('ir.attachment')

    #Additional Informatio
    ad_vessel_flight = fields.Text(string = "Vessel/Flight")
    ad_container = fields.Text(string = "Container")
    ad_awb = fields.Text(string = "AWB No/ BI NO")
    ad_pesawat = fields.Text(string = "Pesawat")
    # Tulisan yang mirip dengan 'Karantina" & 'Karawitan'
    ad_vendor_DO_no = fields.Text(string = "Vendor DO No")
    ad_no_tanggal_PIB = fields.Text(string = "No dan tanggal PIB")
    ad_PIB_pesan = fields.Text(string = "PIB nomor pesan")
    ad_bank_name = fields.Text(string = "Bank Name")
    ad_pph = fields.Text(string = "PPH")
    ad_tgl_bbpcp = fields.Date()
    ad_total_cf = fields.Float(string = "Total CF") 
    ad_NDPBM = fields.Text(string = "NDPBM")
    ad_pi_date = fields.Date(string = "PI Date")
    ad_tgl_invoice = fields.Date(string = "Tanggal Invoice")

    _sql_constraints = [
        ('check_po_code', 'CHECK(po_number IS NOT NULL)', 'You must fill the PO number.'),
        ('check_po_length', 'CHECK(LENGTH(po_number) > 6)', 'Ermm PO must be longer than 5 or 6'),
        ('check_po_unique', 'UNIQUE(po_number)', 'PO number must be distinct or unique'),
        ('check_rate', 'CHECK(rate >= 0)', 'YOU GOTTA SET THIS RATE RIGHT BRO'),
        ('check_discount_percentage', 'CHECK(discount_percentage >= 0 AND discount_percentage <= 100)', 'Discount percentage must be between 0 and 100'),
    ]

    def count_total(self):
        count_total_amount = 0
        for i in self.purchase_contents:
            count_total_amount += i.price
        if count_total_amount == 0:
            self.total_amount = 0
            return
        if self.discount_percentage <= 0.00:
            self.total_amount = count_total_amount

        discounted_tottal = count_total_amount - ((self.discount_percentage/100.0) * count_total_amount)
        self.discount_amount = discounted_tottal
        self.total_amount = discounted_tottal

    @api.onchange('discount_percentage')
    def _calculate_on_discount_change(self):
        self.count_total()

    @api.depends('purchase_contents.total')
    def _calculate_total_before_discount(self):
        final_total_price = 0
        for i in self.purchase_contents:
            final_total_price += i.total
        
        # Calculate discount (different way from the function)
        final_discounted_price = 0
        if self.discount_percentage > 0.00:
            final_discounted_price = final_total_price - ((self.discount_percentage/100.0) * final_total_price)

        # NOTE : GUA GATAU INI HARUS KEK GINI ATO NGGA, PAKE FOR LOOOP ATO ENGGA
        #       Mungkin dia guasa di loop, tapi terakhir kali gua kena error karena gapake loop
        #       for some reason
        for i in self:
            i.total_before_disc = final_total_price
            i.discount_amount = final_discounted_price
            self.count_total()

    # @api.constrains('po_number')
    # def _check_po_number(self):
    #     if self.po_number == "":
    #         return 
    #     for i in self:
    #         if i.po_number == "":
    #             raise ValidationError("PO Number must not be empty.")
    #             return
    #         if len(i.po_number) < 6:
    #             raise ValidationError("PO Number must not be empty & longer than 5 characters")
    #             return