from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime
import math

# For Opening the file after making the pdf
import os
from pathlib import Path
import webbrowser

#Logging for the file
import logging

class PurchaseOrder(models.Model):
    _name = "purchase_order"
    _description = "Purchase Order"

    po_number = fields.Char(string = "Purchase Order No", copy = False) # No Char

    # Vendor Information
    name = fields.Char(string = "Name")
    vendor = fields.Many2one('res.partner') # Nanti Isi
    vendor_ref_no = fields.Char(string = "Vendor Ref. No") # No Char
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

    #Freight
    purchase_freights = fields.One2many(comodel_name="purchase_order_freight", inverse_name="purchase_order_id")

    #Attachment
    att_attachment = fields.Many2many(comodel_name="ir.attachment")
    attachment_count = fields.Integer(string = "attachment_count", compute = "_compute_attachment_amount")

    #Additional Informatio
    ad_vessel_flight = fields.Char(string = "Vessel/Flight")
    ad_container = fields.Char(string = "Container")
    ad_awb = fields.Char(string = "AWB No/ BI NO")
    ad_pesawat = fields.Char(string = "Pesawat")
    # Tulisan yang mirip dengan 'Karantina" & 'Karawitan'
    ad_vendor_DO_no = fields.Char(string = "Vendor DO No")
    ad_no_tanggal_PIB = fields.Char(string = "No dan tanggal PIB")
    ad_PIB_pesan = fields.Char(string = "PIB nomor pesan")
    ad_bank_name = fields.Char(string = "Bank Name")
    ad_pph = fields.Char(string = "PPH")
    ad_tgl_bbpcp = fields.Date()
    ad_total_cf = fields.Float(string = "Total CF") 
    ad_NDPBM = fields.Char(string = "NDPBM")
    ad_pi_date = fields.Date(string = "PI Date")
    ad_tgl_invoice = fields.Date(string = "Tanggal Invoice")

    _sql_constraints = [
        ('check_po_code', 'CHECK(po_number IS NOT NULL)', 'You must fill the PO number.'),
        ('check_po_length', 'CHECK(LENGTH(po_number) >= 5)', 'Ermm PO must be longer than 5 or 6'),
        ('check_po_unique', 'UNIQUE(po_number)', 'PO number must be distinct or unique'),
        ('check_rate', 'CHECK(rate >= 0)', 'YOU GOTTA SET THIS RATE RIGHT BRO'),
        ('check_tax', 'CHECK(tax >= 0 AND tax <= 100)', 'The Tax Percentage must be reasonable.'),
        ('check_discount_percentage', 'CHECK(discount_percentage >= 0 AND discount_percentage <= 100)', 'Discount percentage must be between 0 and 100'),
        # Check Posting date
        ('check_posting_date','CHECK(posting_date IS NOT NULL)', 'Please fill in the posting date.'),
        # ---- CHECK NAME ----
        # Check if name is filled
        ('check_name_filled', 'CHECK(name IS NOT NULL)', 'Please fill in [name] for this entry.'),
        # Check is name is too short or too long
        ('check_name_length', 'CHECK(LENGTH(name) >= 5 AND LENGTH(name) <= 45)', 'Name must be between 3 and 45 characters.'), 
        # Check if vendor is filled or nah
        ('check_vendor_filled', 'CHECK(vendor IS NOT NULL)', 'Please fill in a vendor.')
    ]

    # ------------------------------ REPORT CREATION & RELATED CALCULATIONS

    def grab_download_folder(self):
        home_path = Path.home()
        downloads_path = home_path / "OdooDownloads"
        downloads_path.mkdir(parents = True, exist_ok=True)
        print("GRABBED DOWNLOAD PATH : ", downloads_path)
        return downloads_path


    def template_create_receiving_report(self):
        print("purchase_order.py STARTING RECEIVING REPORT")
        early_path = __file__ # __file__ points to this current .py file.
        print("EARLY PATH : ", early_path)
        def_filepath = Path(early_path).resolve().parent.parent # grab parent folder of our parent folder.
        
        print("FILEPATH : ", def_filepath) 

        env = Environment(
        loader=FileSystemLoader(str(def_filepath / "templates")),
        autoescape=select_autoescape()
        )
        template = env.get_template("template_receiving_report.html")

        template_render = template.render(
            # ========== Main Information, Table Information
            name = self.name,
            po_number = self.po_number,
            date = self.grab_current_date(),
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{round(self.total_before_disc,2):,.2f}",
            discount = f"{round(self.discounted_value,2):,.2f}",
            total = f"{round(self.discount_amount,2):,.2f}",
            tax = f"{round(self.taxed_amount,2):,.2f}",
            grand_total = f"{round(self.total_amount,2):,.2f}",
            remarks = self.remarks,
            # =========== Additional Information
            pi_no = "",
            cont_awb_no = self.ad_awb,
            eta_jkt = self.sta_date,
            dated = self.due_date,
            vendor_name = self.grab_vendor_name(),
            vendor_location = self.grab_vendor_location()
        )

        output_file_name = "example_receiving_" + datetime.now().strftime("%d%m%Y_%H%M%S")

        template_html = HTML(string = template_render)
        po_css = CSS(str(def_filepath / "templates" / "po_style.scss"))

        # Grab folder dari downloads
        output_folder_path = self.grab_download_folder()
        
        # Note, output_file_name itu di wrap jadi string lagi, in case dia berubah
        final_filepath = str(output_folder_path / output_file_name) + ".pdf"
        template_html.write_pdf(final_filepath, stylesheets = [po_css])
        
        webbrowser.open(final_filepath)

    def template_create_purchase_report(self):
        # Debugger
        _logger = logging.getLogger(__name__)

        early_path = __file__ # __file__ points to this current .py file.
        def_filepath = Path(early_path).resolve().parent.parent # grab parent folder of our parent folder.
        
        env = Environment(
        loader=FileSystemLoader(str(def_filepath / "templates")),
        autoescape=select_autoescape()
        )
        template = env.get_template("template_purchase_order.html")

        _logger.debug("Template location " + str(def_filepath))

        template_render = template.render(
            # ========== Main Information, Table Information
            name = self.name,
            po_number = self.po_number,
            date = self.grab_current_date(),
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{round(self.total_before_disc,2):,.2f}",
            discount = f"{round(self.discounted_value,2):,.2f}",
            total = f"{round(self.discount_amount,2):,.2f}",
            tax = f"{round(self.taxed_amount,2):,.2f}",
            grand_total = f"{round(self.total_amount,2):,.2f}",
            remarks = self.remarks,
            # =========== Additional Information
            pi_no = "",
            cont_awb_no = self.ad_awb,
            eta_jkt = self.sta_date,
            dated = self.due_date,
            vendor_name = self.grab_vendor_name(),
            vendor_location = self.grab_vendor_location()
        )

        output_file_name = "example_receiving_" + datetime.now().strftime("%d%m%Y_%H%M%S")

        template_html = HTML(string = template_render)
        po_css = CSS(str(def_filepath / "templates" / "po_style.scss"))

        # Grab folder dari downloads.
        output_folder_path = self.grab_download_folder()
        
        # Note, output_file_name itu di wrap jadi string lagi, in case dia berubah
        final_filepath = str(output_folder_path / output_file_name) + ".pdf"
        template_html.write_pdf(final_filepath, stylesheets = [po_css])
        
        _logger.debug("Final filepath " + str(final_filepath))

        webbrowser.open(final_filepath)


    # ------------------------------ END OF REPORT CREATION

    def debug_view_dependency(self):
        t_view = self.env['ir.ui.view'].search([('model', '=', 'purchase_order')])
        for v in t_view:
            _logger_msg = f"view: {v.name} | inherit_id: {v.inherit_id.name if v.inherit_id else None} | module: {v.inherit_id.module if v.inherit_id else None}"
            print(_logger_msg)

    # ------------------------------ DATA GETTER START
    
    def grab_current_date(self): # Get current date in dd-mm-yyyy format.
        date_str = str(self.posting_date)

        formatted_time = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
        print("FORMATTED TIME IS : "), formatted_time
        return formatted_time

    def grab_our_location(self): # Fill in later when needed.
        return 

    def grab_vendor_name(self): # Grab name of vendor from the vendor Many2One
        t_vendor = self.with_prefetch().vendor
        return t_vendor.name.upper()

    def grab_vendor_location(self): # Grabs vendor street1 address from vendor Many2One
        return self.vendor.street

    def grab_purchase_content(self): # Grabbing purchase_content One2Many
        return_dict = {}
        for i in self.purchase_contents:
            # Check if our real qty has been filled, if not, skip this part.
            supplier_real_qty_uom = 0.0
            our_qty_per_supply = 0.0
            if i.quantity_real != False:
                # Begin the logic here....
                # Mencari berapa uom kita equal to berapa uom mereka.
                if i.quantity != False and i.quantity_packaging != False:
                    if i.quantity == i.quantity_packaging:
                        our_qty_per_supply = 1.0
                        supplier_real_qty_uom = i.quantity_real
                    elif i.quantity > i.quantity_packaging:
                        our_qty_per_supply = i.quantity_packaging / i.quantity
                        supplier_real_qty_uom = i.quantity_real * our_qty_per_supply
                    elif i.quantity < i.quantity_packaging:
                        our_qty_per_supply = i.quantity_packaging / i.quantity 
                        supplier_real_qty_uom = i.quantity_real * our_qty_per_supply
                    else:
                        our_qty_per_supply = 0.0 # Default to this....
                        supplier_real_qty_uom = i.quantity_real

            supplier_real_qty_uom = f"{supplier_real_qty_uom:,.2f}"

            return_dict[i.item_id] = {}
            return_dict[i.item_id]["description"] = i.item_id + " -- " + i.item_name
            return_dict[i.item_id]["quantity"] = i.quantity
            return_dict[i.item_id]["price"] = f"{i.price:,.2f}" 
            return_dict[i.item_id]["total"] = f"{i.total:,.2f}"
            # Supplier QTY and UOM
            return_dict[i.item_id]["supplier_qty_uom"] = str(i.quantity_packaging) + " " + str(i.packaging_uom)
            return_dict[i.item_id]["supplier_real_qty_uom"] = str(supplier_real_qty_uom) + " " + str(i.packaging_uom)
            # Out QTY and UOM
            return_dict[i.item_id]["our_qty_uom"] = str(i.quantity) + " " + str(i.uom)
            return_dict[i.item_id]["our_real_qty_uom"] = str(i.quantity_real) + " " + str(i.uom)

        return return_dict
    # ------------------------------ DATA GETTER END

    def count_total(self):
        # self.total_amount must be the grand total of everything
        # this includes discount + tax + everything else that might be added in the future.
        count_total_amount = 0

        # Count the total from purchase contents
        for i in self.purchase_contents:
            count_total_amount += i.price

        # Count the total from freight
        for i in self.purchase_freights:
            count_total_amount += i.gross_amount
        
        if count_total_amount == 0:
            self.total_amount = 0
            self.total_before_disc = 0
            self.discounted_value = 0
            self.discount_amount = 0
            return

        self.total_before_disc = count_total_amount
        
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

    # ====================== @api functions
    # ============
    @api.depends('att_attachment') # Updates attachment count, currently unused
    def _compute_attachment_amount(self):
        for i in self:
            self.attachment_count = len(self.att_attachment)

    @api.onchange('tax') # Changes total on tax change.
    def _calculate_on_tax_change(self):
        self.count_total()

    @api.onchange('discount_percentage') # Recalculates total on discount change.
    def _calculate_on_discount_change(self):
        self.count_total()

    @api.depends('purchase_contents.total', 'purchase_freights.gross_amount') # 
    def _calculate_total_before_discount(self):
        self.count_total()

