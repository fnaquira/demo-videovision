# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

from datetime import datetime
from xlrd import open_workbook, xldate_as_datetime
import base64
import io

import logging
log = logging.getLogger(__name__)

import base64

class WizardAccountBankStatementNormalizer(models.TransientModel):
    _name = 'wizard.account_bank_statement_normalizer'
    _description = 'Wizard Para normalizar extractos de bancos'
    
    company_id = fields.Many2one(string='Compañia', comodel_name='res.company', required=True, default=lambda self: self.env.company.id)
    journal_id = fields.Many2one(comodel_name='account.journal', string='Diario', required=True)
    name_statement_to_normalize = fields.Char(string='Nombre Extracto a Normalizar')
    statement_to_normalize = fields.Binary(string='Extracto a Normalizar', required=True)
    name_statement_normalized = fields.Char('Nombre Extracto Normalizado')
    statement_normalized = fields.Binary(string='Extracto Normalizado', readonly=True)

    def _normalize_banco_chile(self, record):
        with io.BytesIO(base64.b64decode(record.statement_to_normalize)) as file:
            book = open_workbook(file_contents=file.getvalue())
        sheet = book.sheets()[0]

        payment_lines = ['date,note,amount,balance,name,partner_id/.id']
        for cur_row in range(1, sheet.nrows):
            line = ''
            cargo = False
            for cur_col in range(0, sheet.ncols):
                cell = sheet.cell(cur_row, cur_col)
                cell_value = cell.value
                if cur_col == 0:
                    string_date = xldate_as_datetime(int(cell.value), 0).date().isoformat()
                    split_string_date = string_date.split('-')
                    cell_value = split_string_date[2] + '/' + split_string_date[1] + '/' + split_string_date[0]
                    line += cell_value + ','
                elif cur_col == 1:
                    line += str(cell.value) + ','
                elif cur_col == 2 and cell.value:
                    line += str(cell.value * -1)  + ','
                    cargo = True
                elif cur_col == 3 and not cargo:
                    line += str(cell.value) + ','
                elif cur_col == 4:
                    line += str(cell.value) + ','
                elif cur_col == 5:
                    line += str(cell.value) + ','
            payment_lines.append(line)
            
        return payment_lines

    def _normalize_banco_bci(self, record):
        with io.BytesIO(base64.b64decode(record.statement_to_normalize)) as file:
            book = open_workbook(file_contents=file.getvalue())
        sheet = book.sheets()[0]

        payment_lines = ['date,note,name,amount,balance,partner_id/.id']
        for cur_row in range(23, sheet.nrows):
            line = ''
            for cur_col in range(0, sheet.ncols):
                cell = sheet.cell(cur_row, cur_col)
                if cell.value:
                    if cur_col == 0:
                        line += cell.value + ','
                    elif cur_col == 5:
                        line += cell.value + ','
                    elif cur_col == 8:
                        line += cell.value + ','
                    elif cur_col == 10:
                        line += str(float(cell.value.replace('.', '')) * -1)  + ','
                    elif cur_col == 11:
                        line += (cell.value.replace('.', '')) + ','
                    elif cur_col == 12:
                        line += (cell.value.replace('.', '')) + ','
            payment_lines.append(line)
            
        return payment_lines

    def create_csv_normalized(self):
        for record in self:
            payment_lines = []
            if record.journal_id.bank_id.l10n_cl_sbif_code == "001":
                payment_lines.extend(self._normalize_banco_chile(record))
            elif record.journal_id.bank_id.l10n_cl_sbif_code == "016":
                payment_lines.extend(self._normalize_banco_bci(record))
            encoded_lines = [l.encode('utf-8') for l in payment_lines]
            encoded_output_file = base64.b64encode(b'\r\n'.join(encoded_lines))
            record.name_statement_normalized = 'Normalizado_' + record.name_statement_to_normalize + '.csv'
            record.statement_normalized = encoded_output_file
        return {
            'name': 'Generar CSV Normalizado',
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.account_bank_statement_normalizer',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }