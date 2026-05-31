from odoo import _, models
from odoo.exceptions import UserError
from .res_partner import clean_phone

_PARAM_KEY = 'whatsapp_direct_link.invoice_template'

_DEFAULT_TEMPLATE = (
    'Hello {partner_name},\n\n'
    'Please find below the details of your invoice:\n\n'
    'Invoice No : {name}\n'
    'Date       : {invoice_date}\n'
    'Due Date   : {invoice_date_due}\n'
    'Total      : {amount_total} {currency}\n\n'
    'Kindly arrange payment before the due date.\n\n'
    'Thank you!'
)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_whatsapp(self):
        self.ensure_one()
        partner = self.partner_id
        phone = clean_phone(partner.mobile or partner.phone or '')
        if not phone:
            raise UserError(
                _('No phone number found for %s. Please add a mobile or phone number first.')
                % partner.name
            )

        template = (
            self.env['ir.config_parameter'].sudo().get_param(_PARAM_KEY)
            or _DEFAULT_TEMPLATE
        )

        message = template.format(
            partner_name=partner.name or '',
            name=self.name or '',
            invoice_date=self.invoice_date.strftime('%Y-%m-%d') if self.invoice_date else '',
            invoice_date_due=(
                self.invoice_date_due.strftime('%Y-%m-%d') if self.invoice_date_due else ''
            ),
            amount_total=f'{self.amount_total:,.2f}',
            currency=self.currency_id.name if self.currency_id else '',
        )

        return self.env['whatsapp.message.wizard']._open_for_record(phone, message)
