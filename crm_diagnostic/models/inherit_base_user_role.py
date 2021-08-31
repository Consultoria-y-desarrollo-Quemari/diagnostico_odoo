# -*- encoding: utf-8 -*-
from odoo import models, fields


class ResUsersRole(models.Model):
    _inherit = 'res.users.role'

    role_type =  fields.Selection(
        string='Tipo de rol',
        selection=[('facilitador', 'Facilitador'),
                   ('estudiante', 'Estudiante'),
                   ('coordinador', 'Coordinador'),
                   ('orientador', 'Orientador'),
                   ('administrativo', 'Administrativo'),
                   ('mentor', 'Mentor'),
                   ('admin', 'ADMIN'),
                   ],
        default='facilitador',
        required=True,
        help='Esta campo sirve para identificar el tipo de rol al que pertenece '
             'el usuario.'
    )
