# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date

import logging
log = logging.getLogger(__name__)

class HrEmployee(models.Model):
	_inherit = 'hr.employee'

	loan_ids = fields.One2many('hr.payroll.loan', 'employee_id', string='Préstamos del empleado', readonly=True)
	loan_count = fields.Integer(compute='_compute_loan_count', string='Loan Count', groups="hr_payroll.group_hr_payroll_user")
	
	def _compute_loan_count(self):
		for employee in self:
			employee.loan_count = len(employee.loan_ids)
