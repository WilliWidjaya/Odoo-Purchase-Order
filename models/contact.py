from odoo import fields, models

class PoContact(models.Model):
    _name = "po_contact"
    _description = "Purchase Order Contact"

    name = fields.Char()
    location = fields.Text()

