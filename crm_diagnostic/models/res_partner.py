# -*- encoding: utf-8 -*-
from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection(string='Tipo de Contacto', selection=[
        ('facilitador', 'Facilitador'),
        ('estudiante', 'Estudiante'),
        ('coordinador', 'Orientador'),
        ('orientador', 'Orientador'),
        ('administrativo', 'Administrativo'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin')
    ])