# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
# pylint: disable=too-complex

from odoo import _, models
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    def generate_payment_file(self):
        self.ensure_one()
        if self.payment_method_id.code != 'banorte_credit_transfer':
            return super().generate_payment_file()
        payment_line = self._process_payment_lines()
        return (payment_line.encode('ascii'), self.name + '.txt')

    def _process_payment_lines(self):
        """ Method used to generate payment lines, this is based on layout
        located in data folder of this module.
        Each line will contain description of the field, type and the leght of
        a  field.
        """
        errors = []
        payment_line = ''
        for line in self.bank_line_ids:
            partner = line.partner_id
            # Operación
            # 01 - Propias
            # 02 - Terceros
            # 04 - SPEI
            # 05 - TEF
            # Numérico
            if not line.partner_bank_id.operation_type:
                errors.append(_(
                    'Operation type of supplier %s is not defined') %
                    partner.name)
            payment_line += line.partner_bank_id.operation_type + '\t'
            # Clave ID
            # El ID del proveedor debe previamente existir en el catálogo de
            # proveedores.
            # Obligatorio si Operación es 02, 04 o 05.
            # Alfanumerico 13 carácteres.
            if (line.partner_bank_id.operation_type != '01' and not
                    line.partner_bank_id.id_supplier):
                errors.append(_(
                    'ID Supplier for %s is not defined') % partner.name)
            if line.partner_bank_id.operation_type == '01':
                payment_line += '\t'
            else:
                payment_line += self._format_width_value(
                    value=self._format_characters(
                        line.partner_bank_id.id_supplier),
                    width=13) + '\t'
            # Cuenta Origen
            # Numérico 10 dígitos.
            # Obligatorio.
            payment_line += self.company_partner_bank_id.acc_number + '\t'
            # Cuenta / CLABE Destino
            # Cuentas Banorte deben contener 10 dígitos.
            # Clabes InterBancarias deben contener 18 dígitos.
            if line.partner_bank_id.operation_type in ['01', '02']:
                if len(line.partner_bank_id.acc_number) != 10:
                    errors.append(_(
                        'The account number for %s must be 10 characters '
                        'and is %s') % (partner.name, str(
                            len(line.partner_bank_id.acc_number))))
                payment_line += line.partner_bank_id.acc_number + '\t'
            else:
                if len(line.partner_bank_id.l10n_mx_edi_clabe) != 18:
                    errors.append(_(
                        'The CLABE for %s must be 18 characters '
                        'and is %s') % (partner.name, str(
                            len(line.partner_bank_id.l10n_mx_edi_clabe))))
                payment_line += line.partner_bank_id.l10n_mx_edi_clabe + '\t'
            # Importe
            # Puede llevar "Punto decimal", seguido de hasta dos dígitos.
            bnk_currency = line.order_id.journal_id.currency_id or self.company_id.currency_id
            if line.currency_id == bnk_currency:
                payment_line += '%.2f' % line.amount_currency + '\t'
            else:
                payment_line += '%.2f' % line.amount_company_currency + '\t'
            # Referencia
            # Numérico 10 carácteres.
            if line.partner_bank_id.operation_type == '01':
                payment_line += '\t'
            else:
                payment_line += self._format_width_value(
                    value=str(line.name[1:]),
                    width=10) + '\t'
            # Descripción
            # Alfanumérico 30 carácteres
            communication = line.communication
            if line.partner_bank_id.supplier_reference:
                communication = line.partner_bank_id.supplier_reference
            payment_line += self._format_width_value(
                value=self._format_characters(communication),
                width=30) + '\t'
            # RFC Ordenante
            if line.partner_bank_id.operation_type in ['04', '05']:
                vat = self.company_id.vat
                payment_line += vat + '\t'
            else:
                payment_line += '\t'
            # IVA (Se ignora por requerimiento del cliente.)
            payment_line += '\t'
            # Fecha aplicación
            if line.partner_bank_id.operation_type == '05':
                payment_line += self.date_scheduled.strftime('%d%m%Y') + '\t'
            else:
                payment_line += '\t'
            # Instrucción de pago
            # Si no es SPEI, deben indicarse una X.
            if line.partner_bank_id.operation_type in ['01', '02', '05']:
                payment_line += 'X\n'
            else:
                payment_line += self._format_width_value(
                    value=self._format_characters(
                        _('Payment of %s\n') % self.company_id.name),
                    width=70)
        if errors:
            raise UserError(_(
                'You have the following errors: \n%s') % '\n'.join(errors))
        return payment_line

    def _format_characters(self, text):
        special_chars = "!\"#$%/()=?¡¨*[];:_'¿´+{},.-><°|@¬\\~`^ñÑ"
        for char in special_chars:
            text = text.replace(char, '')
        return text

    def _format_width_value(self, value, width):
        if len(value) > width:
            value = value[:width]
        return value
