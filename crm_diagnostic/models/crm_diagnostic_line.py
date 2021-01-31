# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError



class CrmDiagnosticLine(models.Model):
    _name = 'crm.diagnostic.line'
    _description = 'Líneas de diagnostico'

    ANSWER_VALUES = {
        'SI': 5,
        'En proceso': 3,
        'NO': 1,
        'No aplica': 0,
        'Totalmente de acuerdo': 5,
        'De acuerdo': 4,
        'Ni de acuerdo': 3,
        'ni en desacuerdo': 3,
        'En desacuerdo': 2,
        'Totalmente en desacuerdo': 1
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
    name = fields.Text(
        string='Pregunta',
        help='Este campo es usado para guardar la pregunta pero también es '
             'usado para guardar el valor de notas y secciones, el tipo de dato '
             'de este debe ser Text, ya que solo así odoo lo reconoce como una '
             'sección o una nota y hace el render de la línea mediante el '
             'widget, el nombre técnico del campo siempre tiene que ser name.'
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
    display_type = fields.Selection([
        ('line_section', "Sección"),
        ('line_note', "Nota")],
        default=False,
        help="Technical field for UX purpose.")


    @api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(respuesta=False, puntaje=False,
                area=False, sugerencia=False, valoracion=False)
        return super(CrmDiagnosticLine, self).create(values)
