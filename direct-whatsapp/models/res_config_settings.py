from odoo import fields, models

_PARAM_PARTNER = 'whatsapp_direct_link.partner_template'
_PARAM_SALE = 'whatsapp_direct_link.sale_template'
_PARAM_INVOICE = 'whatsapp_direct_link.invoice_template'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    whatsapp_partner_template = fields.Text(
        string='Contact Message Template',
        help=(
            'Template used when opening WhatsApp from a Contact record.\n'
            'Available placeholders: {partner_name}, {phone}'
        ),
    )
    whatsapp_sale_template = fields.Text(
        string='Sales Quotation Message Template',
        help=(
            'Template used when opening WhatsApp from a Sales Quotation.\n'
            'Available placeholders: {partner_name}, {name}, {date_order}, '
            '{amount_total}, {currency}'
        ),
    )
    whatsapp_invoice_template = fields.Text(
        string='Invoice Message Template',
        help=(
            'Template used when opening WhatsApp from a Customer Invoice.\n'
            'Available placeholders: {partner_name}, {name}, {invoice_date}, '
            '{invoice_date_due}, {amount_total}, {currency}'
        ),
    )

    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            whatsapp_partner_template=params.get_param(_PARAM_PARTNER, default=''),
            whatsapp_sale_template=params.get_param(_PARAM_SALE, default=''),
            whatsapp_invoice_template=params.get_param(_PARAM_INVOICE, default=''),
        )
        return res

    def set_values(self):
        super().set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param(_PARAM_PARTNER, self.whatsapp_partner_template or '')
        params.set_param(_PARAM_SALE, self.whatsapp_sale_template or '')
        params.set_param(_PARAM_INVOICE, self.whatsapp_invoice_template or '')
