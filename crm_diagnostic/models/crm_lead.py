# -*- coding: utf-8 -*-
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    crm_lead_id = fields.One2many('crm.diagnostic', 'lead_id', string='CRM Diagnostic', copy=False)


    def action_crm_diagnostic_view(self):
        # import pdb; pdb.set_trace()
        for record in self:
            search_view = self.env.ref('crm_diagnostic.crm_diagnostic_view')
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'crm.diagnostic',
                'res_id': record.crm_lead_id.id,
                'views': [(search_view.id, 'form')],
                'view_id': search_view.id,
                'target': 'current',
                'context': {
                    'default_partner_id': self.id,
                },
            }
