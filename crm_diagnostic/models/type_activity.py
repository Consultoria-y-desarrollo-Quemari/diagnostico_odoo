from odoo import _, api, fields, models, tools

class TypeActivity(models.Model):
    _name = 'crm.lead.type_activity'
    _description = "Opciones para el tipo de actividad"

    tipo_actividad = fields.Char()
    name = fields.Char()