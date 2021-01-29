# -*- coding: utf-8 -*-
{
    'name': 'CRM Diagnostic',
    'version': '0.1',
    'category': 'Crm',
    'summary': 'CRM Diagnostic',
    'description': """
CRM Diagnostic
==============
    """,
    'depends': [
        'base', 'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/crm_diagnostic_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
