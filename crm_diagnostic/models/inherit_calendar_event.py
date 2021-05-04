# -*- encoding: utf-8 -*-
from odoo import models, fields, api


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'


    @api.model_create_multi
    def create(self, vals_list):
        results = super(CalendarEvent, self).create(vals_list)
        for res in results:
            res.write({'allday': False})
            res.write({'duration': 2})
        return results
