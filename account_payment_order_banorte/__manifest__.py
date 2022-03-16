# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Account Payment Order Banorte',
    'summary': 'Module that install Account Payment Order Banorte',
    'version': '15.0.1.0.0',
    'category': 'Accounting',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'account_payment_order',
        'l10n_mx',
        'l10n_mx_edi',
    ],
    'data': [
        'data/data_account_payment_method.xml',
        'data/data_account_payment_mode.xml',
        'views/res_partner_bank_views.xml',
        'wizards/account_payment_line_create_view.xml',
    ],
}
