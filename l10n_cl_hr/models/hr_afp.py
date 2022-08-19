# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging
log = logging.getLogger(__name__)


class AFP(models.Model):
    _name = 'hr.afp'
    _description = 'Información de AFP'

    codigo = fields.Char('Codigo', required=True)
    name = fields.Char('Nombre', required=True)
    rut = fields.Char('RUT', required=True)
    rate = fields.Float('Tasa', required=True)
    sis = fields.Float('Aporte Empresa', required=True)
    independiente = fields.Float('Independientes', required=True)
    partner_id = fields.Many2one(
        string='Contacto',
        comodel_name='res.partner',
        ondelete='restrict',
    )
