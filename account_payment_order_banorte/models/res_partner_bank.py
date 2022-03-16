# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    id_supplier = fields.Char(
        size=13,
        help='Supplier ID that must exist in the supplier database.',
        string="ID Supplier"
    )
    operation_type = fields.Selection([
        ('01', 'Own'),
        ('02', 'Third parties'),
        ('04', 'SPEI'),
        ('05', 'TEF'),
    ])
    supplier_reference = fields.Char(
        help="Field used to define reference of supplier, if it's not used the"
        " reference must be the invoices that are paid."
    )
