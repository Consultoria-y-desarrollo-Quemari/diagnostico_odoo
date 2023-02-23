# -*- encoding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    stage_state =  fields.Selection(
        string='Estado de la etapa',
        selection=[('primer_encuentro', 'Primer encuentro'),
                   ('segundo_encuentro', 'Segundo encuentro'),
                   ('tercer_encuentro', 'Tercer encuentro'),
                   ('espera_de_plan', 'En espera de plan de atención'),
                   ('cuarto_encuentro', 'Cuarto encuentro: Ejecución Plan de atención'),
                   ('pre_finalizacion', 'Pre finalización'),
                   ('quinto_encuentro', 'Quinto'),
                   ('finalizar', 'finalizar')],
        help='Esta campo sirve para el estado al que pertence la etapa'
    )

    allow_mark_as_won = fields.Boolean(string='Permitir marcar como ganado',
                                        default=False)

    stage_after_confirm_social_plan = fields.Boolean(string='Etapa asignada una vez confirmada la socialización del plan de atención', default=False)

    @api.onchange('stage_after_confirm_social_plan')
    def _onchange_stage_after_confirm_social_plan(self):
        stage_after = self.search([('stage_after_confirm_social_plan', '=', True)])

        if stage_after and self.stage_after_confirm_social_plan:
            self.stage_after_confirm_social_plan = False
            raise ValidationError('La etapa {} ya esta marcada para ser asignada una vez confirmada la socialización del plan de atención.'.format(stage_after[0].name))

            

