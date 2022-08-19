# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging
log = logging.getLogger(__name__)


class Isapre(models.Model):
    _name = 'hr.isapre'
    _description = 'Información ISAPRE'

    partner_id = fields.Many2one(
        string='Contacto',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    name = fields.Char(string='Nombre', required=True)
    rut = fields.Char('RUT', required=True)
    codigo = fields.Char('Codigo', required=True)
