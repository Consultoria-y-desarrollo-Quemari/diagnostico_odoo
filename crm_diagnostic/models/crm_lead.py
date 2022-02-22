# -*- coding: utf-8 -*-
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from lxml import etree
import json
import logging

_logger = logging.getLogger(__name__)


RANGES = {
        'incipiente': range(0, 47),
        'confiable': range(48, 93),
        'competente': range(94, 132),
        'excelencia': range(133, 155)
    }

CRM_DIAGNOSTIC_SELECTION_FIELDS = {
    'doctype': 'tipo_documento',
    'x_ubic': 'ubicacion',
    'x_forma41': 'actividad_micronegocio',
    'x_microneg': 'tipo_micronegocio',
    }

ANSWER_VALUES = {
        'si': 5,
        'en_proceso': 3,
        'parcialmente' : 3,
        'no': 1,
        'cuenta_del_negocio' : 5,
        'cuenta_personal' : 5,
        'los_dos_tipos_cuenta' : 5,
        'no_tiene' : 1,
        'no_empleados' : 5,
        'no_regulaciones' : 5,
    }

TEXT_VALUATION = {
        1: 'Incipiente',
        2: 'Confiable',
        3: 'Confiable',
        4: 'Competente',
        5: 'Excelencia'
    }

M2M_FIELDS = ['x_neg6', 'x_neg5', 'x_mer_com32', 'x_mer_com34', 'x_forma51']

SELECTION_FIELDS = [
    'x_innova_org_1', 'x_innova_org_2', 'x_innova_org_3', 'x_innova_org_4', 'x_innova_org_5',
    'x_innova_org_6', 'x_neg4','x_neg7', 'x_neg8', 'x_neg14', 'x_financiero18',
    'x_financiero20', 'x_financiero21', 'x_financiero22', 'x_financiero23', 'x_financiero24',
    'x_financiero25', 'x_mer_com30', 'x_mer_com31', 'x_mer_com38', 'x_mer_com39',
    'x_forma44', 'x_forma45', 'x_forma46', 'x_forma47_1', 'x_forma49_1',
    'x_neg16', 'x_financiero26', 'x_fin97n'
    ]

SELECTION_FIELDS_WO_POINTS = [
    'x_neg16', 'x_financiero26', 'x_fin97n'
    ]

