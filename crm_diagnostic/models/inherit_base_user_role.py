# -*- encoding: utf-8 -*-
from odoo import models, fields, api


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
                   ('gestor_social', "Gestor social")
                   ],
        default='facilitador',
        required=True,
        help='Esta campo sirve para identificar el tipo de rol al que pertenece '
             'el usuario.'
    )

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.depends('name', 'role_line_ids')     # this definition is recursive
    def name_get(self):
        result = []
        for user in self:
            if user.sudo().role_line_ids:
                result.append((user.id,  user.name + ' - ' + user.sudo().role_line_ids[0].role_id.name))
            else:
                result.append((user.id, user.name))
        return result
