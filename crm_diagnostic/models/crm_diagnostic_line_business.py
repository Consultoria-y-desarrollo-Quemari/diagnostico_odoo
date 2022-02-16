# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError



class CrmDiagnosticLineBusiness(models.Model):
    _name = 'crm.diagnostic.line.business'
    _description = 'Líneas de diagnostico business'
    # _rec_name = 'area'

    ANSWER_VALUES = {
        'si': 5,
        'en_proceso': 3,
        'parcialmente' : 3,
        'no': 1,
    }

    TEXT_VALUATION = {
            1: 'Incipiente',
            2: 'Confiable',
            3: 'Confiable',
            4: 'Competente',
            5: 'Excelencia'
        }


    sequence = fields.Integer(
        default=10)
    name = fields.Char(
        string='Pregunta',
    )
    respuesta =  fields.Char(
        string='Respuesta'
    )
    puntaje = fields.Char(
        string='Puntaje'
    )
    area = fields.Char(
        string='Área'
    )
    sugerencia = fields.Char(
        string='Sugerencia'
    )
    valoracion = fields.Char(
        string='Valoración'
    )
    diagnostic_id = fields.Many2one(
        'crm.diagnostic'
    )


    @api.model
    def create(self, values):
        return super(CrmDiagnosticLineBusiness, self).create(values)
