from odoo import api, fields, models
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from weasyprint import HTML, CSS
from datetime import datetime
import os, os.path, platform
from pathlib import Path
import webbrowser

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

    def grab_output_folder(self):
        curr_platform = platform.system()
        report_path_temp = "" # Start with an empty path?

        match curr_platform:
            case "Windows":
                t_file = Path(__file__).resolve()
                report_path_temp = t_file.anchor # For Windows.
            case "Linux":
                report_path_temp = Path(os.path.expanduser("~"))
            case _:
                print("Invalid OS.")

        report_path = Path(report_path_temp) / "OdooDownloads"
        report_path.mkdir(parents = True, exist_ok=True)

        print("GRABBED DOWNLOAD PATH : ", report_path)
        return report_path

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
            date = self.grab_date(),
            document_no = self.document_no,
            revision_no = self.revision_no,
            valid_date = self.valid_date,
            affiliated_one = self.affiliated_one.name,
            affiliated_two = self.affiliated_two.name,
            request_data = self.grab_request_data()
        )

        # output_file_name = "example_request_form_" + datetime.now().strftime("%d%m%Y_%H%M%S")
        output_file_name = "example_request_form_"

        template_html = HTML(string = template_render)
        request_css = CSS(str(template_filepath / "po_request_style.scss"))

        # Grab folder lokasi file akan disimpan
        output_folder_path = self.grab_output_folder()

        final_filepath = str(output_folder_path / output_file_name) + ".pdf"
        template_html.write_pdf(final_filepath, stylesheets = [request_css])

        webbrowser.open(Path(final_filepath).as_uri())

        return

    def grab_request_data(self):
        return_dict = {}
        item_index = 0

        # Logic yang sama ada di beberapa line dibawah, cuma memastikan disini.
        if self.request_items == False:
            return False

        for i in self.request_items:
            curr_idx = str(item_index)
            return_dict[curr_idx] = {}
            return_dict[curr_idx]["no"] = str(item_index + 1)
            return_dict[curr_idx]["unit"] = i.name + " - " + i.description
            return_dict[curr_idx]["dept"] = i.department
            return_dict[curr_idx]["qty"] = i.quantity
            return_dict[curr_idx]["est_price"] = "IDR " + f"{i.estimated_price:,.2f}"
            item_index += 1

        # Logic yang sama yang dimaksud. tapi dia ngecek return_dict
        if return_dict == False or return_dict == {}:
            return False
        else:
            return return_dict


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