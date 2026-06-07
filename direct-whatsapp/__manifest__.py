{
    'name': 'WhatsApp Direct Link',
    'version': '16.0.1.0.0',
    'summary': 'Send WhatsApp messages directly from Contacts, Sales, and Invoices',
    'description': """
WhatsApp Direct Link
====================
Adds a WhatsApp button across key Odoo records so your team can reach customers
instantly — no copy-pasting phone numbers, no switching apps.

Features
--------
* **Contacts** – One-click WhatsApp button on every partner record.
* **Sales Quotations** – Open a pre-filled message wizard from any quotation.
* **Customer Invoices** – Open a pre-filled message wizard from any invoice.
* **Configurable Templates** – Manage message templates per document type from
  General Settings (no developer mode needed).
* **No API key required** – Uses the free ``api.whatsapp.com/send`` deep-link.

Supported Odoo version: 16.0
    """,
    'author': 'Hasan Mustafa',
    'website': 'https://sm-iot.com',
    'support': 'sm_iot@qq.com',
    'category': 'Sales/CRM',
    'license': 'LGPL-3',
    'sequence': 10,
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': [
        'contacts',
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/default_templates.xml',
        'views/res_partner_view.xml',
        'views/whatsapp_wizard_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/screenshot1.png',
        'static/description/screenshot2.png',
        'static/description/screenshot3.png',
    ],
}
