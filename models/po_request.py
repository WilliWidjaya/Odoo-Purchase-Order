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
            document_no = self.document_no,
            revision_no = self.revision_no,
            valid_date = self.valid_date,
            affiliated_one = self.affiliated_one.name,
            affiliated_two = self.affiliated_two.name
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

    # def grab_request_data(self):
    #     return_dict = {}
    #     for i in self.request_items:
    #         return_dict[i.name]
    #     return

    def do_nothing(self):
        return