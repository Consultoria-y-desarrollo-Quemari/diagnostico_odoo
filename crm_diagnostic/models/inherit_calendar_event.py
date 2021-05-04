# -*- encoding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'
