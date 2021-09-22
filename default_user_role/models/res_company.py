# -*- coding: utf-8 -*-

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    role_id = fields.Many2one('res.users.role', string='Rol por defecto nuevos usuarios')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    role_id = fields.Many2one('res.users.role', related='company_id.role_id', string='Rol por defecto nuevos usuarios', readonly=False)