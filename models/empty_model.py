from odoo import fields, models

class EmptyModel(models.Model):
    _name = "po_empty_model"
    _description = "This is an empty model for testing purposes."

    name = fields.Char() # Data minimal