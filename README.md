# WhatsApp Direct Link

## Overview
An Odoo 18 module that adds WhatsApp integration across the system,
allowing users to quickly contact customers and vendors via WhatsApp
directly from Odoo records.

---

## Current Features

### 1. Contact WhatsApp Button
- Adds a WhatsApp button on the **Contacts (res.partner)** form view
- Button appears next to the mobile field
- Clicking it opens WhatsApp with the contact's phone number
- Button is hidden if no phone/mobile number is set

---

## Planned Features

### 2. Sales Invoice & Quotation WhatsApp Button
- Add a WhatsApp button next to the **customer name** field in:
  - Sales Quotations (`sale.order`)
  - Sales Invoices (`account.move` - customer invoices)
- Clicking the button opens a **popup (Wizard)** containing a
  pre-filled message with the relevant invoice/quotation details

### Message Template (auto-generated)
The popup message will include the following fields:
- Customer name
- Document number (Invoice / Quotation reference)
- Document date
- Due date (for invoices)
- Total amount
- Currency

### Workflow
1. User opens a Sales Invoice or Quotation
2. User clicks the WhatsApp button next to the customer name
3. A popup appears with the pre-filled message
4. User can edit the message before sending
5. User clicks **Send** → WhatsApp opens in a new tab with
   the message ready to send to the customer's number

---

## Technical Stack
- **Odoo Version:** 18.0
- **Models extended:** `res.partner`, `account.move`, `sale.order`
- **WhatsApp method:** `api.whatsapp.com/send?phone=X&text=MESSAGE`
  (no API key required)
- **Popup:** Odoo Wizard (`TransientModel`)

---

## Installation
1. Copy module to your Odoo addons directory
2. Update apps list
3. Install **WhatsApp Direct Link**

## Dependencies
- `contacts`
- `sale` (for Sales Quotations feature)
- `account` (for Invoices feature)