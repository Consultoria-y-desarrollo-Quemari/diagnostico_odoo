# -*- coding: utf-8 -*-
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import logging

_logger = logging.getLogger(__name__)


class CrmDiagnostic(models.Model):
    _name = 'crm.diagnostic'
    _rec_name = 'diagnostico'


    lead_id = fields.Many2one('crm.lead')
    fecha = fields.Date("Fecha")
    nombre_negocio = fields.Char(string="Nombre del Negocio")
    nombre_propietario = fields.Char(string="Nombre del Propietario")
    tipo_documento = fields.Char(string="Tipo de Documento")
    ubicacion = fields.Char(string="Ubicación")
    actividad_micronegocio = fields.Char(string="Actividad del Micronegocio")
    tipo_micronegocio = fields.Char(string="Tipo de Negocio")
    numero_identificacion = fields.Char(string="Numero de Identificacion")
    codigo_formulario = fields.Char(string="Codigo de formulario")
    valoracion_micronegocio = fields.Char(string="Valoracion del Micronegocio")
    diagnostico = fields.Text(string="Diagnostico")
    crm_diagnostic_line_ids = fields.One2many(
        'crm.diagnostic.line',
        'diagnostic_id'
    )


    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        res = super(CrmDiagnostic, self.with_context(context)).create(vals)
        return res

