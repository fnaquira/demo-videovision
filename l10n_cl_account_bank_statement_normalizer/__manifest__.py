# -*- coding: utf-8 -*-
{
    'name' : 'Normalizador de Extractos Bancarios',
    'version' : '14.0.1',
    'summary': 'Normalizardor de estractos bancarios a archivos CSV para Odoo',
    'sequence': 30,
    'description': """""",
    'category': 'Account',
    'website': 'https://conflux.pe',
    'depends' : ['account', 'account_accountant'],
    'data': [
        "security/ir.model.access.csv",
        "wizards/account_bank_statement_normalizer.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}