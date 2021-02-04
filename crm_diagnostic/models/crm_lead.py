# -*- coding: utf-8 -*-
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, time, timedelta
import logging

_logger = logging.getLogger(__name__)

CRM_DIAGNOSTIC_SELECTION_FIELDS = {
    'doctype': 'tipo_documento',
    'x_ubic': 'ubicacion',
    'x_actcomer': 'actividad_micronegocio',
    'x_microneg': 'tipo_micronegocio',
    }

ANSWER_VALUES = {
        'si': 5,
        'en_proceso': 3,
        'no': 1,
        'no_aplica': 0,
        'totalmente_de_acuerdo': 5,
        'de_acuerdo': 4,
        'ni_de_acuerdo_ni_en_desacuerdo': 3,
        'en_desacuerdo': 2,
        'totalmente_en_desacuerdo': 1
    }

TEXT_VALUATION = {
        1: 'Incipiente',
        2: 'Aceptable',
        3: 'Confiable',
        4: 'Competente',
        5: 'Excelencia'
    }

SUGGEST_VALUATION = {
    'x_proto1': {
        1: 'Acompañamiento y asesoría en la implementación de los protocolos de bioseguridad según la actividad económica del micronegocio.',
        2: 'Acompañamiento y asesoría en la implementación de los protocolos de bioseguridad según la actividad económica del micronegocio.',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto2': {
        1: 'Acompañamiento y asesoría en la implementación de los protocolos de bioseguridad según la actividad económica del micronegocio.',
        2: 'Acompañamiento y asesoría en la implementación de los protocolos de bioseguridad según la actividad económica del micronegocio.',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto3': {
        1: 'Buscar proyectos y programas públicos y privados que subsidien o faciliten la obtención de tapabocas y elementos de protección para el micronegocio',
        2: 'Buscar proyectos y programas públicos y privados que subsidien o faciliten la obtención de tapabocas y elementos de protección para el micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto4': {
        1: 'Buscar proyectos y programas públicos y privados que subsidien o faciliten la obtención de tapabocas y elementos de protección para el micronegocio',
        2: 'Buscar proyectos y programas públicos y privados que subsidien o faciliten la obtención de tapabocas y elementos de protección para el micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto6': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto7': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto8': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto9': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto10': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto11': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto12': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto13': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto14': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto15': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_proto16': {
        1: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        2: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        3: '',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_model21': {
        1: 'Capacitar al propietario en el diseño del modelo de negocio.',
        2: 'Capacitar al propietario en el diseño del modelo de negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model22': {
        1: 'Capacitar al propietario en el diseño del modelo de negocio.',
        2: 'Capacitar al propietario en el diseño del modelo de negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model23': {
        1: 'Capacitar al propietario del negocio sobre los canales de distribución y definir cuál es el más adecuado para el producto o servicio',
        2: 'Capacitar al propietario del negocio sobre los canales de distribución y definir cuál es el más adecuado para el producto o servicio',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model24': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model25': {
        1: 'Determinar los conocimiento y habilidades que requieren los trabajadores para laborar en el micronegocio',
        2: 'Determinar los conocimiento y habilidades que requieren los trabajadores para laborar en el micronegocio',
        3: 'Fortalecer los conocimiento y habilidades que requieren los trabajadores para laborar en el micronegocio',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model26': {
        1: 'Acompañamiento en programas de manipulación de alimentos',
        2: 'Acompañamiento en programas de manipulación de alimentos',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model27': {
        1: 'Capacitar al propietario del negocio en seguridad y salud en el trabajo',
        2: 'Capacitar al propietario del negocio en seguridad y salud en el trabajo',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model28': {
        1: 'Definir procedimientos, instrucciones y normas que se deben tener para producir alimentos saludables',
        2: 'Definir procedimientos, instrucciones y normas que se deben tener para producir alimentos saludables',
        3: 'Fortalecer los procedimientos e instrucciones para cumplir con las normas que se requiere al producir alimentos.',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model29': {
        1: 'Acompañamiento en la búsqueda y selección de proveedores que mejor se adecuen a las necesidades del negocio',
        2: 'Acompañamiento en la búsqueda y selección de proveedores que mejor se adecuen a las necesidades del negocio',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model30': {
        1: 'Orientar al personal sobre los beneficios que puede obtener en cada uno de los pagos.',
        2: 'Orientar al personal sobre los beneficios que puede obtener en cada uno de los pagos.',
        3: 'Fortalecer al propietario en finanzas para que tenga claridad en los pagos a crédito.',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model31': {
        1: 'Capacitar al propietario del negocio en proyecciones de compra.',
        2: 'Capacitar al propietario del negocio en proyecciones de compra.',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model32': {
        1: 'Acompañamiento en la definición de procesos estandarizado para la producción o manipulación del producto',
        2: 'Acompañamiento en la definición de procesos estandarizado para la producción o manipulación del producto',
        3: 'Fortalecimiento en los procesos estandarizado para la producción o manipulación del producto',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model33': {
        1: 'Acompañamiento en la definición de proceso estandarizado para la producción o manipulación del producto',
        2: 'Acompañamiento en la definición de proceso estandarizado para la producción o manipulación del producto',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model34': {
        1: 'Acompañamiento en la definición de controles de existencias, que permitan conocer los productos de mayor demanda y realizar compras inteligentes.',
        2: 'Acompañamiento en la definición de controles de existencias, que permitan conocer los productos de mayor demanda y realizar compras inteligentes.',
        3: 'Fortalecer los controles de existencias, que permitan conocer los productos de mayor demanda y realizar compras inteligentes.',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model35': {
        1: 'Acompañamiento para el diseño de instrumentos que les permita tener los registro de las entradas y salidas para mayor control de los inventarios.',
        2: 'Acompañamiento para el diseño de instrumentos que les permita tener los registro de las entradas y salidas para mayor control de los inventarios.',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model36': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_model37': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_innova24': {
        1: 'Capacitar al propietario en la identificación de costos y gastos propios del negocio.',
        2: 'Capacitar al propietario en la identificación de costos y gastos propios del negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova25': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova26': {
        1: 'Capacitar al propietario en la definición del punto de equilibrio del negocio.',
        2: 'Capacitar al propietario en la definición del punto de equilibrio del negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova27': {
        1: 'Capacitar al propietario en la definición del punto de equilibrio del negocio.',
        2: 'Capacitar al propietario en la definición del punto de equilibrio del negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_prodl42': {
        1: 'Acompañamiento en diseño modelo de negocio innovador',
        2: 'Acompañamiento en diseño modelo de negocio innovador',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_prodl43': {
        1: 'Diseñar un plan de formación para los trabajadores',
        2: 'Diseñar un plan de formación para los trabajadores',
        3: 'Fortalecimiento del plan de formación para los trabadores',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova29': {
        1: 'Apoyo en el diseño de la cultura organizacional',
        2: 'Apoyo en el diseño de la cultura organizacional',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova33': {
        1: 'Formar al propietario en creatividad e innovación',
        2: 'Formar al propietario en creatividad e innovación',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_prodl46': {
        1: 'Acompañamiento en diseño modelo de negocio innovador',
        2: 'Acompañamiento en diseño modelo de negocio innovador',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_prodl47': {
        1: 'Acompañamiento en diseño modelo de negocio innovador',
        2: 'Acompañamiento en diseño modelo de negocio innovador',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova39': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'PRODUCCIÓN'
        },
    'x_innova40': {
        1: 'Acompañamiento para el análisis interno y externo del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        2: 'Acompañamiento para el análisis interno y externo del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        3: 'Fortalecer el análisis interno y externo que realiza el propietario del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        4: '',
        5: '',
        'area': 'INNOVACIÓN'
        },
    'x_ninova50': {
        1: 'Acompañamiento para el análisis interno y externo del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        2: 'Acompañamiento para el análisis interno y externo del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACIÓN'
        },
    'x_innova43_inf': {
        1: 'Acompañamiento para el análisis interno y externo del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        2: 'Acompañamiento para el análisis interno y externo del negocio para identificar los factores que influyen positiva y negativamente, y las oportunidades, fortalezas, debilidades y amenazas propias del negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACIÓN'
        },
    'x_ninova52': {
        1: 'Acompañar al propietario del negocio en la definición de la planeación estratégica del negocio.',
        2: 'Acompañar al propietario del negocio en la definición de la planeación estratégica del negocio.',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACIÓN'
        },
    'x_ninova53': {
        1: 'Diseñar una estrategia para que los trabajadores apropien la cultura organizacional',
        2: 'Diseñar una estrategia para que los trabajadores apropien la cultura organizacional',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACIÓN'
        },
    'x_ninova54': {
        1: 'Orientar al propietario del negocio en normas y estándares de calidad',
        2: 'Orientar al propietario del negocio en normas y estándares de calidad',
        3: '',
        4: '',
        5: '',
        'area': 'INNOVACIÓN'
        },
    'x_for55': {
        1: 'Orientar al propietario del negocio en normas y estándares de calidad',
        2: 'Orientar al propietario del negocio en normas y estándares de calidad',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_forma50_inf': {
        1: 'Acompañamiento y asesoría en las obligaciones correspondientes del negocio',
        2: 'Acompañamiento y asesoría en las obligaciones correspondientes del negocio',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_forma52_inf': {
        1: 'Acompañamiento y asesoría en las obligaciones correspondientes del negocio',
        2: 'Acompañamiento y asesoría en las obligaciones correspondientes del negocio',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_forma54_inf': {
        1: 'Acompañamiento en Innovación en el modelo de Negocio',
        2: 'Acompañamiento en Innovación en el modelo de Negocio',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_forma56_inf': {
        1: 'Acompañamiento y asesoría sobre las obligaciones tributarias correspondientes a la actividad económica del negocio',
        2: 'Acompañamiento y asesoría sobre las obligaciones tributarias correspondientes a la actividad económica del negocio',
        3: 'Acompañamiento para realizar una adecuada liquides de las obligaciones tributarias correspondientes a la actividad económica del negocio',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_los_empl': {
        1: 'Acompañamiento en Innovación en el modelo de Negocio',
        2: 'Acompañamiento en Innovación en el modelo de Negocio',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_org61': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org62': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org63': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org64': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org65': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org66': {
        1: 'Acompañamiento y asesoría sobre las obligaciones correspondientes a los trabajadores que laboran en el negocio',
        2: 'Acompañamiento y asesoría sobre las obligaciones correspondientes a los trabajadores que laboran en el negocio',
        3: 'Acompañamiento para realizar una adecuada liquides de las obligaciones correspondientes a los trabajadores que laboran en el negocio',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org67': {
        1: 'Acompañamiento en el diseño de estrategias para comercialización de producto o servicios',
        2: 'Acompañamiento en el diseño de estrategias para comercialización de producto o servicios',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_org68': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'ORGANIZACIÓN'
        },
    'x_mer69': {
        1: 'Acompañamiento en el diseño de estrategias para la visibilidad de los producto o servicios',
        2: 'Acompañamiento en el diseño de estrategias para la visibilidad de los producto o servicios',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer70': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer71': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer72': {
        1: 'Acompañamiento en el diseño de estrategias de marketing digital',
        2: 'Acompañamiento en el diseño de estrategias de marketing digital',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer73': {
        1: 'Acompañamiento en el diseño de estrategias de marketing digital',
        2: 'Acompañamiento en el diseño de estrategias de marketing digital',
        3: 'Fortalecimiento en el diseño de estrategias de marketing digital',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer74': {
        1: 'Diseñar e implementar estrategias que permitan visibilizar y comercializar el producto o servicio a través de redes sociales',
        2: 'Diseñar e implementar estrategias que permitan visibilizar y comercializar el producto o servicio a través de redes sociales',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer75': {
        1: 'Acompañamiento y asesoría en el uso de internet para realizar actividades propias del negocio',
        2: 'Acompañamiento y asesoría en el uso de internet para realizar actividades propias del negocio',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_merc86_form': {
        1: 'Acompañamiento en el diseño e implementación de planes de seguimiento y fidelización de clientes',
        2: 'Acompañamiento en el diseño e implementación de planes de seguimiento y fidelización de clientes',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_finan92_form': {
        1: 'Acompañamiento en la definición de la Marca',
        2: 'Acompañamiento en la definición de la Marca',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_finan93_form': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_fin85': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_finan98_form': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_finan99_form': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_fin88': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_fin89': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_fin90': {
        1: 'Acompañamiento en el diseño de estrategias de fidelización de clientes',
        2: 'Acompañamiento en el diseño de estrategias de fidelización de clientes',
        3: 'Fortalecimiento en el diseño de estrategias de fidelización de clientes',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_finan104_form': {
        1: 'Acompañamiento en el diseño de técnicas y estrategias para la captación de nuevos clientes',
        2: 'Acompañamiento en el diseño de técnicas y estrategias para la captación de nuevos clientes',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },

}

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    crm_lead_id = fields.One2many(
        'crm.diagnostic',
        'lead_id',
        string='CRM Diagnostic',
        copy=False)

    # returning an action to go to crm.diagnostic form view related to lead
    def action_crm_diagnostic_view(self):
        for record in self:
            # validating if it is necessary to create a new diagnistic record or return the first on the list
            if len(record.crm_lead_id) > 0:
                return record.action_to_return_to_crm_diagnostic(record.crm_lead_id[0])
            else:
                crm_diagnostic_vals = record.getting_values_to_crm_diagnostic()
                crm_diagnostic_id = self.env['crm.diagnostic'].create(crm_diagnostic_vals)
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
            dic_vals['crm_diagnostic_line_ids'] = lead.prepare_diagnostic_lines(lead)
            return dic_vals

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
        dic_fields = lead.read()[0]
        _fields = self.env['ir.model.fields'].search(
            [('name', 'ilike', 'x_'),
             ('model_id.model', '=', lead._name),
             ('selectable', '=', True),
             ('ttype', '=', 'selection')]).filtered(
                 lambda f : f.name.startswith('x_'))
        for field in _fields:
            field_value = dic_fields.get(field.name)
            # TODO
            # validating if the field value is in ANSWER_VALUES
            # we obtain certain values from lead on its field what is iterating
            if field_value in ANSWER_VALUES:
                answer = dict(lead._fields[field.name].selection).get(getattr(lead, field.name))
                score = ANSWER_VALUES.get(field_value)
                valuation = TEXT_VALUATION.get(score)
                suggestion, area = self.get_sugestion(field.name, score)
                lines.append(
                    (0, 0, {
                        'name': field.field_description,
                        'respuesta': answer,
                        'puntaje': score,
                        'area': area,
                        'sugerencia': suggestion,
                        'valoracion': valuation,
                        }))
        return lines

    # returning area and suggestion base on field_name and score
    @api.model
    def get_sugestion(self, field_name, score):
        suggestion = False
        area = False
        # TODO if any param comes in False we immediatly return values in False
        if not score or not field_name:
            return suggestion, area
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
