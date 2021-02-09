# -*- coding: utf-8 -*-
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import logging

import plotly.express as px
import pandas as pd
import base64

# import io


_logger = logging.getLogger(__name__)


class CrmDiagnostic(models.Model):
    _name = 'crm.diagnostic'
    _rec_name = 'nombre_negocio'


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
    company_id = fields.Many2one(
        'res.company',
        default=lambda self : self.env.company)
    # principal records
    crm_diagnostic_line_ids = fields.One2many(
        'crm.diagnostic.line',
        'diagnostic_id',
    )
    # records for Orientaciones de bioseguridad
    crm_diagnostic_line_orientation_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Modelo de Negocio
    crm_diagnostic_line_business_model_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Producción
    crm_diagnostic_line_production_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Innovación
    crm_diagnostic_line_innovation_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Formalización
    crm_diagnostic_line_formalization_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Organización
    crm_diagnostic_line_organization_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Mercadeo y Comercialización
    crm_diagnostic_line_marketing_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')
    # records for Finanzas
    crm_diagnostic_line_finance_ids = fields.One2many(
        'crm.diagnostic.line',
        compute='_get_lines_for_areas')

    #diagnostic_chart = fields.Char(
    #    compute='_get_chart', store=False)

    diagnostic_chart = fields.Char(
        compute='_get_chart', store=True)

    @api.depends('crm_diagnostic_line_ids')
    def _get_lines_for_areas(self):
        for record in self:
            record.crm_diagnostic_line_orientation_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'PROTOCOLOS DE BIOSEGURIDAD')
            record.crm_diagnostic_line_business_model_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'MODELO DE NEGOCIO')
            record.crm_diagnostic_line_production_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'PRODUCCIÓN')
            record.crm_diagnostic_line_innovation_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'INNOVACIÓN')
            record.crm_diagnostic_line_formalization_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'FORMALIZACION')
            record.crm_diagnostic_line_organization_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'ORGANIZACIÓN')
            record.crm_diagnostic_line_marketing_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'MERCADEO Y COMERCIALIZACION')
            record.crm_diagnostic_line_finance_ids = record.crm_diagnostic_line_ids.filtered(
                lambda line : line.area == 'FINANZAS')

    @api.depends('crm_diagnostic_line_ids')
    def _get_chart(self):
        for diagnostic in self:
            modelonegocio = 0
            bioseguridad = 0
            formalizacon = 0
            mercadeo = 0
            finanzas = 0

            for line in diagnostic.crm_diagnostic_line_business_model_ids:
                modelonegocio += int(line.puntaje)
            for line in diagnostic.crm_diagnostic_line_orientation_ids:
                bioseguridad += int(line.puntaje)
            for line in diagnostic.crm_diagnostic_line_formalization_ids:
                formalizacon += int(line.puntaje)
            for line in diagnostic.crm_diagnostic_line_marketing_ids:
                mercadeo += int(line.puntaje)
            for line in diagnostic.crm_diagnostic_line_finance_ids:
                finanzas += int(line.puntaje)

            data_chart = [(modelonegocio/.80), (bioseguridad/.85), (formalizacon/.45), (mercadeo/.60), (finanzas/.65)] 
            print(data_chart)
            df = pd.DataFrame(dict(
                r=data_chart,
                theta=['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
                    'Mercadeo y Comercializacion ', 'Finanzas']))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            image_data = fig.to_html()
            diagnostic.diagnostic_chart = image_data

    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        res = super(CrmDiagnostic, self.with_context(context)).create(vals)
        return res

