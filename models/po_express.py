from odoo import fields, models, api

class PoExpress(models.Model):
    _name = "po_express"
    _description = "Express Code"

    name = fields.Char(compute = "change_display_name") # Ini bakal di hide dari user.

    express_code = fields.Char()
    express_name = fields.Char() # Juga disebut sebagai item name.


    @api.depends('express_code')
    def change_display_name(self):
        for i in self:
            i.name = i.express_code

