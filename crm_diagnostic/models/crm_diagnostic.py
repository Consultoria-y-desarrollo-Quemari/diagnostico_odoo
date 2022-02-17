# -*- coding: utf-8 -*-
import re
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import logging

import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
from math import pi

import io


_logger = logging.getLogger(__name__)


class CrmDiagnostic(models.Model):
    _name = 'crm.diagnostic'
    _rec_name = 'nombre_negocio'


    lead_id = fields.Many2one('crm.lead')
    fecha = fields.Date("Fecha")
    nombre_negocio = fields.Char(string="Nombre del Negocio", required=True)
    nombre_propietario = fields.Char(string="Nombre del Propietario")
    tipo_documento = fields.Char(string="Tipo de Documento")
    ubicacion = fields.Char(string="Ubicación")
    actividad_micronegocio = fields.Char(string="Actividad del Micronegocio")
    tipo_micronegocio = fields.Char(string="Tipo de Negocio")
    numero_identificacion = fields.Char(string="Numero de Identificacion")
    codigo_formulario = fields.Char(string="Codigo de formulario")
    valoracion_micronegocio = fields.Char(string="Valoracion del Micronegocio")
    diagnostico = fields.Text(string="Diagnostico")
    valuacion_diagnostico = fields.Selection(
        selection=[
            ('competitividad', 'Nivel de competitividad'),
            ('incipiente', 'Incipiento'),
            ('aceptable', 'Aceptable'),
            ('confiable', 'Confiable'),
            ('competente', 'Competente'),
            ('excelencia', 'Excelencia')],
        string='Valuación de diagnostico'
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self : self.env.company)
    # principal records
    crm_diagnostic_line_ids = fields.One2many(
        'crm.diagnostic.line',
        'diagnostic_id', store=True
    )
    crm_diagnostic_line_innovation_model_ids = fields.One2many(
        'crm.diagnostic.line.innovation', 'diagnostic_id',
        )
    # records for Modelo de Negocio
    crm_diagnostic_line_business_model_ids = fields.One2many(
        'crm.diagnostic.line.business', 'diagnostic_id',
        )
    # records for Formalización
    crm_diagnostic_line_formalization_ids = fields.One2many(
        'crm.diagnostic.line.formalization', 'diagnostic_id',
        )
    # records for Mercadeo y Comercialización
    crm_diagnostic_line_marketing_ids = fields.One2many(
        'crm.diagnostic.line.marketing', 'diagnostic_id',
        )
    # records for Finanzas
    crm_diagnostic_line_finance_ids = fields.One2many(
        'crm.diagnostic.line.finance', 'diagnostic_id',
        )

    # records for Producción
    crm_diagnostic_line_production_ids = fields.One2many(
        'crm.diagnostic.line', 'diagnostic_id',
        )
    # records for Innovación
    crm_diagnostic_line_innovation_ids = fields.One2many(
        'crm.diagnostic.line', 'diagnostic_id',
        )
    # records for Organización
    crm_diagnostic_line_organization_ids = fields.One2many(
        'crm.diagnostic.line', 'diagnostic_id',
        )

    calificacion = fields.Char()
    calificacion1 = fields.Char()
    calificacion2 = fields.Char()
    calificacion3 = fields.Char()
    calificacion4 = fields.Char()
    calificacion5 = fields.Char()
    valoracion_bio = fields.Char()
    valoracion_innovation = fields.Char()
    valoracion_neg = fields.Char()
    valoracion_finanza = fields.Char()
    valoracion_merca = fields.Char()
    valoracion_forma = fields.Char()

    diagnostic_chart = fields.Html(
        compute='_get_chart', store=True, sanitize=False)
    char_img = fields.Binary(compute='_get_chart', store=True,)
    char_img_bar = fields.Binary(compute='_get_chart', store=True,)
    diagnostic_chart_two = fields.Char(
    compute='_get_chart', store=True)

    # @api.depends('crm_diagnostic_line_ids')
    def _get_lines_for_areas(self):
      for record in self:
        self.create_suggest_lines_per_model(
            record.crm_diagnostic_line_ids.filtered(
                  lambda line : line.area == 'INNOVACION'), 'crm.diagnostic.line.innovation'
        )
        self.create_suggest_lines_per_model(
            record.crm_diagnostic_line_ids.filtered(
                  lambda line : line.area == 'MODELO DE NEGOCIO'), 'crm.diagnostic.line.business'
        )
        self.create_suggest_lines_per_model(
            record.crm_diagnostic_line_ids.filtered(
                  lambda line : line.area == 'FORMALIZACION'), 'crm.diagnostic.line.formalization'
        )
        self.create_suggest_lines_per_model(
            record.crm_diagnostic_line_ids.filtered(
                  lambda line : line.area == 'MERCADEO Y COMERCIALIZACION'), 'crm.diagnostic.line.marketing'
        )
        self.create_suggest_lines_per_model(
            record.crm_diagnostic_line_ids.filtered(
                  lambda line : line.area == 'FINANZAS'), 'crm.diagnostic.line.finance'
        )

    @api.model
    def create_suggest_lines_per_model(self, line_ids, model):
        for line in line_ids:
            if 'sugerencia' in line:
                sugerencia = line.sugerencia
                area = line.area
                if sugerencia != '':
                    values = {'area' : area, 'sugerencia' : sugerencia, 'diagnostic_id' : self.id}
                    self.env[model].create(values)

    def make_chart_barh(self, data):
        buf = io.BytesIO()
        objects = ['Innovación, \n Organización y \n Operación', 'Modelo \n de Negocio', 'Formalizacion',
                     'Mercadeo \n y \n Comercializacion ', 'Finanzas']
        y_pos = np.arange(len(objects))
        performance = data
        _logger.info("="*500)
        _logger.info(data)
        plt.figure(figsize =(10, 6))
        plt.xlim(0, 100)
        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('Porcentaje')
        plt.title('Porcentaje de cumplimiento')

        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()

    def make_chart_radar(self, data):
        buf = io.BytesIO()
        
        values = [30, 25, 25, 35, 40]
        data += data[:1]
        N = len(values)
        values += values[:1]
        angles = ['Innovación, \n Organización y \n Operación', 'Modelo \n de Negocio', 'Formalizacion',
                     'Mercadeo \n y \n Comercializacion ', 'Finanzas']
        plt.figure(figsize =(10, 6))
        plt.subplot(polar = True)
        theta = np.linspace(0, 2 * np.pi, len(values))
        lines, labels = plt.thetagrids(range(0, 360, int(360/len(angles))),
                                                         (angles))
        plt.plot(theta, values)
        plt.fill(theta, values, 'b', alpha = 0.1)
        plt.plot(theta, data)
        plt.legend(labels =('Puntaje Maximo', 'Puntaje Micronegocio'),
           loc = 3)
        plt.title('Puntuación Diagnostico')
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()


    @api.depends('crm_diagnostic_line_ids')
    def _get_chart(self):
        for diagnostic in self:
            innovacion = float(diagnostic.calificacion1)
            modelonegocio = float(diagnostic.calificacion2)
            formalizacion = float(diagnostic.calificacion3)
            mercadeo = float(diagnostic.calificacion4)
            finanzas = float(diagnostic.calificacion5)

            data_chart = [innovacion, modelonegocio, formalizacion, mercadeo, finanzas] 


            data = self.make_chart_radar(data_chart)
            data2 = self.make_chart_barh([(innovacion * 100) / 30, (modelonegocio * 100) /25, (formalizacion * 100) / 40, (mercadeo * 100) / 35, (finanzas * 100) / 25])
            diagnostic.char_img = base64.b64encode(data)
            diagnostic.char_img_bar = base64.b64encode(data2)

    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        res = super(CrmDiagnostic, self.with_context(context)).create(vals)
        return res
