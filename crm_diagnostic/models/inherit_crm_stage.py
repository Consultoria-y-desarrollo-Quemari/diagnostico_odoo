# -*- encoding: utf-8 -*-
from odoo import models, fields


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    stage_state =  fields.Selection(
        string='Estado de la etapa',
        selection=[('primer_encuentro', 'Primer encuentro'),
                   ('segundo_encuentro', 'Segundo encuentro'),
                   ('tercer_encuentro', 'Tercer encuentro'),
                   ('espera_de_plan', 'En espera de plan de atención')],
        required=True,
        help='Esta campo sirve para el estado al que pertence la etapa'
    )