# UNUSED, MARKED FOR DELETION.
# DEPRECATED.
    def create_receiving_report(self):
        if self.posting_date == False: # SQL Constraint already checks if the posting date is null. Kinda redundant.
            raise ValidationError("Please fill in the posting date before moving on.")

        early_path = __file__ # __file__ is this current .py file.
        def_filepath = str(Path(early_path).resolve().parent.parent)
        print("I AM FILEPATH : ", def_filepath)
        env = Environment(
        loader=FileSystemLoader(def_filepath + '/templates'),
        autoescape=select_autoescape()
        )
        template = env.get_template("old_receiving_report.html")
   
        # The part when It renders the things
        template_render = template.render(
            # +++++++ Main Information, Table Information
            page_amount = 2,
            name = self.name,
            po_number = self.po_number,
            date = self.grab_current_date(),
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{self.total_before_disc:,}",
            discount = f"{self.discounted_value:,}",
            total = f"{self.discount_amount:,}",
            tax = f"{self.taxed_amount:,}",
            grand_total = f"{self.total_amount:,}",
            remarks = self.remarks,
            # ++++++++ Additional Information
            pi_no = "",
            cont_awb_no = self.ad_awb,
            eta_jkt = self.sta_date,
            dated = self.due_date,
            vendor_name = self.grab_vendor_name(),
            vendor_location = self.grab_vendor_location()
        )

        template_html = HTML(string = template_render)
        po_css = CSS(def_filepath + '/templates/old_po_style.scss')
        w3css_css = CSS(def_filepath + '/static/src/css/w3css.css')
        template_html.write_pdf('/home/laptop-it/Downloads/old_example_receiving.pdf', stylesheets = [po_css, w3css_css])
        webbrowser.open('/home/laptop-it/Downloads/old_example_receiving.pdf')

    # DEPRECATED
    def create_purchase_order_report(self):
        if self.posting_date == False: # SQL Constraint checks already checks for this one also.
            raise ValidationError("Please fill in the posting date before moving on.")
        
        early_path = __file__ # __file__ points to this current .py file.
        def_filepath = str(Path(early_path).resolve().parent.parent) # grab parent folder of our parent folder.
        print("I AM FILEPATH : ", def_filepath) 

        env = Environment(
        loader=FileSystemLoader(def_filepath + '/templates'),
        autoescape=select_autoescape()
        )
        template = env.get_template("old_purchase_order.html")

        # The part when It renders the things
        template_render = template.render(
            # ========== Main Information, Table Information
            page_amount = 2,
            page_info = self.get_page_count(),
            name = self.name,
            po_number = self.po_number,
            date = self.grab_current_date(),
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{round(self.total_before_disc,2):,.2f}",
            discount = f"{round(self.discounted_value,2):,.2f}",
            total = f"{round(self.discount_amount,2):,.2f}",
            tax = f"{round(self.taxed_amount,2):,.2f}",
            grand_total = f"{round(self.total_amount,2):,.2f}",
            remarks = self.remarks,
            # =========== Additional Information
            pi_no = "",
            cont_awb_no = self.ad_awb,
            eta_jkt = self.sta_date,
            dated = self.due_date,
            vendor_name = self.grab_vendor_name(),
            vendor_location = self.grab_vendor_location()
        )

        template_html = HTML(string = template_render)
        po_css = CSS(def_filepath + '/templates/old_po_style.scss')
        template_html.write_pdf('/home/laptop-it/Downloads/old_po_example.pdf', stylesheets = [po_css])
        webbrowser.open('/home/laptop-it/Downloads/old_po_example.pdf')

    # DEPRECATED!!!
    def get_page_count(self): # This could be used by either the Purchase Report or the Receiving Report.

        # dict structure :
        # {
        #     "page" : {
        #         "item_id" : {},
        #         "item_id2": {},
        #         "last_page" : False,
        #     },
        # }

        page_info = {}  # Dict for the page information
        pg_count = -1 # Page count starts at -1. Triggers the creation of a new page.
        chr_count = 0 # Counts the amount of description characters in one page.
        max_chr = 920 # Approx 85 per row. 
        # The Summary row approx. takes up about 200 chars.

        element_count = 0 # Used to count the current self.purchase_contents index.

        for i in self.purchase_contents:
            c_desc = i.item_id + " -- " + i.item_name 

            temp_char_count = len(c_desc)

            # Consider each row is 40 characters
            if temp_char_count < 40:
                chr_count += 40
            else:
                row_count = math.ceil(temp_char_count / 40)
                temp_char_count = 40 * row_count
                chr_count += temp_char_count

            # chr_count = 0

            # Create a new page if char exceeds max char, or when starting from -1.
            if chr_count > max_chr or pg_count == -1: # If current char length is more than the max, or when starting the first page
                max_chr = 920
                print("<purchase_order.py> OVERFLOW - AT : ", chr_count)
                pg_count += 1
                chr_count = 0
                page_info[str(pg_count)] = {}
                page_info[str(pg_count)]["last_page"] = False
                print("<purchase_order.py> CHAR COUNT RESET")

                # Not a good practice, but this means that we're doing a nested loop here O(N^2)
                t_chr_count = 0 
                t_curr_idx = element_count
                t_last_idx = len(self.purchase_contents) - 1 
                is_last_index = False

                # Note :
                # This only performs calculations. This will check the page the last index would be able
                # to fit the summary or not. 
                # If the last page (where the last index would be) cannot fit the summary, It will decrease the
                # max char threshold. So what this does is that It would increase the page amount on the next iteration.
                for ii in self.purchase_contents[element_count:]:
                    if t_curr_idx >= t_last_idx: # if True, Then this is the last index
                        is_last_index = True
                            
                    t_chr_str = ii.item_id + " -- " + ii.item_name

                    cc_curr_len = len(t_chr_str)
                    if cc_curr_len < 40:
                        t_chr_count += 80
                    else:
                        t_row_count = math.ceil(cc_curr_len / 40)
                        t_temp_char_count = 40 * t_row_count
                        t_chr_count += t_temp_char_count
                        # t_chr_count += cc_curr_len

                    t_curr_idx += 1

                    if t_chr_count > max_chr:
                        print("<purchase_order.py> Exceeded char count for this page, breaking.")
                        break

                    if is_last_index:
                        print("<purchase_order.py> Last index reached.")
                        if t_chr_count < (max_chr - 240): # This still has space, so we not gon do much
                            print("<purchase_order.py> Summary can fit into the current page : ", t_chr_count, " ", t_chr_count + 240, " ", max_chr)
                        else:
                            # THIS LOGIC DOES NOT WORK AS WELL AS I THINK IT DOES
                            # This creates an undesirable gap in the page. 
                            print("<purchase_order.py> Page can't fit Summary, decreating max char. ", t_chr_count, " ", t_chr_count + 240, " ", max_chr)
                            max_chr -= 240
                            # Decrease current max to something..

            page_info[str(pg_count)][i.item_id] = {i.item_id : {},}
            page_info[str(pg_count)][i.item_id]["count"] = chr_count
            element_count += 1
            print("CHAR AMOUNT IS - ", chr_count)

        # Set info marker for last page,
        page_info[str(pg_count)]["last_page"] = True
        print("PAGE INFO : ", page_info)
        return page_info