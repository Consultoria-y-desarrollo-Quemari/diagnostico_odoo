# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError



class CrmDiagnosticLineOrientation(models.Model):
    _name = 'crm.diagnostic.line.orientation'
    _description = 'Líneas de diagnostico orientacion'
    # _rec_name = 'area'

    ANSWER_VALUES = {
        'si': 5,
        'en_proceso': 3,
        'no': 1,
        'no_aplica': 0,
        'totalmente_de_acuerdo': 5,
        'de_acuerdo': 4,
        'ni_de_acuerdo_ni_en_desacuerdo': 3,
        'en_desacuerdo': 2,
        'totalmente_en_desacuerdo': 1
    }

    TEXT_VALUATION = {
        1: 'Incipiente',
        2: 'Aceptable',
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
        return super(CrmDiagnosticLineOrientation, self).create(values)
