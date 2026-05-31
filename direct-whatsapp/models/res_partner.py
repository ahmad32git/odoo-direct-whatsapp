import re
from odoo import models, fields, api


def clean_phone(phone):
    """Return a digit-only string suitable for a WhatsApp deep-link.

    Strips spaces, dashes, parentheses and leading '+'.  Returns an empty
    string when *phone* is falsy so callers can use a simple truthiness check.
    """
    if not phone:
        return ''
    return re.sub(r'[\s\-\(\)\+]', '', phone)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    whatsapp_url = fields.Char(
        string='WhatsApp Link',
        compute='_compute_whatsapp_url',
    )

    @api.depends('phone', 'mobile')
    def _compute_whatsapp_url(self):
        for record in self:
            number = clean_phone(record.mobile or record.phone or '')
            record.whatsapp_url = (
                f'https://api.whatsapp.com/send?phone={number}' if number else False
            )

    def action_open_whatsapp(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.whatsapp_url,
            'target': 'new',
        }
