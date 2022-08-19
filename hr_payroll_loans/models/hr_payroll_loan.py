# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date

import logging
log = logging.getLogger(__name__)

class HrPayrollLoan(models.Model):
	_name = 'hr.payroll.loan'
	_description = 'Prestamos de nominas'

	name = fields.Char(string='Secuencia de Préstamo', required=True, copy=False, default="New")
	employee_id = fields.Many2one('hr.employee', string='Empleado', required=True, copy=False)
	avg_amount = fields.Float(string='Valor promedio de la cuota', default=0.0)
	months = fields.Integer(string='Cantidad de cuotas', default=0)
	start_at = fields.Date(string='Fecha de inicio')
	notes = fields.Text(string='Notas')
	company_id = fields.Many2one(string='Compañia', comodel_name='res.company', required=True, default=lambda self: self.env.company)
	state = fields.Selection([('draft','Borrador'),
		('open','Abierto'),
		('closed','Cerrado')], string='Estado', default='draft')
	line_ids = fields.One2many('hr.payroll.loan.line', 'loan_id', string='Cuotas de préstamo')
		
	@api.model
	def create(self, vals):
		if 'company_id' in vals:
			self = self.with_company(vals['company_id'])
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('hr.payroll.loan') or _('New')

		result = super(HrPayrollLoan, self).create(vals)
		return result
	
	def unlink(self):
		for loan in self:
			# Prevent deleting lines on posted entries
			if not self.env.context.get('force_delete', False) and loan.state != 'draft':
				raise UserError('No puede eliminar un pedido ya iniciado')
		res = super(HrPayrollLoan, self).unlink()
		return res

	def fill_lines(self):
		self.write({
			'line_ids': [5]
		})
		for line in self.line_ids:
			line.unlink()
		lines = []
		for i in range(self.months):
			lines.append([0,0,{
				'name': int(i+1),
				'total_amount': self.avg_amount
			}])
		self.write({
			'line_ids': lines
		})

	def action_open(self):
		if len(self.line_ids) == 0:
			raise UserError('Debe establecer las cuotas antes de validar el préstamo')
		self.write({
			'state': 'open'
		})

	def action_draft(self):
		self.write({
			'state': 'draft'
		})

class HrPayrollLoanLine(models.Model):
	_name = 'hr.payroll.loan.line'
	_description = 'Lineas de prestamos de nominas'

	loan_id = fields.Many2one('hr.payroll.loan')
	name = fields.Integer(string='Cuota', default=0)
	total_amount = fields.Float(string='Valor de la cuota', default=0.0)
	#due_date = fields.Date(string='Fecha de vencimiento')
	state = fields.Selection([('open','Por cobrar'),
		('paid','Pagada')], string="Estado", default='open')
	payslip_id = fields.Many2one('hr.payslip', string='Boleta de pago')