import urllib.parse
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from ..models.res_partner import clean_phone

_WHATSAPP_BASE = 'https://api.whatsapp.com/send'


class WhatsappMessageWizard(models.TransientModel):
    """Shared wizard used by sale.order and account.move to compose and send a
    WhatsApp message with a pre-filled, editable body."""

    _name = 'whatsapp.message.wizard'
    _description = 'WhatsApp Message Wizard'

    phone = fields.Char(
        string='Phone / Mobile',
        required=True,
        help='International format recommended, e.g. +966500000000',
    )
    message = fields.Text(
        string='Message',
        required=True,
    )
    whatsapp_url = fields.Char(
        string='WhatsApp URL',
        compute='_compute_whatsapp_url',
    )

    @api.depends('phone', 'message')
    def _compute_whatsapp_url(self):
        for record in self:
            number = clean_phone(record.phone or '')
            if number and record.message:
                params = urllib.parse.urlencode({'phone': number, 'text': record.message})
                record.whatsapp_url = f'{_WHATSAPP_BASE}?{params}'
            else:
                record.whatsapp_url = False

    def action_send(self):
        self.ensure_one()
        if not self.whatsapp_url:
            raise UserError(_('Please provide a valid phone number and message.'))
        return {
            'type': 'ir.actions.act_url',
            'url': self.whatsapp_url,
            'target': 'new',
        }

    # ------------------------------------------------------------------
    # Factory helpers called by sale.order / account.move
    # ------------------------------------------------------------------

    @api.model
    def _open_for_record(self, phone, message):
        """Create a wizard record and return the action to open it."""
        wizard = self.create({'phone': phone, 'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Send WhatsApp Message'),
            'res_model': 'whatsapp.message.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
