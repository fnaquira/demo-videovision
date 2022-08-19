# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    last_name = fields.Char('Apellido Paterno', required=True)
    mother_last_name = fields.Char('Apellido Materno')
    first_name = fields.Char('Nombres', required=True)

    @api.model
    def create(self, vals):
        name = vals.get('last_name')
        name += (' ' + vals['mother_last_name'] if vals['mother_last_name'] else '') + ', ' + vals.get('first_name')
        vals['name'] = name
        res = super(HrEmployee, self).create(vals)
        return res

    def write(self, vals):
        print(vals)
        if 'mother_last_name' in vals and isinstance(vals['mother_last_name'], str):
            name = self.last_name
            if name == False:
                name = vals['last_name']
            if self.first_name:
                name += (' ' + vals['mother_last_name'] if vals['mother_last_name'] else '') + ', ' + self.first_name
            elif 'first_name' in vals:
                name += (' ' + vals['mother_last_name'] if vals['mother_last_name'] else '') + ', ' + vals['first_name']
            else:
                name += (' ' + vals['mother_last_name'] if vals['mother_last_name'] else '')
            vals['name'] = name
        res = super(HrEmployee, self).write(vals)
        return res