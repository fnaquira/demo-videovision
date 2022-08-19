# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Payslip(models.Model):
    _inherit = 'hr.payslip'

    l10n_cl_hr_indicator_id = fields.Many2one(string='Indicador', comodel_name='hr.l10n_cl_hr.indicator', ondelete='restrict', required=True)
