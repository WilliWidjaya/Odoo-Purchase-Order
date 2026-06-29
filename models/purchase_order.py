from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from weasyprint import HTML, CSS

# For Opening the file after making the pdf
import os
import webbrowser

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

    # Sub Total
    total_before_disc = fields.Float(string = "Total Before Disc.", compute = "_calculate_total_before_discount")
    # Discount in Percentage
    discount_percentage = fields.Float(string = "Discount Percentage")
    # Discounted Value
    discounted_value = fields.Float(string = "Discounted Amount", readonly = True)
    # Total (before Tax)
    discount_amount = fields.Float(string = "Discounted Total", readonly = True)

    # Tax
    tax = fields.Float(string = "Tax") # Between 0.00 and 100.00, must not exceed the top and bottom threshold
    taxed_amount = fields.Float(string = "Amount to Tax")

    # Grand Total (post discount and post tax)
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
        ('check_tax', 'CHECK(tax >= 0 AND tax <= 100)', 'The Tax Percentage must be reasonable.'),
        ('check_discount_percentage', 'CHECK(discount_percentage >= 0 AND discount_percentage <= 100)', 'Discount percentage must be between 0 and 100'),
    ]

    # -------------------------------------------------

    def create_receiving_report(self):
        def_filepath = "/home/laptop-it/odoo_src/src/tutorials/"
        env = Environment(
        loader=FileSystemLoader(def_filepath + 'purchase_order/templates'),
        autoescape=select_autoescape()
        )
        template = env.get_template("receiving_report.html")
   
        # The part when It renders the things
        template_render = template.render(
            name = self.name,
            po_number = self.po_number,
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{self.total_before_disc:,}",
            discount = f"{self.discounted_value:,}",
            total = f"{self.discount_amount:,}",
            tax = f"{self.taxed_amount:,}",
            grand_total = f"{self.total_amount:,}"
        )

        template_html = HTML(string = template_render)
        po_css = CSS(def_filepath + 'purchase_order/templates/po_style.scss')
        w3css_css = CSS(def_filepath + 'purchase_order/static/src/css/w3css.css')
        template_html.write_pdf('/home/laptop-it/Downloads/da_example.pdf', stylesheets = [po_css, w3css_css])
        webbrowser.open('/home/laptop-it/Downloads/da_example.pdf')

    def test_jinja(self):
        def_filepath = "/home/laptop-it/odoo_src/src/tutorials/"
        env = Environment(
        loader=FileSystemLoader(def_filepath + 'purchase_order/templates'),
        autoescape=select_autoescape()
        )
        template = env.get_template("purchase_order.html")
   
        # The part when It renders the things
        template_render = template.render(
            name = self.name,
            po_number = self.po_number,
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{self.total_before_disc:,}",
            discount = f"{self.discounted_value:,}",
            total = f"{self.discount_amount:,}",
            tax = f"{self.taxed_amount:,}",
            grand_total = f"{self.total_amount:,}"
        )

        template_html = HTML(string = template_render)
        po_css = CSS(def_filepath + 'purchase_order/templates/po_style.scss')
        w3css_css = CSS(def_filepath + 'purchase_order/static/src/css/w3css.css')
        template_html.write_pdf('/home/laptop-it/Downloads/da_example.pdf', stylesheets = [po_css, w3css_css])
        webbrowser.open('/home/laptop-it/Downloads/da_example.pdf')

    def grab_purchase_content(self):
        return_dict = {}
        for i in self.purchase_contents:
            return_dict[i.item_id] = {}
            return_dict[i.item_id]["description"] = i.item_id + " -- " + i.item_name
            return_dict[i.item_id]["quantity"] = i.quantity
            return_dict[i.item_id]["price"] = f"{i.price:,}"
            return_dict[i.item_id]["total"] = f"{i.total:,}"
        return return_dict


    def test_weasyprint(self):
        HTML('/home/laptop-it/odoo_src/src/tutorials/purchase_order/templates/purchase_order.html').write_pdf('/home/laptop-it/Downloads/da_example.pdf')

    def create_report(self):
        return self.env.ref('purchase_order.report_purchase_order').report_action(self)

    def count_total(self):
        # self.total_amount must be the grand total of everything
        # this includes discount + tax + everything else that might be added in the future.
        count_total_amount = 0
        for i in self.purchase_contents:
            count_total_amount += i.price
        if count_total_amount == 0:
            self.total_amount = 0
            return
        if self.discount_percentage <= 0.00: # Put the Discounted Price here.
            self.discount_amount = count_total_amount
            self.discounted_value = 0

        self.discounted_value = (self.discount_percentage/100.0) * count_total_amount

        # Calculate the Discounter Price
        discounted_tottal = count_total_amount - self.discounted_value
        self.discount_amount = discounted_tottal

        self.taxed_amount = (self.tax / 100) * discounted_tottal

        # Calculate the grand total.
        # Calculate this from the discounted price + percentage of that discounted amount
        self.total_amount = discounted_tottal + self.taxed_amount

    @api.onchange('tax')
    def _calculate_on_tax_change(self):
        self.count_total()

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
            # i.discount_amount = final_discounted_price
            self.count_total()

# class PurchaseOrderReport(models.AbstractModel):
#     _name = "report.purchase_order.report_purchase_order_template"
#     _description = "null"

#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['purchase_order'].browse(docids)

#         summaries = {}
#         for i in docs:
#             summaries["po_id"] = i.po_number
#             summaries["name"] = i.name
#             summaries["total"] = i.total_amount

#         return {
#             'doc_ids' : docids,
#             'doc_model' : 'purchase_order',
#             'docs' : docs,
#             'summaries' : summaries,
#             'report_title' : 'Purchase Order'
#         }