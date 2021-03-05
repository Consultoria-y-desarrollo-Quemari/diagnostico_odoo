# -*- encoding: utf-8 -*-
from odoo import models, fields


class CrmAttentionPlan(models.Model):
    _name = 'crm.attention.plan'
    _rec_name = 'nombre_negocio'


    nombre_negocio = fields.Char(
        string='Nombre del negocio'
    )
    ubicacion = fields.Char(
        string='Ubicación'
    )
    responsable = fields.Char(
        string='Responsable'
    )
    fecha = fields.Date(
        string='Fecha'
    )
    diagnostico = fields.Selection(
        selection=[
            ('competitividad', 'Nivel de competitividad'),
            ('incipiente', 'Incipiento'),
            ('aceptable', 'Aceptable'),
            ('confiable', 'Confiable'),
            ('competente', 'Competente'),
            ('excelencia', 'Excelencia')],
        string='Diagnostico'
    )
    #programa de entrenamiento
    programa = fields.Char(
        string='Programa'
    )
    duración = fields.Char(
        string='Duración (horas)'
    )
    inicia = fields.Char(
        string='Inicia'
    )
    finaliza = fields.Char(
        string='Finaliza'
    )
    plataforma = fields.Char(
        string='Plataforma'
    )
    enlace = fields.Char(
        string='Enlace para ingresar'
    )
    soluciones = fields.Text(
        string='Soluciones'
    )
    # cursos virtuales
    cvc_programa = fields.Char(
        string='Programa'
    )
    cvc_duración = fields.Char(
        string='Duración (horas)'
    )
    cvc_inicia = fields.Char(
        string='Inicia'
    )
    cvc_finaliza = fields.Char(
        string='Finaliza'
    )
    cvc_plataforma = fields.Char(
        string='Plataforma'
    )
    cvc_enlace = fields.Char(
        string='Enlace para ingresar'
    )
    cvc_soluciones = fields.Text(
        string='Soluciones'
    )
    #mentorias
    tema = fields.Char(
        string='Tema'
    )
    mentor = fields.Char(
        string='Mentor'
    )
    horario = fields.Char(
        string='Horario'
    )
    m_soluciones = fields.Text(
        string='Soluciones'
    )
    #indicadores
    indicador1 = fields.Char(
        string='Indicador 1'
    )
    indicador2 = fields.Char(
        string='Indicador 2'
    )
    #Lineas
    plan_line_ids = fields.One2many(
        'crm.attention.plan.line',
        'crm_attention_id'
    )
    lead_id = fields.Many2one(
        'crm.lead'
    )
    partner_id = fields.Many2one(
        'res.partner',
        related='lead_id.partner_id'
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self : self.env.company)



class CrmAttentionPlanLines(models.Model):
    _name = 'crm.attention.plan.line'

    crm_attention_id = fields.Many2one(
        'crm.attention.plan'
    )
    prioridad = fields.Char(
        string='Prioridad'
    )
    actividades = fields.Char(
        string='Actividades'
    )
    soluciones = fields.Char(
        string='Soluciones'
    )
    reponsable = fields.Char(
        string='Responsable'
    )