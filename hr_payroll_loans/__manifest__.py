# -*- coding: utf-8 -*-
{
	'name' : 'Gestion de prestamos simples para nominas',
	'version' : '14.0.1',
	'summary': 'Gestion de prestamos simples para nominas',
	'sequence': 30,
	'description': """
Gestion de prestamos simples para nominas
	""",
	'category': 'Localization',
	'website': 'https://conflux.pe',
	'depends' : ['hr_payroll'],
	'data': [
		'security/ir.model.access.csv',
		'data/ir_sequence_data.xml',
		'views/hr_payroll_loan_views.xml',
		'views/hr_employee_views.xml'
	],
	'installable': True,
	'application': False,
	'auto_install': False,
}