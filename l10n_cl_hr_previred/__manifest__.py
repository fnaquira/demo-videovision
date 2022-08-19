# -*- coding: utf-8 -*-
{
    'name' : 'Chile Previred txt',
    'version' : '14.0.1',
    'summary': 'Personalizacion de Chile Previred txt',
    'sequence': 30,
    'description': """
Personalizacion de Chile Previred txt
    """,
    'category': 'Localization',
    'website': 'https://conflux.pe',
    'depends' : ['l10n_cl_hr','wizard_files'],
    'data': [
        "views/hr_employee_views.xml",
        "views/hr_contract_views.xml",
        "security/ir.model.access.csv",
        # "wizards/previred_txt.xml",
        "wizards/wizard_export_csv_previred_view.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}