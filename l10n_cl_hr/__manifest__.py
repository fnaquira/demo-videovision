{
    'name': 'Chile Payroll',
    'author': 'Conflux',
    'website': 'https://conflux.pe',
    'license': 'AGPL-3',
    'depends': [
            'hr_payroll',
            'hr_payroll_loans'
        ],
    'version': '14.0.0',
    'category': 'Localization/Chile',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/hr_afp_isapre.xml',
        'data/hr_salary_rule.xml',
        'data/hr_entry_type.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_indicator_views.xml',
        'views/hr_payslip_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
