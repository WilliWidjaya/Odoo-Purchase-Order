from odoo import api, fields, models
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime
import os, os.path, platform
from pathlib import Path
import webbrowser
import base64

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
    affiliated_one = fields.Many2one('po_vendor')
    affiliated_two = fields.Many2one('po_vendor')

    # Custom Title and location
    custom_title_vendor = fields.Many2one('po_vendor')
    custom_title_contact = fields.Many2one('po_contact')

    def grab_custom_name(self):
        if self.custom_title_vendor:
            return self.custom_title_vendor.name
        if self.custom_title_contact:
            return self.custom_title_contact.name

        return "PT. INDOGUNA UTAMA"

    def grab_custom_location(self):
        if self.custom_title_vendor:
            return self.custom_title_vendor.location
        if self.custom_title_contact:
            return self.custom_title_contact.location

        return "Jl. Taruna No. 8 Pondok Bambu Jakarta Timur - Indonesia"

    def create_request_form(self):
        # Grab filepath for the template and style
        # Mengikuti pola file, dimana dia ambil parent folder dari parent folder.
        def_filepath = Path(__file__).resolve().parent.parent

        # Lokasi folder template.
        template_filepath = def_filepath / "templates"

        env = Environment(
        loader=FileSystemLoader(str(def_filepath / "templates")),
        autoescape=select_autoescape()
        )

        # Template html-nya
        template = env.get_template("template_request_form.html")

        template_render = template.render(
            name = self.name,
            title_name = self.grab_custom_name(),
            title_location = self.grab_custom_location(),
            date = self.grab_date(),
            document_no = self.document_no,
            revision_no = self.revision_no,
            valid_date = self.valid_date,
            affiliated_one = self.affiliated_one.name,
            affiliated_two = self.affiliated_two.name,
            request_data = self.grab_request_data(),
            logo_path = (template_filepath / "assets" / "logo_igu.png").as_uri()
        )

        template_html = HTML(string = template_render)
        po_css = CSS(str(template_filepath / "po_request_style.scss"))
        generated_file = template_html.write_pdf(stylesheets = [po_css])
        
        file_name = self.name + "_request_" + datetime.now().strftime("%d%m%Y_%H%M%S")

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

    def grab_request_data(self):
        return_arr = []
        item_index = 0

        # Logic yang sama ada di beberapa line dibawah, cuma memastikan disini.
        if self.request_items == False:
            return False

        for i in self.request_items:
            current_dict = {}
            current_dict["no"] = str(item_index + 1)
            current_dict["unit"] = i.item_id.item_code + " - " + i.description
            current_dict["dept"] = i.department
            current_dict["qty"] = i.quantity
            current_dict["est_price"] = "IDR " + f"{i.estimated_price:,.2f}"
            item_index += 1
            return_arr.append(current_dict)

        # Logic yang sama yang dimaksud. tapi dia ngecek return_dict
        if not return_arr:
            return False
        else:
            return return_arr

    def grab_date(self):
        curr_date = datetime.now()
        
        date_num = curr_date.strftime("%d")
        month_name = self.grab_month_name_indonesian(curr_date.strftime("%m"))
        year = curr_date.strftime("%Y")

        date_str = date_num + " " + month_name + " " + year
        return date_str

    def grab_month_name_indonesian(self, month_name):
        match month_name:
            case "01":
                return "Januari"
            case "02":
                return "Februari"
            case "03":
                return "Maret"
            case "04":
                return "April"
            case "05":
                return "Mei"
            case "06":
                return "Juni"
            case "07":
                return "Juli"
            case "08":
                return "Agustus"
            case "09":
                return "September"
            case "10":
                return "Oktober"
            case "11":
                return "November"
            case "12":
                return "Desember"

    def do_nothing(self):
        return