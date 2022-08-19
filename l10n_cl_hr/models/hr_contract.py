# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Contract(models.Model):
    _inherit = 'hr.contract'

    l10n_cl_hr_union_dues = fields.Monetary('Cuota sindical', required=True)
    l10n_cl_hr_type = fields.Selection(
        string='Tipo de contrato',
        selection=[
            ('empresarial','Sueldo Empresarial'),
            ('plazo_fijo','Plazo Fijo'),
            ('plazo_indefinido','Plazo Indefinido'),
            ('indefinido','Indefinido 11 años o más'),
        ],
        default='plazo_indefinido',
        required=True,
    )
    l10n_cl_hr_legal_grati = fields.Boolean('Gratificación L. Manual')
    l10n_cl_hr_colacion = fields.Float(string='Colación')
    l10n_cl_hr_movilizacion = fields.Float(string='Movilización')

    l10n_cl_hr_pension = fields.Boolean('Pensionado')
    l10n_cl_hr_sin_afp = fields.Boolean('No Calcula AFP')
    l10n_cl_hr_sin_afp_sis = fields.Boolean('No Calcula AFP SIS')

    afp_id = fields.Many2one(string='AFP', comodel_name='hr.afp', ondelete='restrict')
    isapre_id = fields.Many2one(string='Isapre', comodel_name='hr.isapre', ondelete='restrict')
    l10n_cl_hr_isapre_cotizacion_uf = fields.Float('Cotización (UF)', digits=(6, 4),  help="Cotización Pactada")  
    l10n_cl_hr_isapre_fun = fields.Char('Número de FUN',  help="Indicar N° Contrato de Salud a Isapre") 
    l10n_cl_hr_isapre_cuenta_propia = fields.Boolean('Isapre Cuenta Propia')
