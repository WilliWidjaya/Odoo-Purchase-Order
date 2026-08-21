from odoo import api, fields, models
from jinja2 import Environment, select_autoescape, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime
import base64

# For Opening the file after making the pdf
from pathlib import Path

# bagian open AI
from openai import OpenAI
import json

# For Running Bash
import subprocess
from odoo.exceptions import UserError

import pandas as pd
import psycopg2
import os

#LLM Tool
from odoo.addons.llm_tool.decorators import llm_tool

class PurchaseOrder(models.Model):
    _name = "purchase_order"
    _description = "Purchase Order"
    _inherit = ['mail.thread']

    po_number = fields.Char(string = "Purchase Order No", copy = False) # No Char

    # Vendor Information
    name = fields.Char(string = "Name")

    vendor = fields.Many2one('po_vendor') # INI DIAMBIL DARI PO_VENDOR

    vendor_ref_no = fields.Char(string = "Vendor Ref. No") # No Char

    contact_person = fields.Many2one('po_contact') # INI DIAMBIL DARI PO_CONTACTS

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
    total_before_disc = fields.Float(string = "Total Before Disc.", compute = "_calculate_total_before_discount", store = True)
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
    ship_to = fields.Many2one('po_shipping_location')
    pay_to = fields.Many2one('po_pay_accounts')
    ship_tb = fields.Text()
    pay_tb = fields.Text()

    #Freight
    purchase_freights = fields.One2many(comodel_name="purchase_order_freight", inverse_name="purchase_order_id")

    #Attachment
    att_attachment = fields.Many2many(comodel_name="ir.attachment")
    attachment_count = fields.Integer(string = "attachment_count", compute = "_compute_attachment_amount", store = True)

    #Additional Informatio
    ad_vessel_flight = fields.Char(string = "Vessel/Flight")
    ad_container = fields.Char(string = "Container")
    ad_awb = fields.Char(string = "AWB No/ BI NO")
    ad_pesawat = fields.Char(string = "Pesawat")
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


    # VARIABLES FOR CUSTOM TITLE AND LOCATION
    # Logicnya, kalo dua2 keisi, dia bakal fallback ke default. ato bakal ada
    # yang ngecek.
    custom_title_from_vendor = fields.Many2one('po_vendor')
    custom_title_from_contact = fields.Many2one('po_contact')

    # Either bisa pake lu ketik sendiri
    custom_title = fields.Char(string="Custom Title")
    custom_location = fields.Char(string="Custom Location")

    # This is the chat history for the chatbot 
    chat_history = fields.Text()

    _sql_constraints = [
        ('check_po_code', 'CHECK(po_number IS NOT NULL)', 'You must fill the PO number.'),
        ('check_po_length', 'CHECK(LENGTH(po_number) >= 5)', 'Ermm PO must be longer than 5 or 6'),
        ('check_po_unique', 'UNIQUE(po_number)', 'PO number must be distinct or unique'),
        ('check_rate', 'CHECK(rate >= 0)', 'YOU GOTTA SET THIS RATE RIGHT BRO'),
        ('check_tax', 'CHECK(tax >= 0 AND tax <= 100)', 'The Tax Percentage must be reasonable.'),
        ('check_discount_percentage', 'CHECK(discount_percentage >= 0 AND discount_percentage <= 100)', 'Discount percentage must be between 0 and 100'),
        ('check_posting_date','CHECK(posting_date IS NOT NULL)', 'Please fill in the posting date.'),
        ('check_name_filled', 'CHECK(name IS NOT NULL)', 'Please fill in [name] for this entry.'),
        ('check_name_length', 'CHECK(LENGTH(name) >= 5 AND LENGTH(name) <= 45)', 'Name must be between 3 and 45 characters.'), 
        ('check_vendor_filled', 'CHECK(vendor IS NOT NULL)', 'Please fill in a vendor.')
    ]


    # ------------------------------ REPORT CREATION & RELATED CALCULATIONS

    def grab_title(self):
        if self.custom_title_from_contact:
            return self.custom_title_from_contact.name
        elif self.custom_title_from_vendor:
            return self.custom_title_from_vendor.name
        else:
            return "PT. INDOGUNA UTAMA"

    def grab_title_location(self):
        if self.custom_title_from_contact:
            return self.custom_title_from_contact.location
        elif self.custom_title_from_vendor:
            return self.custom_title_from_vendor.location
        else:
            return "Jl. Taruna No.8 Pondok Bambu Jakarta Timur - Indonesia"


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
            title_name = self.grab_title(),
            title_location = self.grab_title_location(),
            po_number = self.po_number,
            date = self.grab_current_date(),
            purchase_data = self.grab_purchase_content(),
            sub_total = f"{round(self.total_before_disc,2):,.2f}",
            supplier_total_quantity = self.grab_total_supplier_quantity(),
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
        po_css = CSS(str(def_filepath / "templates" / "po_style.scss"))
        generated_file = template_html.write_pdf(stylesheets = [po_css])
        
        file_name = self.name + "_receiving_" + datetime.now().strftime("%d%m%Y_%H%M%S")

        # Create new ir.attachment (dia persistent dan bisa diakses di Odoo ir.attachments)
        f_attachment = self.env['ir.attachment'].create({
            'name' : f'{file_name}.pdf',
            'type' : 'binary', 
            'datas' : base64.b64encode(generated_file),
            'res_model' : self._name,
            'res_id' : self.id,
            'mimetype' : 'application/pdf'
        })

        # Buka file dengan ir.actions.act_url Odoo 
        return {
            'type' : 'ir.actions.act_url',
            'url' : f'/web/content/{f_attachment.id}?download=true',
            'target' : 'new',
        }


    def template_create_purchase_report(self):
        early_path = __file__ # __file__ points to this current .py file.
        def_filepath = Path(early_path).resolve().parent.parent # grab parent folder of our parent folder.
        
        env = Environment(
        loader=FileSystemLoader(str(def_filepath / "templates")),
        autoescape=select_autoescape()
        )
        template = env.get_template("template_purchase_order.html")

        template_render = template.render(
            # ========== Main Information, Table Information
            name = self.name,
            title_name = self.grab_title(),
            title_location = self.grab_title_location(),
            po_number = self.po_number,
            date = self.grab_current_date(),
            purchase_data = self.grab_purchase_content(),
            supplier_total_quantity = self.grab_total_supplier_quantity(),
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
        po_css = CSS(str(def_filepath / "templates" / "po_style.scss"))
        generated_file = template_html.write_pdf(stylesheets = [po_css])
        
        file_name = self.name + "_po_" + datetime.now().strftime("%d%m%Y_%H%M%S")

        # Create new ir.attachment (dia persistent dan bisa diakses di Odoo ir.attachments)
        f_attachment = self.env['ir.attachment'].create({
            'name' : f'{file_name}.pdf',
            'type' : 'binary', 
            'datas' : base64.b64encode(generated_file),
            'res_model' : self._name,
            'res_id' : self.id,
            'mimetype' : 'application/pdf'
        })

        # Buka file dengan ir.actions.act_url Odoo 
        return {
            'type' : 'ir.actions.act_url',
            'url' : f'/web/content/{f_attachment.id}?download=true',
            'target' : 'new',
        }


    # ------------------------------ END OF REPORT CREATION

    # -------------------- OPEN AI START

    chatgpt_prompt = fields.Char()

    def read_purchase_orders(self):
        os_cwd = os.getcwd()
        script_folder_path = Path(os_cwd) / "OdooExternalPrograms" / "export_purchase_order_to_spreadsheet"

        output_path = script_folder_path / "input_files" / "purchase_orders.xlsx"

        if not output_path.exists(): 
            self.bash_export_to_xlsx()
            return "tell the player that you updated the table, and ask the user to ask again."

        read_output = pd.read_excel(output_path) 

        data = read_output.to_dict(orient='records')
        dumped_json = json.dumps(data, default=str)
        return dumped_json

    def get_all_purchase_orders(self):
        print("RUNNING GET ALL PURCHASE ORDERS")
        datas = self.env['purchase_order'].search([])

        data_list = []

        for order in datas:
            data_list.append(order.read()[0])


        # grabbed_purchase_orders = datas.read()[0]
        # print("GRABBED PO : ", grabbed_purchase_orders)
        return json.dumps(data_list, default=str)
        # return "There are no datas for now, say BANANA"

    def get_datas(self):
        self.ensure_one()
        data = self.read()[0]
        data['purchase_contents'] = self.purchase_contents.read()
        return json.dumps(data, default=str)

    def do_chat(self):
        self.message_post(body=self.chatgpt_prompt, message_type='comment')

    def message_post(self, **kwargs):
        msg = super().message_post(**kwargs)
        reply = "No reply was given."
        if kwargs.get('message_type') == 'comment' and kwargs.get('author_id') != self.env.ref('base.partner_root').id:
            reply = self.do_chatgpt(kwargs.get('body', ''))
            super().message_post(
                body=reply,
                message_type='comment',
                author_id=self.env.ref('base.partner_root').id,
            )


        # TODO :
        #   - Disini ada bug dimana kalo kita return reply instead of msg, kita gabakal bsia chat di <chatter/> dan cuma bisa di wizard.
        return msg
        # return reply

    def do_chatgpt(self, prompt):
        history = json.loads(self.chat_history or "[]")
        tools = [
                {
                    "type": "function",
                    "name": "get_datas",
                    "description": """
                                    Use this when prompt requires data from the current purchase order entry only, the one you are currently in.
                                    Example questions : Who is the vendor? What's the customers name? What' the payment term? When is the purchase order due?
                                    How many days between posting date and due date?
                                """,
                },
                {
                    "type" : "function",
                    "name" : "read_purchase_orders",
                    "description" : """ 
                                    Use this when prompt requires data from the entirety of the PO database, or all purchase order entries.
                                    only the current purchase order.
                                    For example : How many POs are there?, Which POs start with PO-2026?, Whats the total cost of all POs?
                                    Which POs are handled by Ricky?
                                    
                                    """
                }
                ] 

        input_list = [{"role": "user", "content": prompt}]

        client = OpenAI()

        history.append({"role": "user", "content": prompt})

        response = client.responses.create(
            model="gpt-5.6",
            instructions = "You are currently in a page which shows a singular PO data. Assume questions ask about the current PO, and go get_datas(). Users will ask for information regarding purchase order datas Decide whether the user is asking for data of the current PO, or a question regarding the entirety of the PO database.",
            # input= input_list,
            input = history,
            tools= tools,
        )

        input_list += response.output

        for item in response.output:
            if item.type == "function_call":
                if item.name == "get_datas":
                    all_datas = self.get_datas()

                    # 4. Provide function call results to the model
                    history.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": all_datas,
                        }
                    )
                elif item.name == "read_purchase_orders":
                    read_files = self.read_purchase_orders()
                    history.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": read_files,
                        }
                    )

        response = client.responses.create(
            model="gpt-5.6",
            instructions="Respond appropraitely.",
            tools=tools,
            input=history,
        )

        reply = response.output_text
                
        history.append({"role": "assistant", "content": reply})

        self.chat_history = json.dumps(history)

        # 5. The model should be able to give a response!
        print("Final output:")
        print(response.model_dump_json(indent=2))
        print("\n" + response.output_text)
        return response.output_text

    # ------------------------------ OPEN AI END


    # --------------------- RUNNING BASH FILE
    
    def run_bash_grab_data_psql(self):
        self.bash_export_to_xlsx()
        self.upload_to_gdrive()

    def bash_export_to_xlsx(self):
        early_path = __file__ # __file__ points to this current .py file.
        def_filepath = Path(early_path).resolve().parent.parent # grab parent folder of our parent folder.

        sql_query = """
                    SELECT 
                        po.po_number,
                        po.status,
                        po.name, 
                        po_vendor.name AS "vendor_name",
                        po.vendor_ref_no, 
                        po_contact.name AS "contact_name",
                        po.posting_date::text,
                        po.due_date::text,
                        po.payment_date::text,
                        po.sta_date::text,
                        po.total_before_disc,
                        po.discount_percentage,
                        po.discounted_value,
                        po.discount_amount,
                        po.tax,
                        po.taxed_amount,
                        po.total_amount,
                        po.payment_terms,
                        po.remarks,
                        po_shipping_location.shipping_location,
                        po_pay_accounts.payment_information,
                        po.ad_vessel_flight,
                        po.ad_container,
                        po.ad_awb,
                        po.ad_pesawat,
                        "ad_vendor_DO_no",
                        "ad_no_tanggal_PIB"::text,
                        "ad_PIB_pesan",
                        po.ad_bank_name,
                        po.ad_pph,
                        po.ad_tgl_bbpcp::text,
                        po.ad_total_cf,
                        "ad_NDPBM",
                        po.ad_pi_date::text, 
                        po.ad_tgl_invoice 
                    FROM purchase_order po
                    LEFT JOIN po_shipping_location ON po.ship_to = po_shipping_location.id
                    LEFT JOIN po_pay_accounts ON po.pay_to = po_pay_accounts.id
                    LEFT JOIN po_vendor ON po.vendor = po_vendor.id
                    LEFT JOIN po_contact ON po.contact_person = po_contact.id
                    """

        self.env.cr.execute(sql_query)
        rows = self.env.cr.fetchall()

        columns = [desc[0] for desc in self.env.cr.description]

        df = pd.DataFrame(rows, columns=columns)

        os_cwd = os.getcwd()
        script_folder_path = Path(os_cwd) / "OdooExternalPrograms" / "export_purchase_order_to_spreadsheet"
        output_path = script_folder_path / "input_files" / "purchase_orders.xlsx"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)

        print("OUTPUT PATH : ", output_path)
        return

    def upload_to_gdrive(self):
        # Create another running bash script here again

        os_cwd = os.getcwd()
        script_folder_path = Path(os_cwd) / "OdooExternalPrograms" / "export_purchase_order_to_spreadsheet"
        bash_filepath = str(script_folder_path / "run.sh")
        
        result = subprocess.run( # $1, $2, dan $3
            ['bash', bash_filepath],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise UserError(f"Script failed: {result.stderr}")
        print("THIS IS THE FINAL BASH RESULT : ", result.stdout)
        return

    # ---------------------



    # ------------------------------ DATA GETTER START
    
    def grab_current_date(self): # Get current date in dd-mm-yyyy format.
        date_str = str(self.posting_date)

        formatted_time = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
        return formatted_time

    def grab_our_location(self): # Fill in later when needed.
        return 

    def grab_vendor_name(self): # Grab name of vendor from the vendor Many2One
        t_vendor = self.with_prefetch().vendor
        return t_vendor.name.upper()

    def grab_vendor_location(self): # Grabs vendor street1 address from vendor Many2One
        return self.vendor.location

    def grab_total_supplier_quantity(self): # Ini ngambil total kuantitas dari semua entry dari supplier, tanpa diskriminasi UOM
        grabbed_total_supplier_quantity = 0 # Panjang namanya, tapi biar dia jelas ngitung apa :)
        for i in self.purchase_contents:
            grabbed_total_supplier_quantity += i.quantity_packaging
        return grabbed_total_supplier_quantity


    def grab_purchase_content(self): # Grabbing purchase_content One2Many

        return_arr = []
        for i in self.purchase_contents:
            content_dict = {}
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

            content_dict["description"] = i.item_id.item_code + " -- " + i.item_name
            content_dict["quantity"] = i.quantity

            content_dict["price"] = f"{i.price:,.2f}" 
            content_dict["total"] = f"{i.total:,.2f}"

            # Supplier QTY and UOM
            content_dict["supplier_qty_uom"] = str(i.quantity_packaging) + " " + str(i.packaging_uom)
            content_dict["supplier_real_qty_uom"] = str(supplier_real_qty_uom) + " " + str(i.packaging_uom)
            # Out QTY and UOM
            content_dict["our_qty_uom"] = str(i.quantity) + " " + str(i.uom)
            content_dict["our_real_qty_uom"] = str(i.quantity_real) + " " + str(i.uom)

            return_arr.append(content_dict)

        return return_arr
    # ------------------------------ DATA GETTER END

    def count_total(self):
        self.ensure_one()
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
        if self.purchase_contents != False:
            self.count_total()

    @api.onchange('discount_percentage') # Recalculates total on discount change.
    def _calculate_on_discount_change(self):
        if self.purchase_contents != False:
            self.count_total()

    @api.depends('purchase_contents.total', 'purchase_freights.gross_amount') # 
    def _calculate_total_before_discount(self):
        for record in self:
            # if record.purchase_contents != False:
            record.count_total()

    


    