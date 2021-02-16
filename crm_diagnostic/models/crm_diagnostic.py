# -*- coding: utf-8 -*-
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import logging

import plotly.express as px
import pandas as pd
import plotly
import plotly.graph_objects as go
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

    diagnostic_chart = fields.Html(
        compute='_get_chart', store=True, sanitize=False)
    char_img = fields.Binary(compute='_get_chart', store=True,)
    char_img_bar = fields.Binary(compute='_get_chart', store=True,)
    diagnostic_chart_two = fields.Char(
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
    def make_chart_barh(self, data):
        buf = io.BytesIO()
        objects = ['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
                     'Mercadeo y Comercializacion ', 'Finanzas']
        y_pos = np.arange(len(objects))
        performance = data

        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('Usage')
        plt.title('Programming language usage')

        plt.savefig(buf, format='png')
        return buf.getvalue()

    def make_chart_radar(self, data):
        buf = io.BytesIO()
        values = [80,85,45,60,65]
        data += data[:1]
        N = len(values)
        values += values[:1]
        angles = ['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
                     'Mercadeo y Comercializacion ', 'Finanzas']
        # angles += angles[:1]
        plt.figure(figsize =(10, 6)) 
        plt.subplot(polar = True)
        theta = np.linspace(0, 2 * np.pi, len(values))
        lines, labels = plt.thetagrids(range(0, 360, int(360/len(angles))), 
                                                         (angles))
        plt.plot(theta, values)
        plt.fill(theta, values, 'b', alpha = 0.1)
        plt.plot(theta, data)
        plt.legend(labels =('Puntaje Maximo', 'Puntaje Micronegocio'), 
           loc = 1) 
        # plt.polar(angles, values)
        # plt.xticks(angles[:-1], values)
        plt.savefig(buf, format='png')
        return buf.getvalue()
        

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

            data_chart = [modelonegocio, bioseguridad, formalizacon, mercadeo, finanzas] 
            print(data_chart)
            df = pd.DataFrame(dict(
                Valor=[80,85,45,60,65],
                etiqueta=['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
                    'Mercadeo y Comercializacion ', 'Finanzas']))
            fig = px.line_polar(df, r='Valor', theta='etiqueta', line_close=True)
            fig.add_trace(go.Scatterpolargl(
                r = data_chart,
                theta = ['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
                    'Mercadeo y Comercializacion ', 'Finanzas'],
                fill = 'tonext',
            ))

            image_data = fig.to_html(include_plotlyjs=False)
            # im_data = fig.to_image()

            # data = dict(
            #     number=[modelonegocio/0.80, bioseguridad/0.85, formalizacon/0.45, mercadeo/0.60, finanzas/0.60],
            #     stage=['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
            #         'Mercadeo y Comercializacion ', 'Finanzas'])
            fig2 = px.funnel_area(names=['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
                    'Mercadeo y Comercializacion ', 'Finanzas'], values=[modelonegocio/0.80, bioseguridad/0.85, formalizacon/0.45, mercadeo/0.60, finanzas/0.60])
            
            # plt.polar(['Innovacion en el Modelo de Negocio','Protocolo de Bioseguridad','Formalizacion',
            #         'Mercadeo y Comercializacion ', 'Finanzas'], [80,85,45,60,65])
            # plt.ylabel('some numbers')

            # buf = io.BytesIO()
            # self.make_chart_radar().savefig(buf, format='png')
            _logger.info('^'*90)
            data = self.make_chart_radar(data_chart)
            data2 = self.make_chart_barh([modelonegocio/0.80, bioseguridad/0.85, formalizacon/0.45, mercadeo/0.60, finanzas/0.60])
            _logger.info(data)
            diagnostic.char_img = base64.b64encode(data)
            diagnostic.char_img_bar = base64.b64encode(data2)
            image_data = fig.to_html(full_html=False, include_plotlyjs=False)
            image_data2 = fig2.to_html(full_html=False, include_plotlyjs=False)


            diagnostic.diagnostic_chart = image_data
            diagnostic.diagnostic_chart_two = image_data2

    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        res = super(CrmDiagnostic, self.with_context(context)).create(vals)
        return res

