from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

from ..models.res_partner import clean_phone


class TestCleanPhone(TransactionCase):
    """Unit tests for the clean_phone helper."""

    def test_strips_spaces_and_dashes(self):
        self.assertEqual(clean_phone('+966 50 000-0000'), '966500000000')

    def test_strips_parentheses(self):
        self.assertEqual(clean_phone('(966)500000000'), '966500000000')

    def test_strips_plus_sign(self):
        self.assertEqual(clean_phone('+1234567890'), '1234567890')

    def test_empty_string_returns_empty(self):
        self.assertEqual(clean_phone(''), '')

    def test_false_returns_empty(self):
        self.assertEqual(clean_phone(False), '')

    def test_none_returns_empty(self):
        self.assertEqual(clean_phone(None), '')

    def test_digits_only_unchanged(self):
        self.assertEqual(clean_phone('966500000000'), '966500000000')


class TestResPartnerWhatsApp(TransactionCase):
    """Tests for the res.partner WhatsApp computed field and action."""

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'mobile': '+966 50 000-0000',
        })

    def test_whatsapp_url_computed(self):
        self.assertIn('966500000000', self.partner.whatsapp_url)
        self.assertIn('api.whatsapp.com', self.partner.whatsapp_url)

    def test_no_phone_gives_false_url(self):
        partner = self.env['res.partner'].create({'name': 'No Phone Partner'})
        self.assertFalse(partner.whatsapp_url)

    def test_mobile_preferred_over_phone(self):
        self.partner.phone = '+1 000 000 0000'
        self.assertIn('966500000000', self.partner.whatsapp_url)

    def test_action_open_whatsapp_returns_act_url(self):
        action = self.partner.action_open_whatsapp()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertEqual(action['target'], 'new')

    def test_action_raises_when_no_url(self):
        partner = self.env['res.partner'].create({'name': 'Empty'})
        with self.assertRaises(Exception):
            partner.action_open_whatsapp()


class TestWhatsappWizard(TransactionCase):
    """Tests for the whatsapp.message.wizard model."""

    def test_url_built_correctly(self):
        wizard = self.env['whatsapp.message.wizard'].create({
            'phone': '+966500000000',
            'message': 'Hello World',
        })
        self.assertIn('966500000000', wizard.whatsapp_url)
        self.assertIn('Hello+World', wizard.whatsapp_url.replace('%20', '+').replace(' ', '+'))

    def test_action_send_returns_act_url(self):
        wizard = self.env['whatsapp.message.wizard'].create({
            'phone': '+966500000000',
            'message': 'Test message',
        })
        action = wizard.action_send()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertEqual(action['target'], 'new')

    def test_action_send_raises_without_phone(self):
        wizard = self.env['whatsapp.message.wizard'].new({
            'phone': '',
            'message': 'Test',
        })
        with self.assertRaises(UserError):
            wizard.action_send()


class TestSaleOrderWhatsApp(TransactionCase):
    """Tests for the sale.order WhatsApp action."""

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Sale Partner',
            'mobile': '+966500000001',
        })
        self.order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

    def test_action_open_whatsapp_opens_wizard(self):
        action = self.order.action_open_whatsapp()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'whatsapp.message.wizard')
        self.assertEqual(action['target'], 'new')

    def test_no_phone_raises_user_error(self):
        partner_no_phone = self.env['res.partner'].create({'name': 'No Phone'})
        order = self.env['sale.order'].create({'partner_id': partner_no_phone.id})
        with self.assertRaises(UserError):
            order.action_open_whatsapp()


class TestAccountMoveWhatsApp(TransactionCase):
    """Tests for the account.move WhatsApp action."""

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Invoice Partner',
            'mobile': '+966500000002',
        })
        self.invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        })

    def test_action_open_whatsapp_opens_wizard(self):
        action = self.invoice.action_open_whatsapp()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'whatsapp.message.wizard')
        self.assertEqual(action['target'], 'new')

    def test_no_phone_raises_user_error(self):
        partner_no_phone = self.env['res.partner'].create({'name': 'No Phone'})
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner_no_phone.id,
        })
        with self.assertRaises(UserError):
            invoice.action_open_whatsapp()