SUGGEST_VALUATION = {
    # 1
    'x_innova_org_1': {
        1: 'Remitir a talleres o cursos de innovación con el objetivo de prototipar y lanzar nuevos productos o servicios en su micronegocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACION'
        },
    # 2
    'x_innova_org_2': {
        1: 'Buscar y explicar de nuevas herramientas tecnológicas que puedan mejorar los procesos o productividad del micronegocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACION'
        },
    # 3
    'x_innova_org_3': {
        1: 'Acompañar y capacitar acerca de hábitos de planeación y organización, así como el diseño de un registro para llevar el cumplimiento de un plan y las metas',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACION'
        },
    # 4
    'x_innova_org_4': {
        1: 'Acompañar y capacitar aspectos de planeación estratégica, así como la definición de una misión, visión y objetivos a largo plazo del micronegocio',
        2: 'Revisar y hacer sugerencias acerca de la misión, visión y objetivos a largo plazo del micronegocio',
        3: 'Revisar y hacer sugerencias acerca de la misión, visión y objetivos a largo plazo del micronegocio',
        4: '',
        5: '',
        'area': 'INNOVACION'
        },
    # 5
    'x_innova_org_5': {
        1: 'Acompañar y capacitar acerca de la elaboración y seguimientos de los registros de inventario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACION'
        },
    # 6
    'x_innova_org_6': {
        1: 'Identificar alternativas y/o acciones necesarias para adecuar su espacio de trabajo',
        2: 'Revisar y hacer sugerencias acerca de los cambios necesarios para adecuar correctamente su espacio de trabajo',
        3: 'Revisar y hacer sugerencias acerca de los cambios necesarios para adecuar correctamente su espacio de trabajo',
        4: '',
        5: '',
        'area': 'INNOVACION'
        },
    # 7
    'x_neg4': {
        1: 'Definir para quién está creando valor y quienes son sus clientes más importantes y la posibilidad de agrupar estos por medio de sus características, definir como aumentar su satisfacción',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    # 8 
    'x_neg6': {
        1: 'Ajustar los canales comerciales de acuerdo a la propuesta de valor y sus clientes',
        2: 'Requiere explorar más canales , afinarlos y ponerlos a funcionar',
        3: 'Requiere explorar más canales , afinarlos y ponerlos a funcionar',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    # 9
    'x_neg7': {
        1: 'Buscar apoyo en herramientas tecnológicas o registros donde pueda llevar el control y supervisión de los clientes para generar estrategias de fidelización y compra más frecuente',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    # 10
    'x_neg8': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    # 14
    'x_neg14': {
        1: 'Gestionar acuerdos con proveedores',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    # 15
    'x_neg16': {
        0: 'Definir el valor que quiere entregar a sus clientes, clarificar que problemas o dolores quiere ayudar a resolver, validar si los productos y/o servicios ofrecidos, realmente solucionan problemas o satisfacen las necesidades de los clientes',
        'area': 'MODELO DE NEGOCIO'
        },
    # 17
    'x_financiero18': {
        1: 'Orientar al propietario del negocio acerca de los hábitos positivos financieros y la importancia de llevar registros económicos',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 19
    'x_financiero20': {
        1: 'Orientar al propietario del negocio acerca de los hábitos positivos financieros y la importancia de llevar registros económicos',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 20
    'x_financiero21': {
        1: 'Acompañar y explicar el proceso para calcular el punto de equilibrio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 21
    'x_financiero22': {
        1: 'Acompañar y explicar los beneficios de la Inclusión financiera para el acceso a los productos del sistema bancario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 22
    'x_financiero23': {
        1: 'Explicar procesos de agrupación y reestructuración de los pagos de la deuda, idealmente para que todo quede asociado a un solo acreedor',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 23
    'x_financiero24': {
        1: 'Remitir a un asesor de una entidad bancaria para que realicen el proceso de asesoramiento y determinación del monto máximo de endeudamiento',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 24
    'x_financiero25': {
        1: 'Acompañar y capacitar aspectos de educación financiera para la búsqueda e implementación de una herramienta (Excel, SIIGO) que permita realizar los registros contables del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    # 25
    'x_financiero26': {
        0: 'Remitir a la Cooperativa Minuto de Dios',
        'area': 'FINANZAS'
        },
    # 27
    'x_neg5': {
        1: 'Definir el valor que quiere entregar a sus clientes, clarificar que problemas o dolores quiere ayudar a resolver, validar si los productos y/o servicios ofrecidos, realmente solucionan problemas o satisfacen las necesidades de los clientes',
        2: 'Validar los productos y/o servicios ofrecidos, para lograr asegurar que realmente solucionan problemas o satisfacen las necesidades de los clientes',
        3: 'Validar los productos y/o servicios ofrecidos, para lograr asegurar que realmente solucionan problemas o satisfacen las necesidades de los clientes',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 28
    'x_mer_com30': {
        1: 'Acompañar en el diseño de estrategias para la visibilidad de los productos o servicios',
        2: 'Acompañar en el diseño de estrategias para la visibilidad de los productos o servicios',
        3: 'Acompañar en el diseño de estrategias para la visibilidad de los productos o servicios',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 29
    'x_mer_com31': {
        1: 'Acompañar en el diseño de estrategias para la visibilidad de los productos o servicios',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 30
    'x_mer_com32': {
        1: 'Acompañar en la identificación de oportunidades de mercado y nuevos segmentos de clientes',
        2: 'Acompañar en la definición del plan de marketing',
        3: 'Acompañar en la definición del plan de marketing',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 32
    'x_mer_com34': {
        1: 'Acompañar en el diseño de estrategias para la visibilidad de los producto o servicios',
        2: 'Acompañar en la definición del plan de marketing',
        3: 'Acompañar en la definición del plan de marketing',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 34
    'x_mer_com38': {
        1: 'Acompañar en el uso de redes sociales para promocionar y posicionar su negocio y productos',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 35
    'x_mer_com39': {
        1: 'Acompañar en el uso de herramientas digitales para promoción de sus productos (uso de redes sociales o el desarrollo de páginas web)',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    # 36
    'x_forma44': {
        1: 'Acompañar y asesorar en los procesos para la formalización del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    # 37
    'x_forma45': {
        1: 'Acompañar y asesorar en los procesos para la formalización del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    # 38
    'x_forma46': {
        1: 'Acompañar y asesorar en los procesos para la formalización del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    # 40
    'x_forma47_1': {
        1: 'Acompañar y asesorar en los procesos de pagos parafiscales para sus empleados',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    # 43
    'x_forma49_1': {
        1: 'Revisar las regulaciones del sector y plantear con el propietario un plan de trabajo para empezar a cumplirlas',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    # 44
    'x_fin97n': {
        0: 'Remitir al programa de Empleabilidad',
        'area': 'FORMALIZACION'
        },
}

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    crm_lead_id = fields.One2many(
        'crm.diagnostic',
        'lead_id',
        string='CRM Diagnostic',
        copy=False)

    mentors = fields.Many2one(
        'res.partner',
        string='Mentores',
    )

    coordinador = fields.Many2one(
        'res.users',
        string='Coordinador'
    )
    diagnostico = fields.Selection(
        selection=[
            ('competitividad', 'Nivel de competitividad'),
            ('incipiente', 'Incipiente'),
            ('aceptable', 'Aceptable'),
            ('confiable', 'Confiable'),
            ('competente', 'Competente'),
            ('excelencia', 'Excelencia')],
        string='Diagnostico'
    )
    # computed fields
    first_module_ready = fields.Boolean(
        compute='compute_first_module'
    )
    second_module_read = fields.Boolean(
        compute='compute_second_module'
    )
    third_module_ready = fields.Boolean(
        compute='compute_third_module'
    )
    current_user = fields.Many2one(
        'res.users',
        compute='get_current_user'
    )
    root_current_user = fields.Boolean(
        compute='current_user_is_root'
    )
    current_user_facilitator = fields.Boolean(
        compute='current_user_is_facilitator'
    )
    current_user_mentor = fields.Boolean(
        compute="current_user_is_mentor"
    )
    current_user_admin = fields.Boolean(
        compute="current_user_is_admin"
    )

    social_plan = fields.Boolean(default = False)

    facilitator_role = fields.Char(compute="get_facilitator_role")

    show_action_set_rainbowman = fields.Boolean(compute="compute_show_action_set_rainbowman")

    def confirm_social_plan(self):
        stage_after = self.env['crm.stage'].search([('stage_after_confirm_social_plan', '=', True)])
        for lead in self:
            lead.social_plan = True
            if stage_after:
                lead.with_user(SUPERUSER_ID).stage_id = stage_after[0]

    # returning an action to go to crm.diagnostic form view related to lead
    def action_crm_diagnostic_view(self):
        for record in self:
            # we avoid to execute the diagnostic whether question modules haven't executed yet
            if (not record.is_cordinator() or not record.is_orientador()) and (not record.first_module_ready or not record.second_module_read or not record.third_module_ready):
                raise ValidationError('Para realizar el diagnostico, debe responder las preguntas de los 3 modulos.')
            crm_diagnostic_vals = record.getting_values_to_crm_diagnostic()
            crm_diagnostic_id = self.env['crm.diagnostic'].create(crm_diagnostic_vals)
            crm_diagnostic_id._get_lines_for_areas()
            _logger.info("&"*500)
            _logger.info(crm_diagnostic_id.read())
            crm_diagnostic_id.valuacion_diagnostico = record.diagnostico
            return record.action_to_return_to_crm_diagnostic(crm_diagnostic_id)

    # return a dic values for crm.diagnostic
    def getting_values_to_crm_diagnostic(self):
        for lead in self:
            dic_vals = {
                'lead_id': lead.id,
                'fecha': fields.Date.today(),
                'nombre_negocio': lead.x_nombre_negocio,
                'nombre_propietario': lead.x_nombre,
                'numero_identificacion': lead.x_identification,
                'crm_diagnostic_line_ids': []
            }
            dic_sel_fields = lead.getting_selection_fields_to_dignostic_form(lead)
            dic_vals.update(dic_sel_fields)
            results = lead.prepare_diagnostic_lines(lead)
            innovation = []
            bussiness = []
            formalization = []
            marketing = []
            finance = []

            for result in results:
                if 'INNOVACION' in result:
                    innovation.append(result.get('INNOVACION'))
                if 'MODELO DE NEGOCIO' in result:
                    bussiness.append(result.get('MODELO DE NEGOCIO'))
                if 'FORMALIZACION' in result:
                    formalization.append(result.get('FORMALIZACION'))
                if 'MERCADEO Y COMERCIALIZACION' in result:
                    marketing.append(result.get('MERCADEO Y COMERCIALIZACION'))
                if 'FINANZAS' in result:
                    finance.append(result.get('FINANZAS'))

            if len(innovation):
                puntaje1 = 0
                count1 = 0
                for dic in innovation:
                    if type(dic).__name__ == 'dict':
                        if 'puntaje' in dic.keys():
                            print(dic.get('puntaje'))
                            puntaje1 += int(dic.get('puntaje'))
                            count1 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                    elif type(dic).__name__ == 'tuple':
                        if 'puntaje' in dic[2].keys():
                            puntaje1 += int(dic[1].get('puntaje'))
                            count1 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                dic_vals['calificacion1'] = puntaje1

                if puntaje1 in range(0,9):
                    valoracion = 'Incipiente'
                elif puntaje1 in range(10,18):
                    valoracion = 'Confiable'
                elif puntaje1 in range(19,26):
                    valoracion = 'Competente'
                elif puntaje1 > 26:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_innovation'] = valoracion
                
            if len(bussiness):
                puntaje2 = 0
                count2 = 0
                for dic in bussiness:
                    if type(dic).__name__ == 'dict':
                        if 'puntaje' in dic.keys():
                            print(dic.get('puntaje'))
                            puntaje2 += int(dic.get('puntaje'))
                            count2 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                    elif type(dic).__name__ == 'tuple':
                        if 'puntaje' in dic[2].keys():
                            puntaje2 += int(dic[2].get('puntaje'))
                            count2 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                dic_vals['calificacion2'] = puntaje2

                if puntaje2 in range(0,8):
                    valoracion = 'Incipiente'
                elif puntaje2 in range(9,15):
                    valoracion = 'Confiable'
                elif puntaje2 in range(16,21):
                    valoracion = 'Competente'
                elif puntaje2 > 21:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_neg'] = valoracion
    
            if len(formalization):
                puntaje3 = 0
                count3 = 0
                for dic in formalization:
                    if type(dic).__name__ == 'dict':
                        if 'puntaje' in dic.keys():
                            print(dic.get('puntaje'))
                            puntaje3 += int(dic.get('puntaje'))
                            count3 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                    elif type(dic).__name__ == 'tuple':
                        if 'puntaje' in dic[2].keys():
                            puntaje3 += int(dic[2].get('puntaje'))
                            count3 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                dic_vals['calificacion3'] = puntaje3

                if puntaje3 in range(0,8):
                    valoracion = 'Incipiente'
                elif puntaje3 in range(9,15):
                    valoracion = 'Confiable'
                elif puntaje3 in range(16,22):
                    valoracion = 'Competente'
                elif puntaje3 > 22:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_forma'] = valoracion

            if len(marketing):
                puntaje4 = 0
                count4 = 0
                for dic in marketing:
                    if type(dic).__name__ == 'dict':
                        if 'puntaje' in dic.keys():
                            print(dic.get('puntaje'))
                            puntaje4 += int(dic.get('puntaje'))
                            count4 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                    elif type(dic).__name__ == 'tuple':
                        if 'puntaje' in dic[2].keys():
                            puntaje4 += int(dic[2].get('puntaje'))
                            count4 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                dic_vals['calificacion4'] = puntaje4

                if puntaje4 in range(0,11):
                    valoracion = 'Incipiente'
                elif puntaje4 in range(10,21):
                    valoracion = 'Confiable'
                elif puntaje4 in range(19,30):
                    valoracion = 'Competente'
                elif puntaje4 > 30:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_merca'] = valoracion

            if len(finance):
                puntaje5 = 0
                count5 = 0
                for dic in finance:
                    count5 += 1
                    if type(dic).__name__ == 'dict':
                        if 'puntaje' in dic.keys():
                            print(dic.get('puntaje'))
                            puntaje5 += int(dic.get('puntaje'))
                            count5 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                    elif type(dic).__name__ == 'tuple':
                        if 'puntaje' in dic[2].keys():
                            puntaje5 += int(dic[2].get('puntaje'))
                            count5 += 1
                            dic_vals['crm_diagnostic_line_ids'].append((0, 0, dic))
                dic_vals['calificacion5'] = puntaje5
                
                if puntaje5 in range(0,12):
                    valoracion = 'Incipiente'
                elif puntaje5 in range(13,24):
                    valoracion = 'Confiable'
                elif puntaje5 in range(25,34):
                    valoracion = 'Competente'
                elif puntaje5 > 34:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_finanza'] = valoracion

            _logger.info("?"*500)
            _logger.info(dic_vals)
        return dic_vals

    @api.model
    def _get_valoracion_bio(self, puntaje):
        if puntaje <= 2:
            valoracion = 'Incipiente'
        elif puntaje == 3:
            valoracion = 'Confiable'
        elif puntaje == 4:
            valoracion = 'Competente'
        elif puntaje >= 5:
            valoracion = 'Excelencia'

        return valoracion


    # getting str values from selection fields
    @api.model
    def getting_selection_fields_to_dignostic_form(self, lead):
        dic_fields = lead.read()[0]
        dic_selection_fields = {}
        for k, v in CRM_DIAGNOSTIC_SELECTION_FIELDS.items():
            for key in dic_fields:
                if k == key:
                    dic_selection_fields[v] = dict(lead._fields[k].selection).get(getattr(lead, k))
        return dic_selection_fields

    # return a list of values to create diagnostic lines
    @api.model
    def prepare_diagnostic_lines(self, lead):
        lines = []
        lines_dict = []
        dic_fields = lead.read()[0]
        _fields = self.env['ir.model.fields'].search(
            [('name', 'ilike', 'x_'),
             ('model_id.model', '=', lead._name)]).filtered(
                 lambda f : f.name.startswith('x_'))
        puntaje = 0
        for field in _fields:
            field_value = dic_fields.get(field.name)
            # TODO
            # validating if the field value is in ANSWER_VALUES
            # we obtain certain values from lead on its field what is iterating
            if field.ttype == 'selection' and field.name in SELECTION_FIELDS:
                if field_value in ANSWER_VALUES:
                    answer = dict(lead._fields[field.name].selection).get(getattr(lead, field.name))
                    score = ANSWER_VALUES.get(field_value)
                    if field.name in SELECTION_FIELDS_WO_POINTS and answer == 'Si':
                        score = 0
                    valuation = TEXT_VALUATION.get(score)
                    suggestion, area = self.get_sugestion(field.name, score)
                    if area:
                        values = {
                                'name': field.field_description,
                                'respuesta': answer,
                                'puntaje': score,
                                'area': area,
                                'sugerencia': suggestion,
                                'valoracion': valuation,
                                }
                        lines_dict.append({area:values})

            if field.ttype == 'many2many' and field.name in M2M_FIELDS:
                if field.name == 'x_forma51':
                    continue
                answers = getattr(lead, field.name)
                score = 0
                for answer in answers:
                    score += answer.puntaje
                if score > 5:
                    score = 5
                valuation = TEXT_VALUATION.get(score)
                suggestion, area = self.get_sugestion(field.name, score)
                if area:
                    values = {
                            'name': field.field_description,
                            'respuesta': answers,
                            'puntaje': score,
                            'area': area,
                            'sugerencia': suggestion,
                            'valoracion': valuation,
                            }
                    lines_dict.append({area:values})
                if score and area:
                    puntaje += score
        self.set_diagnostico(puntaje, lead)
        return lines_dict

    # set diagnostico based on range
    @api.model
    def set_diagnostico(self, score, lead):
        _logger.info(score)
        if score > 156:
            lead.diagnostico = 'excelencia'
            return
        for k, v in RANGES.items():
            if score in v:
                lead.diagnostico = k

    # this method is called from cron
    def relate_events_to_leads(self):
        lead_ids = self.search(
            [('mentors', '=', False),
            ('diagnostico', 'in', ('incipiente', 'confiable', 'competente'))])
        if not lead_ids:
            return
        event_ids = event_ids = self.available_events().sorted(reverse=True)
        if not event_ids:
            return
        for lead in lead_ids:
            if event_ids and lead_ids:
                event_ids[0].opportunity_id = lead.id
                lead.mentors = event_ids[0].partner_ids[0]
                self.send_mail_notification(lead)
                event_ids -= event_ids[0]
                lead_ids -= lead
                self.env.cr.commit()

    # send email notification to coordinador and facilitador
    @api.model
    def send_mail_notification(self, lead_id):
        try:
            template_id = self.env.ref('crm_diagnostic.q_mail_template_event_notification')
            template_id.send_mail(lead_id.id, force_send=False)
        except Exception as e:
            print(e)

    # return events availables
    def available_events(self):
        week_days = range(1, 6)
        date_to_search = fields.Datetime.now().replace(hour=0, minute=0) + timedelta(days=1)
        events = self.env['calendar.event'].search(
            [('start_datetime', '>', date_to_search),
            ('opportunity_id', '=', False)])
        _logger.info(events)
        for event in events:
            if event.start_datetime.weekday() not in week_days:
                events -= event
        _logger.info(len(events))
        return events

    # returning area and suggestion base on field_name and score
    @api.model
    def get_sugestion(self, field_name, score):
        # suggestion = False
        # area = False
        # TODO if any param comes in False we immediatly return values in False
        # if not score or not field_name:
        #     return suggestion, area
        if field_name in SUGGEST_VALUATION:
            suggestion = SUGGEST_VALUATION[field_name].get(score, False)
            area = SUGGEST_VALUATION[field_name].get('area', False)
        return suggestion, area

    @api.model
    def action_to_return_to_crm_diagnostic(self, crm_diagnostic_id):
        search_view = self.env.ref('crm_diagnostic.crm_diagnostic_view')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'crm.diagnostic',
            'res_id': crm_diagnostic_id.id,
            'views': [(search_view.id, 'form')],
            'view_id': search_view.id,
            'target': 'current',
            'flags': {'mode': 'readonly', 'action_buttons': True},
        }

##########################################################################
#                            ROLE METHODS
##########################################################################

    # set the current user
    @api.depends('current_user')
    def get_current_user(self):
        for lead in self:
            lead.current_user = self.env.user.id

    # check if the current user is facilitator
    @api.depends('current_user')
    def current_user_is_facilitator(self):
        for lead in self:
            if lead.is_facilitator():
                lead.current_user_facilitator = True
            else:
                lead.current_user_facilitator = False
    
    # check if the curren user is mentor
    @api.depends('current_user')
    def current_user_is_mentor(self):
        for lead in self:
            if lead.is_mentor():
                lead.current_user_mentor = True
            else:
                lead.current_user_mentor = False

    @api.depends('current_user')
    def current_user_is_admin(self):
        for lead in self:
            if lead.is_admin():
                lead.current_user_admin = True
            else:
                lead.current_user_admin = False
                
    @api.depends('user_id')
    def get_facilitator_role(self):
        for lead in self:
            facilitator_roles = lead.user_id.role_ids
            if facilitator_roles:
                facilitator_role = facilitator_roles[0].name

                if facilitator_role:
                    lead.facilitator_role = facilitator_role
                else:
                    lead.facilitator_role = ''
            else:
                lead.facilitator_role = ''

    @api.depends()
    def compute_show_action_set_rainbowman(self):
        for lead in self:
            if lead.stage_id.allow_mark_as_won:
                lead.show_action_set_rainbowman = True
            else:
                lead.show_action_set_rainbowman = False



    # check if the current user is admin user
    @api.depends('current_user')
    def current_user_is_root(self):
        for lead in self:
            try:
                root = self.env.ref('base.user_admin').id
                if root == lead.current_user.id or lead.is_cordinator() or lead.is_orientador():
                    lead.root_current_user = True
                else:
                    lead.root_current_user = False
            except Exception as e:
                lead.root_current_user = False
                print(e)

    def write(self, values):
        if len(values) == 1 and 'stage_id' in values:
                    if self.is_facilitator():
                        raise ValidationError("No tienes permiso para cambiar de etapa directamente. {}".format(values))
        return super(CrmLead, self).write(values)


    # return the field list to validate the module1
    def fields_module1(self):
        return [
            'x_datos1', 'attach_file', "x_nombre_negocio", "x_nombre", "doctype",
            "x_identification", "x_sexo", "x_edad", "state_id", "xcity", "x_dir_res",
            "x_comuna", "x_vereda", "x_ubicacion_negocio", "mobile", "x_estrato", 
            "x_pobl_esp", "x_tipo_vivienda", "x_no_personas_viven_propietario", "x_etnia", "x_sisben",
            "x_afiliado", "x_escolaridad", "x_ubic", "x_com_cuenta", "x_tien_dur", "x_herramientas", "x_depend"
            ]

    # return the field list to validate the module2
    def fields_module2(self):
        return ['x_cont1', 'first_module_ready']

    # methos that return list of fields by section
    def fields_module3_generalities(self):
        return [
            'x_datos3'
        ]

    # MÓDULO 3 INNOVACIÓN, OPERACIÓN Y ORGANIZACIÓN
    def fields_module3_inno_org_op(self):
        return [
            'x_innova_org_1', 'x_innova_org_2', 'x_innova_org_3',
            'x_innova_org_4', 'x_innova_org_5', 'x_innova_org_6',
        ]

    #MODULO 3 MODELO DE NEGOCIOS
    def fields_module3_business_model(self):
        return [
            'x_neg4', 'x_neg6', 'x_neg7',
            'x_neg8', 'x_neg14',
        ]

    #MODELO 3 FINANCIERO
    def fields_module3_financial(self):
        return [
            'x_financiero18', 'x_financiero20', 'x_financiero21',
            'x_financiero22', 'x_financiero23', 'x_financiero24',
            'x_financiero25',
        ]

    #MODELO 3 MERCADEO
    def fields_module3_marketing(self):
        return [
            'x_neg5', 'x_mer_com30', 'x_mer_com31',
            'x_mer_com32', 'x_mer_com34', 'x_mer_com38',
            'x_mer_com39',
        ]

    #MODELO 3 FORMALIZACION
    def fields_module3_formalization(self):
        return [
            'x_forma44', 'x_forma45', 'x_forma46',
            'x_forma47_1', 'x_forma49_1',
        ]

    def full_list_field(self):
        full_fields = []
        full_fields.extend(self.fields_module3_generalities())
        full_fields.extend(self.fields_module3_inno_org_op())
        full_fields.extend(self.fields_module3_business_model())
        full_fields.extend(self.fields_module3_financial())
        full_fields.extend(self.fields_module3_marketing())
        full_fields.extend(self.fields_module3_formalization())
        full_fields.extend(['second_module_read'])
        return full_fields
    # ended section

    # validating if the current user has the facilitador profile
    def is_facilitator(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'facilitador')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    # validating if the current user has the cordinator profile
    def is_cordinator(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'coordinador')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    # validating if the current user has the mentor profile
    def is_mentor(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'mentor')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False
    
    def is_orientador(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'orientador')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    def is_admin(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'admin')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    def is_administrativo(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'administrativo')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    def is_estudiante(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'estudiante')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    # computed if the module1 is ok
    @api.depends(fields_module1)
    def compute_first_module(self):
        for lead in self:
            if lead.is_facilitator() or lead.is_admin():
                if lead.all_fields_module1_are_ok():
                    lead.first_module_ready = True
                else:
                    lead.first_module_ready = False
            elif lead.is_cordinator() or lead.is_orientador() or lead.is_mentor() or lead.is_admin():
                lead.first_module_ready = True
            else:
                lead.first_module_ready = False

    # computed if the module2 is ok
    @api.depends(fields_module2)
    def compute_second_module(self):
        for lead in self:
            if (lead.is_facilitator() or lead.is_admin()) and lead.first_module_ready:
                if lead.all_fields_module2_are_ok():
                    lead.second_module_read = True
                else:
                    lead.second_module_read = False
            elif lead.is_cordinator() or lead.is_orientador() or lead.is_mentor() or lead.is_admin():
                lead.second_module_read = True
            else:
                lead.second_module_read = False

    # computed if the module3 is ok
    @api.depends(full_list_field)
    def compute_third_module(self):
        for lead in self:
            if (lead.is_facilitator() or lead.is_admin()) and lead.second_module_read:
                if lead.all_fields_module3_are_ok():
                    lead.third_module_ready = True
                else:
                    lead.third_module_ready = False
            elif lead.is_cordinator() or lead.is_orientador() or lead.is_mentor() or lead.is_admin():
                lead.third_module_ready = True
            else:
                lead.third_module_ready = False

    # validating it all fields of module3 were filled
    def all_fields_module3_are_ok(self):
        result = []
        result.append(self.check_inno_org_op(self.fields_module3_inno_org_op()))
        result.append(self.check_business_model_fields(self.fields_module3_business_model()))
        result.append(self.check_financial_fields(self.fields_module3_financial()))
        result.append(self.check_marketing_fields(self.fields_module3_marketing()))
        result.append(self.check_formalization_fields(self.fields_module3_formalization()))
        if any(r == False for r in result):
            return False
        else:
            return True

    # checking if all generalities field section are ok
    def check_generalities_fields(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # cheking if all innovation fields section are ok
    def check_inno_org_op(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # checking if all business model field section are ok
    def check_business_model_fields(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # checking if all financial field section are ok
    def check_financial_fields(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # checking if all marketing field section are ok
    def check_marketing_fields(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # checking if all formalization field section are ok
    def check_formalization_fields(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # validating it all fields of module1 were filled
    def all_fields_module1_are_ok(self):
        fields = self.fields_module1()
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # validating it all fields of module2 were filled
    def all_fields_module2_are_ok(self):
        if getattr(self, 'x_cont1') and getattr(self, 'x_cont1') == 'si':
            return True
        elif (getattr(self, 'x_cont1') and getattr(self, 'x_cont1') == 'no') and getattr(self, 'x_cont1_por'):
            return False
        else:
            return False

    # getting the stage by stage state
    @api.model
    def get_stage(self, stage_state):
        stage_id = self.env['crm.stage'].sudo().search([('stage_state', '=', stage_state)], limit=1)
        return stage_id

    # change the stage on lead according if the question modules
    @api.onchange('first_module_ready', 'second_module_read', 'third_module_ready')
    def update_stage(self):
        if (self.is_facilitator()  or self.is_cordinator()):
            if self.first_module_ready:
                second_stage =  self.get_stage('segundo_encuentro')
                self.with_user(SUPERUSER_ID).stage_id = second_stage if second_stage else self.stage_id
            if self.first_module_ready and self.second_module_read:
                third_stage =  self.get_stage('tercer_encuentro')
                self.with_user(SUPERUSER_ID).stage_id = third_stage if third_stage else self.stage_id
            if self.first_module_ready and self.second_module_read and self.third_module_ready:
                fourth_stage =  self.get_stage('espera_de_plan')
                self.with_user(SUPERUSER_ID).stage_id = fourth_stage if fourth_stage else self.stage_id

    # inherit method to validate if the current user has the cordinator profile
    # if so then we set readonly=False on mentors field
    @api.model
    def fields_view_get(
            self, view_id=None, view_type='form', toolbar=False,
            submenu=False):
        res = super(CrmLead, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if self.is_cordinator():
                for node in doc.xpath("//field[@name='mentors']"):
                    if 'modifiers' in node.attrib:
                        modifiers = json.loads(node.attrib['modifiers'])
                        modifiers['readonly'] = False
                        node.attrib['modifiers'] = json.dumps(modifiers)
                    if 'options' in node.attrib:
                        options = json.loads(node.attrib['options'])
                        options['no_create'] = True
                        options['no_open'] = True
                        node.attrib['options'] = json.dumps(options)

                #res['arch'] = etree.tostring(doc)
            if self.is_facilitator():
                for node in doc.xpath("//header/field[@name='stage_id']"):
                    if 'options' in node.attrib:
                        node.attrib.pop('options')

                #res['arch'] = etree.tostring(doc)

                for node in doc.xpath("//field[@name='mentors']"):
                    if not 'options' in node.attrib:
                        options = json.loads(node.attrib['options'])
                        options['no_create'] = False
                        options['no_open'] = False
                        node.attrib['options'] = json.dumps(options)

            if not self.is_mentor():
                if not self.is_admin():
                    if not self.is_facilitator():
                        for node in doc.xpath("//header/button[@name='action_set_won_rainbowman']"):
                            if 'modifiers' in node.attrib:
                                modifiers = json.loads(node.attrib['modifiers'])
                                modifiers['invisible'] = True
                                node.attrib['modifiers'] = json.dumps(modifiers)

            #            res['arch'] = etree.tostring(doc)

            if not self.is_mentor():
                if not self.is_admin():
                    if not self.is_facilitator():
                        for node in doc.xpath("//header/field[@name='stage_id']"):
                            if 'modifiers' in node.attrib:
                                modifiers = json.loads(node.attrib['modifiers'])
                                modifiers['readonly'] = True
                                node.attrib['modifiers'] = json.dumps(modifiers)

            res['arch'] = etree.tostring(doc)
        #import pdb; pdb.set_trace()
        return res

    @api.onchange('x_nombre_negocio')
    def _onchange_x_nombre_negocio(self):
        if self.x_nombre_negocio:
            self.x_nombre_negocio = str(self.x_nombre_negocio).upper()

    @api.onchange('name')
    def _onchange_name(self):
        chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '\\', ':', ';', '<', '=', '>', '?', '@', '[',  ']', '^', '_', '`', '{', '|', '}', '~']
        delimiter = ''
        for char in chars:
            if char in str(self.name) :
                raise ValidationError(('No se permiten caracteres especiales en el Nombre del Propietario: {}'.format(delimiter.join(chars))))
    
    @api.onchange('x_nombre')
    def _onchange_x_nombre(self):
        chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '\\', ':', ';', '<', '=', '>', '?', '@', '[',  ']', '^', '_', '`', '{', '|', '}', '~']
        delimiter = ''
        for char in chars:
            if char in str(self.x_nombre) :
                raise ValidationError(('No se permiten caracteres especiales en el Nombre del Propietario: {}'.format(delimiter.join(chars))))
##########################################################################
#                           ATTENTION PLAN METHODS
##########################################################################
    crm_attenation_plan_ids = fields.One2many(
        'crm.attention.plan',
        'lead_id',
        copy=False)

    # returning an action to go to crm.attention.plan form view related to lead
    def call_action_crm_attention_plan(self):
        for record in self:
            # validating if it is necessary to create a new attention plan record or return the first on the list
            if len(record.crm_attenation_plan_ids) > 0:
               return record.action_to_return_to_crm_attention_plan(record.crm_attenation_plan_ids[0])
            else:
                if len(record.crm_lead_id) <= 0:
                    # we avoid to execute the attention plan whether diagnostic haven't executed yet
                    raise ValidationError('No puede realizar el plan de atención sin antes haber realizado el diagnostico.')
                attention_plan_vals = record.getting_values_to_crm_attention_plan()
                crm_attention_id = self.env['crm.attention.plan'].create(attention_plan_vals)
                crm_attention_id.diagnostico = record.diagnostico
            return record.action_to_return_to_crm_attention_plan(crm_attention_id)

    # return a dic values for crm.diagnostic
    def getting_values_to_crm_attention_plan(self):
        for lead in self:
            dic_vals = {
                'lead_id': lead.id,
                'nombre_negocio': lead.x_nombre_negocio,
                'ubicacion': lead.x_dir_neg,
                'fecha': fields.Date.today(),
                'plan_line_ids': lead.get_attention_plan_lines()
            }
            return dic_vals

    def get_attention_plan_lines(self):
        lines = []
        items = ['48 H', '1 Semana', '2 Semanas', '1 Mes', 'A futuro', 'Hábitos a desarrollar']
        for item in items:
            lines.append(
                (0, 0, {
                    'prioridad': item,
                    'actividades': False,
                    'soluciones': False,
                    'reponsable': False,
                }))
        return lines

    @api.model
    def action_to_return_to_crm_attention_plan(self, crm_attention_id):
        form_view = self.env.ref('crm_diagnostic.q_crm_attention_plan_form_view')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'crm.attention.plan',
            'res_id': crm_attention_id.id,
            'views': [(form_view.id, 'form')],
            'view_id': form_view.id,
            'target': 'current',
        }
