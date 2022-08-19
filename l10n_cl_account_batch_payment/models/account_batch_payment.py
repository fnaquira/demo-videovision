# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64

class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'
    
    name_payments_csv_file = fields.Char('Nombre CSV de Pagos')
    payments_csv_file = fields.Binary('CSV de Pagos', readonly=True)

    def _generate_csv_banco_chile(self, record):
        payment_lines = ['Fecha,Detalle Movimiento,Cheque o Cargo,Deposito o Abono,Docto. Nro.,Trn,Caja,Sucursal']
        for payment_id in record.payment_ids.sorted(key=lambda p: p.date):
            date = payment_id.date
            det_mov = payment_id.name
            cargo = payment_id.amount if payment_id.partner_type == 'supplier' else 0
            abono = payment_id.amount if payment_id.partner_type == 'customer' else 0
            doc_num = payment_id.ref
            trn = 0
            caja = 0
            sucursal = 0 # No se tiene registro
            payment_lines.append("{0},{1},{2},{3},{4},{5},{6},{7}".format(date, det_mov, cargo, abono, doc_num, trn, caja, sucursal))
        return payment_lines

    def _generate_csv_banco_bci(self, record):
        payment_lines = ['Fecha,Sucursal,Descripcion,Nro Documento,Cheque o Cargo,Deposito o Abono']
        for payment_id in record.payment_ids.sorted(key=lambda p: p.date):
            date = payment_id.date
            sucursal = 0 # No se tiene registro
            descrip = payment_id.name
            doc_num = payment_id.ref
            cargo = payment_id.amount if payment_id.partner_type == 'supplier' else 0
            abono = payment_id.amount if payment_id.partner_type == 'customer' else 0
            payment_lines.append("{0},{1},{2},{3},{4},{5}".format(date, sucursal, descrip, doc_num, cargo, abono))
        return payment_lines

    def validate_batch_button(self):
        res = super(AccountBatchPayment, self).validate_batch_button()
        for record in self:
            if record.journal_id.bank_id.l10n_cl_sbif_code not in ["001", "016"]:
                return res
            elif record.journal_id.bank_id.l10n_cl_sbif_code == "001":
                self.name_payments_csv_file = 'Cartola_Banco_Chile.csv'
                payment_lines = self._generate_csv_banco_chile(record)
            elif record.journal_id.bank_id.l10n_cl_sbif_code == "016":
                self.name_payments_csv_file = 'Cartola_Banco_BCI.csv'
                payment_lines = self._generate_csv_banco_bci(record)
            encoded_lines = [l.encode('utf-8') for l in payment_lines]
            encoded_output_file = base64.b64encode(b'\r\n'.join(encoded_lines))
            self.payments_csv_file = encoded_output_file
        return res