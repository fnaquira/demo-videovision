# -*- coding: utf-8 -*-
from odoo import models, fields


class HrContract(models.Model):
    _inherit = 'hr.contract'

    l10n_cl_pension_system = fields.Selection(string='Regimen Previsional', selection=[
        ('AFP', 'AFP'),
        ('INP', 'IPS (Ex-INP)'),
        ('SIP', 'Sin Institución Previsional')
    ], default='AFP')
    l10n_cl_worker_type = fields.Selection(string='Tipo Trabajador', selection=[
        ('0', 'Activo (No Pensionado)'),
        ('1', 'Pensionado y cotiza'),
        ('2', 'Pensionado y no cotiza'),
        ('3', 'Activo > 65 años (nunca pensionado)'),
        ('8', 'Exento de cotizar (Mujer mayor de 60 años, Hombre mayor de 65 o Extranjero)')
    ], default='0')