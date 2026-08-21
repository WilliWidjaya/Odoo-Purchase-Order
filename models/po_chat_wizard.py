from odoo import models, fields

class PoChatWizard(models.TransientModel): # Thanks Claude
    _name = 'po_chat_wizard'
    _description = 'Purchase Order AI Chat Wizard'

    prompt = fields.Char(string="Ask AI")
    response = fields.Text(string="Response", readonly=True)
    po_id = fields.Many2one('purchase_order', string="Purchase Order")

    def action_send(self):
        self.ensure_one()
        if not self.prompt:
            return

        reply = self.po_id.message_post(body=self.prompt, message_type='comment')

        # reply = self.po_id.message_post(body=reply, message_type='comment', author_id=self.env.ref('base.partner_root').id)

        self.response = reply

        self.prompt = False
        return {'type': 'ir.actions.act_window', 'res_model': 'po_chat_wizard', 'res_id': self.id, 'view_mode': 'form', 'target': 'new'}
