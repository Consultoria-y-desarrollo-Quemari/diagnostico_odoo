# -*- coding: utf-8 -*-

{
    'name': 'Default User Role',
    'version': '1.0',
    'category': "Users",
    'summary': 'Add a default role to new users',
    'description': """
    Add a default role to new users
""",
    'depends': [
        'base_user_role'
        ],
    'data': [ 
        'views/res_config_settings_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}