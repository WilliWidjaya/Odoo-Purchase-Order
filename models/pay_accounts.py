from odoo import fields, models, api

class PoPayAccounts(models.Model):
    _name = "po_pay_accounts"
    _description = "Pay To Accounts"

    name = fields.Char() # Ini bakal di hide dari user.
    payment_information = fields.Text()

