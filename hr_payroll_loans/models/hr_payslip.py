# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date

import logging
log = logging.getLogger(__name__)

class HrPayslip(models.Model):
	_inherit = 'hr.payslip'

	def action_payslip_done(self):
		super(HrPayslip, self).action_payslip_done()
		if self.env.context.get('payslip_generate_pdf'):
			regular_payslips = self.filtered(lambda p: p.struct_id.type_id.default_struct_id == p.struct_id)
			for regular_payslip in regular_payslips:
				if len(regular_payslip.employee_id.loan_ids) > 0:
					active_loan = regular_payslip.employee_id.loan_ids.filtered(lambda r: r.state == 'open')
					if len(active_loan) > 0:
						active_loan = active_loan[0]
						lines = active_loan.line_ids.filtered(lambda r: r.state == 'open')
						lines[0].write({
							'state': 'paid',
							'payslip_id': regular_payslip.id
						})