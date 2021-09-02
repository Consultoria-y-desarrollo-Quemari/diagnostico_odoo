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
        'totalmente_en_desacuerdo': 1,
        'promociones': 5,
        'referidos': 5, 
        'redes_sociales': 5,
        'ninguna': 1,
    }

TEXT_VALUATION = {
        1: 'Incipiente',
        2: 'Aceptable',
        3: 'Confiable',
        4: 'Competente',
        5: 'Excelencia'
    }

SUGGEST_VALUATION = {
    'x_proto1_bio': {
        1: 'Buscar proyectos y programas públicos y privados que subsidien o faciliten la obtención de tapabocas y elementos de protección para el micronegocio',
        2: '',
        3: 'Capacitación e implementación en protocolos de bioseguridad para el funcionamiento seguro del micronegocio',
        4: '',
        5: '',
        'area': 'PROTOCOLOS DE BIOSEGURIDAD'
        },
    'x_neg4': {
        1: 'Definir para quién está creando valor y quienes son sus clientes más importantes y la posibilidad de agrupar estos por medio de sus características, definir como aumentar su satisfacción',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg5': {
        1: 'Definir el valor que quiere entregar a sus clientes, clarificar que problemas o dolores quiere ayudar a resolver, validar  si los productos y/o servicios ofrecidos, realmente solucionan problemas o satisfacen las necesidades de los clientes',
        2: '',
        3: 'Validación de los productos y/o servicios ofrecidos, para lograr asegurar que realmente solucionan problemas o satisfacen las necesidades de los clientes',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg6': {
        1: 'Definir para quién está creando valor y quienes son sus clientes más importantes y la posibilidad de agrupar estos por medio de sus características, definir como aumentar su satisfacción',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg7': {
        1: 'Definir mecanismos de captación de los diferentes clientes potenciales de acuerdo a sus caracteriísticas',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg8': {
        1: 'Definir mecanismos de captación de los diferentes clientes potenciales de acuerdo a sus caracteriísticas',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg9': {
        1: 'Gestionar los recursos requeridos para el perfecto funcionamiento del modelo de negocio y para  el cumplimiento de la propuesta de valor',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg10': {
        1: 'Gestionar los recursos requeridos para el perfecto funcionamiento del modelo de negocio y para  el cumplimiento de la propuesta de valor',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg11': {
        1: 'Gestionar los recursos requeridos para el perfecto funcionamiento del modelo de negocio y para  el cumplimiento de la propuesta de valor',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg12': {
        1: 'Gestionar acuerdos con proveedores',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg13': {
        1: 'Gestionar acuerdos con proveedores',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg14': {
        1: 'Gestionar acuerdos con proveedores',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg15': {
        1: 'Identificar y definir la rentabilidad de cada producto o servicio que ofrece como la utilidad total del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_neg16': {
        1: 'Definir el valor que quiere entregar a sus clientes, clarificar que problemas o dolores quiere ayudar a resolver, validar  si los productos y/o servicios ofrecidos, realmente solucionan problemas o satisfacen las necesidades de los clientes',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MODELO DE NEGOCIO'
        },
    'x_financiero18': {
        1: 'Orientacion al propietario del negocio en los habitos positivos financieros',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero20': {
        1: 'Orientacion al propietario del negocio en los habitos positivos financieros',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero21': {
        1: 'Acompañamiento en el proceso de calculo del punto de equilibrio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero22': {
        1: 'Acompañamiento en la Inclusión financiera para el acceso a los productos financieros del sistema bancario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero22': {
        1: 'Acompañamiento en la Inclusión financiera para el acceso a los productos financieros del sistema bancario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero23': {
        1: 'Acompañamiento en la Inclusión financiera para el acceso a los productos financieros del sistema bancario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero24': {
        1: 'Acompañamiento en la Inclusión financiera para el acceso a los productos financieros del sistema bancario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_financiero25': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: 'Remitir a la Cooperativa Minuto de Dios',
        'area': 'FINANZAS'
        },
    'x_financiero26': {
        1: 'Acompañamiento en la Inclusión financiera para el acceso a los productos financieros del sistema bancario',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FINANZAS'
        },
    'x_mer_com30': {
        1: 'Acompañamiento en el diseño de estrategias para la visibilidad de los productos o servicios',
        2: '',
        3: 'Acompañamiento en el diseño de estrategias para la visibilidad de los productos o servicios',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer_com31': {
        1: 'Acompañamiento en el diseño de estrategias para la visibilidad de los producto o servicios',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer_com38': {
        1: 'Acompañamiento en el uso de redes sociales para promocionar y posicionar su negocio y productos',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_mer_com39': {
        1: 'Acompañamiento en el uso de herramientas digitales para promoción de sus productos (uso de redes sociales o el desarrollo de paginas web)',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'MERCADEO Y COMERCIALIZACION'
        },
    'x_forma44': {
        1: 'Acompañamiento y asesoria en la formalizacion del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_forma45': {
        1: 'Acompañamiento y asesoria en la formalizacion del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_forma46': {
        1: 'Acompañamiento y asesoria en la formalizacion del negocio',
        2: '',
        3: '',
        4: '',
        5: '',
        'area': 'FORMALIZACION'
        },
    'x_in_empleo': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: 'Remitir al programa de Empleabilidad',
        'area': 'FINANZAS'
        },
    'x_fin97n': {
        1: '',
        2: '',
        3: '',
        4: '',
        5: 'Remitir a la Cooperativa Minuto de Dios',
        'area': 'FINANZAS'
        },
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

    mentors = fields.Many2one(
        'res.partner',
        string='Mentores',
        readonly=True
    )

    coordinador = fields.Many2one(
        'res.users',
        string='Coordinador'
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

    # returning an action to go to crm.diagnostic form view related to lead
    def action_crm_diagnostic_view(self):
        for record in self:
            # we avoid to execute the diagnostic whether question modules haven't executed yet
            if (not record.is_cordinator() or not record.is_orientador()) and (not record.first_module_ready or not record.second_module_read or not record.third_module_ready):
                raise ValidationError('Para realizar el diagnostico, debe responder las preguntas de los 3 modulos.')
            crm_diagnostic_vals = record.getting_values_to_crm_diagnostic()
            crm_diagnostic_id = self.env['crm.diagnostic'].create(crm_diagnostic_vals)
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
            
            if 'PROTOCOLOS DE BIOSEGURIDAD' in results:
                area_val = 'bioseguridad'
                dic_vals['crm_diagnostic_line_orientation_ids'] = results.get('PROTOCOLOS DE BIOSEGURIDAD')
                puntaje1 = 0
                count1 = 0
                for record in dic_vals['crm_diagnostic_line_orientation_ids']:
                    for dic in record:
                        if type(dic).__name__ == 'dict':
                            if 'puntaje' in dic.keys():
                                print(dic.get('puntaje'))
                                puntaje1 += int(dic.get('puntaje'))
                                count1 += 1
                                # dic.get('puntaje')
                        elif type(dic).__name__ == 'tuple':
                            if 'puntaje' in dic[2].keys():
                                puntaje1 += int(dic[2].get('puntaje'))
                                count1 += 1
                dic_vals['calificacion'] = puntaje1
                dic_vals['valoracion_bio'] = self._get_valoracion_bio(puntaje1)

            if 'MODELO DE NEGOCIO' in results:
                dic_vals['crm_diagnostic_line_business_model_ids'] = results.get('MODELO DE NEGOCIO')
                puntaje2 = 0
                count2 = 0
                for record in dic_vals['crm_diagnostic_line_business_model_ids']:
                    for dic in record:
                        if type(dic).__name__ == 'dict':
                            if 'puntaje' in dic.keys():
                                print(dic.get('puntaje'))
                                puntaje2 += int(dic.get('puntaje'))
                                count2 += 1
                        elif type(dic).__name__ == 'tuple':
                            if 'puntaje' in dic[2].keys():
                                puntaje2 += int(dic[2].get('puntaje'))
                                count2 += 1
                dic_vals['calificacion2'] = puntaje2

                if puntaje2 in range(0,21):
                    valoracion = 'Incipiente'
                elif puntaje2 in range(20,40):
                    valoracion = 'Confiable'
                elif puntaje2 in range(39,56):
                    valoracion = 'Competente'
                elif puntaje2 >= 56:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_neg'] = valoracion
    
            # elif 'PRODUCCIÓN' in results:
            #     dic_vals['crm_diagnostic_line_production_ids'] = [results.get('PRODUCCIÓN')]
            # elif 'INNOVACIÓN' in results:
            #     dic_vals['crm_diagnostic_line_innovation_ids'] = [results.get('INNOVACIÓN')]
            if 'FORMALIZACION' in results:
                dic_vals['crm_diagnostic_line_formalization_ids'] = results.get('FORMALIZACION')
                _logger.info("$"*500)
                _logger.info(results.get('FORMALIZACION'))
                puntaje3 = 0
                count3 = 0
                for record in dic_vals['crm_diagnostic_line_formalization_ids']:
                    for dic in record:
                        if type(dic).__name__ == 'dict':
                            if 'puntaje' in dic.keys():
                                print(dic.get('puntaje'))
                                puntaje3 += int(dic.get('puntaje'))
                                count3 += 1
                        elif type(dic).__name__ == 'tuple':
                            if 'puntaje' in dic[2].keys():
                                puntaje3 += int(dic[2].get('puntaje'))
                                count3 += 1
                dic_vals['calificacion3'] = puntaje3

                if puntaje3 <= 4.5:
                    valoracion = 'Incipiente'
                elif puntaje3 > 4.6 and puntaje3 <= 9:
                    valoracion = 'Confiable'
                elif puntaje3 > 9 and puntaje3 <= 13:
                    valoracion = 'Competente'
                elif puntaje3 >= 14:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_forma'] = valoracion

            # elif 'ORGANIZACIÓN' in results:
            #     dic_vals['crm_diagnostic_line_organization_ids'] = [results.get('ORGANIZACIÓN')]
            if 'MERCADEO Y COMERCIALIZACION' in results:
                dic_vals['crm_diagnostic_line_marketing_ids'] = results.get('MERCADEO Y COMERCIALIZACION')
                puntaje4 = 0
                count4 = 0
                for record in dic_vals['crm_diagnostic_line_marketing_ids']:
                    for dic in record:
                        if type(dic).__name__ == 'dict':
                            if 'puntaje' in dic.keys():
                                print(dic.get('puntaje'))
                                puntaje4 += int(dic.get('puntaje'))
                                count4 += 1
                                # dic.get('puntaje')
                        elif type(dic).__name__ == 'tuple':
                            if 'puntaje' in dic[2].keys():
                                puntaje4 += int(dic[2].get('puntaje'))
                                count4 += 1
                dic_vals['calificacion4'] = puntaje4

                if puntaje4 in range(0,10):
                    valoracion = 'Incipiente'
                elif puntaje4 in range(10,19):
                    valoracion = 'Confiable'
                elif puntaje4 in range(19,27):
                    valoracion = 'Competente'
                elif puntaje4 >= 27:
                    valoracion = 'Excelencia'
                dic_vals['valoracion_merca'] = valoracion

            if 'FINANZAS' in results:
                dic_vals['crm_diagnostic_line_finance_ids'] = results.get('FINANZAS')
                puntaje5 = 0
                count5 = 0
                for record in dic_vals['crm_diagnostic_line_finance_ids']:
                    for dic in record:
                        count5 += 1
                        if type(dic).__name__ == 'dict':
                            if 'puntaje' in dic.keys():
                                print(dic.get('puntaje'))
                                puntaje5 += int(dic.get('puntaje'))
                                count5 += 1
                                # dic.get('puntaje')
                        elif type(dic).__name__ == 'tuple':
                            if 'puntaje' in dic[2].keys():
                                puntaje5 += int(dic[2].get('puntaje'))
                                count5 += 1
                dic_vals['calificacion5'] = puntaje5

                if puntaje5 in range(0,13):
                    valoracion = 'Incipiente'
                elif puntaje5 in range(13,25):
                    valoracion = 'Confiable'
                elif puntaje5 in range(25,35):
                    valoracion = 'Competente'
                elif puntaje5 >= 35:
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
        lines_dict = {}
        dic_fields = lead.read()[0]
        _fields = self.env['ir.model.fields'].search(
            [('name', 'ilike', 'x_'),
             ('model_id.model', '=', lead._name),
             ('selectable', '=', True),
             ('ttype', '=', 'selection')]).filtered(
                 lambda f : f.name.startswith('x_'))
        puntaje = 0
        for field in _fields:
            tmp_list = []
            field_value = dic_fields.get(field.name)
            # TODO
            # validating if the field value is in ANSWER_VALUES
            # we obtain certain values from lead on its field what is iterating
            if field_value in ANSWER_VALUES:
                answer = dict(lead._fields[field.name].selection).get(getattr(lead, field.name))
                score = ANSWER_VALUES.get(field_value)
                valuation = TEXT_VALUATION.get(score)
                suggestion, area = self.get_sugestion(field.name, score)
                if area in lines_dict:
                    tmp_list = lines_dict.get(area)
                    values = {
                            'name': field.field_description,
                            'respuesta': answer,
                            'puntaje': score,
                            'area': area,
                            'sugerencia': suggestion,
                            'valoracion': valuation,
                            }
                    tmp_list.append((0, 0, values))
                    lines_dict.update({area:tmp_list})

                else:
                    vals = {
                            'name': field.field_description,
                            'respuesta': answer,
                            'puntaje': score,
                            'area': area,
                            'sugerencia': suggestion,
                            'valoracion': valuation,
                            }

                    lines_dict.update({area: [(0,0,vals)] })
            else:
                answer = dict(lead._fields[field.name].selection).get(getattr(lead, field.name))
                score = ANSWER_VALUES.get(field_value)
                valuation = TEXT_VALUATION.get(score)
                suggestion, area = self.get_sugestion(field.name, score)
                if area in lines_dict:
                    tmp_list = list(lines_dict.get(area))
                    values = {
                            'name': field.field_description,
                            'respuesta': answer,
                            'puntaje': score,
                            'area': area,
                            'sugerencia': suggestion,
                            'valoracion': valuation,
                            }
                    tmp_list.append((0, 0, values))
                    lines_dict.update({area:tmp_list})
                else:
                    vals = {
                            'name': field.field_description,
                            'respuesta': answer,
                            'puntaje': score,
                            'area': area,
                            'sugerencia': suggestion,
                            'valoracion': valuation,
                            }

                    lines_dict.update({area:(0, 0, vals)})
            if score:
                puntaje += score
        self.set_diagnostico(puntaje, lead)
        return lines_dict

    # set diagnostico based on range
    @api.model
    def set_diagnostico(self, score, lead):
        if score > 380:
            lead.diagnostico = 'excelencia'
            return
        for k, v in RANGES.items():
            if score in v:
                lead.diagnostico = k

    # this method is called from cron
    def relate_events_to_leads(self):
        event_ids = self.available_events()
        if not event_ids:
            return
        lead_ids = self.search(
            [('mentors', '=', False),
             ('diagnostico', 'in', ('confiable', 'competente', 'excelencia'))])
        if not lead_ids:
            return
        count_max = 0
        last_week = True
        _logger.info("&"*100)
        next_week = True
        user_ids = True

        for lead in lead_ids:

            for event in event_ids.sorted(reverse=True):

                if user_ids == True:
                    user_ids = event.partner_ids
                _logger.info(next_week)
                if last_week and last_week != event.start_datetime.isocalendar()[1]:
                    if next_week == True:
                        next_week = event.start_datetime.isocalendar()[1]
                    if next_week == event.start_datetime.isocalendar()[1] and user_ids == event.partner_ids:
                        last_week = event.start_datetime.isocalendar()[1]
                        event.opportunity_id = lead.id
                        lead.mentors += event.partner_ids[0]
                        self.send_mail_notification(lead)
                        event_ids -= event
                        lead_ids -= lead
                        count_max += 1
                        next_week = (event.start_datetime  + timedelta(weeks=2)).isocalendar()[1]
                if count_max == 1:
                    count_max = 0
                    next_week = False
                    user_ids = True
                    last_week = True
                    break

    # send email notification to coordinador and facilitador
    @api.model
    def send_mail_notification(self, lead_id):
        try:
            template_id = self.env.ref('crm_diagnostic.q_mail_template_event_notification')
            template_id.send_mail(lead_id.id, force_send=True)
        except Exception as e:
            print(e)

    # return events availables
    def available_events(self):
        week_days = range(0, 5)
        date_to_search = fields.Datetime.now().replace(hour=0, minute=0) + timedelta(days=1)
        events = self.env['calendar.event'].search(
            [('start_datetime', '>', date_to_search),
            ('opportunity_id', '=', False)])
        _logger.info(events)
        for event in events:
            if event.start_datetime.weekday() not in week_days:
                events -= event
        _logger.info(events)
        return events

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

    # return the field list to validate the module1
    def fields_module1(self):
        return [
            'x_datos1', 'attach_file', "x_nombre_negocio", "x_nombre", "doctype",
            "x_identification", "x_sexo", "x_edad", "country_id", "state_id", "xcity", "x_dir_res",
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
            # 'x_in_empleo', 'x_forma58_form', 'x_forma61_form', 'x_forma60_form',
            # 'x_forma65_inf', 
            'x_datos3']

    #MODULO 3 BIOSEGURIDAD
    def fields_module3_biosecurity(self):
        return [
            'x_proto1_bio'
        ]

    #MODULO 3 NEGOCIOS
    def fields_module3_business_model(self):
        return [
            'x_neg4', 'x_neg5', 'x_neg6', 'x_neg7', 'x_neg8',
            'x_neg12', 'x_neg13', 'x_neg14', 'x_neg15', 'x_neg16'
        ]

    #Ya no esta en uso
    def fields_module3_production(self):
        return [
        ]

    #Ya No Se Usa
    def fields_module3_innovation(self):
        return [
        ]

    #MODELO 3 FORMALIZACION
    def fields_module3_formalization(self):
        return [
            'x_forma40', 'x_forma41', 'x_forma43', 'x_forma44',
            'x_forma45', 'x_forma46', 'x_forma47', 'x_forma48', 'x_forma49',
            'x_forma50', 'x_forma51', 'x_forma52'
        ]

    #Ya No Se Usa
    def fields_module3_organization(self):
        return [
            # 'x_org61', 'x_org62', 'x_org63', 'x_org64', 'x_org65', 'x_org66',
            # 'x_org67', 'x_org68'
        ]
    #MODELO 3 MERCADEO
    def fields_module3_marketing(self):
        return [
            'x_mer_com30', 'x_mer_com31', 'x_mer_com32', 'x_mer_com33', 'x_mer_com34',
            'x_mer_com35', 'x_mer_com36', 'x_mer_com37', 'x_mer_com38', 'x_mer_com39',
        ]

    #MODELO 3 FINANCIERO
    def fields_module3_financial(self):
        return [
            'x_financiero18', 'x_financiero19', 'x_financiero20', 'x_financiero21',
            'x_financiero22', 'x_financiero23', 'x_financiero24', 'x_financiero25',
            'x_financiero26', 'x_financiero27', 'x_financiero28', 'x_financiero29',
        ]

    def full_list_field(self):
        full_fields = []
        full_fields.extend(self.fields_module3_generalities())
        full_fields.extend(self.fields_module3_biosecurity())
        full_fields.extend(self.fields_module3_business_model())
        # full_fields.extend(self.fields_module3_production())
        # full_fields.extend(self.fields_module3_innovation())
        full_fields.extend(self.fields_module3_formalization())
        # full_fields.extend(self.fields_module3_organization())
        # full_fields.extend(self.fields_module3_marketing())
        full_fields.extend(self.fields_module3_financial())
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

    # validating if the current user has the cordinator profile
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
            if lead.is_facilitator():
                if lead.all_fields_module1_are_ok():
                    lead.first_module_ready = True
                else:
                    lead.first_module_ready = False
            elif lead.is_cordinator() or lead.is_orientador():
                lead.first_module_ready = True
            else:
                lead.first_module_ready = False

    # computed if the module2 is ok
    @api.depends(fields_module2)
    def compute_second_module(self):
        for lead in self:
            if lead.is_facilitator() and lead.first_module_ready:
                if lead.all_fields_module2_are_ok():
                    lead.second_module_read = True
                else:
                    lead.second_module_read = False
            elif lead.is_cordinator() or lead.is_orientador():
                lead.second_module_read = True
            else:
                lead.second_module_read = False

    # computed if the module3 is ok
    @api.depends(full_list_field)
    def compute_third_module(self):
        for lead in self:
            if lead.is_facilitator() and lead.second_module_read:
                if lead.all_fields_module3_are_ok():
                    lead.third_module_ready = True
                else:
                    lead.third_module_ready = False
            elif lead.is_cordinator() or lead.is_orientador():
                lead.third_module_ready = True
            else:
                lead.third_module_ready = False

    # validating it all fields of module3 were filled
    def all_fields_module3_are_ok(self):
        result = []
        # fields = self.fields_module3()
        # result.append(self.check_generalities_fields(self.fields_module3_generalities()))
        result.append(self.check_biosecurity_fields(self.fields_module3_biosecurity()))
        result.append(self.check_business_model_fields(self.fields_module3_business_model()))
        # result.append(self.check_production_fields(self.fields_module3_production()))
        # result.append(self.check_innovation_fields(self.fields_module3_innovation()))
        result.append(self.check_formalization_fields(self.fields_module3_formalization()))
        # result.append(self.check_organization_fields(self.fields_module3_organization()))
        result.append(self.check_marketing_fields(self.fields_module3_marketing()))
        result.append(self.check_financial_fields(self.fields_module3_financial()))
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

    # checking if all biosecurity field section are ok
    def check_biosecurity_fields(self, fields):
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

    # checking if all production field section are ok
    def check_production_fields(self, fields):
        if any(not getattr(self, field) for field in fields):
            return False
        else:
            return True

    # checking if all innovation field section are ok
    def check_innovation_fields(self, fields):
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

    # checking if all organization field section are ok
    def check_organization_fields(self, fields):
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

    # checking if all financial field section are ok
    def check_financial_fields(self, fields):
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
                self.stage_id = second_stage if second_stage else self.stage_id
            if self.first_module_ready and self.second_module_read:
                third_stage =  self.get_stage('tercer_encuentro')
                self.stage_id = third_stage if third_stage else self.stage_id
            if self.first_module_ready and self.second_module_read and self.third_module_ready:
                fourth_stage =  self.get_stage('espera_de_plan')
                self.stage_id = fourth_stage if fourth_stage else self.stage_id

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

                res['arch'] = etree.tostring(doc)
            if self.is_facilitator():
                for node in doc.xpath("//header/field[@name='stage_id']"):
                    if 'options' in node.attrib:
                        node.attrib.pop('options')

                res['arch'] = etree.tostring(doc)

                for node in doc.xpath("//field[@name='mentors']"):
                    if not 'options' in node.attrib:
                        options = json.loads(node.attrib['options'])
                        options['no_create'] = False
                        options['no_open'] = False
                        node.attrib['options'] = json.dumps(options)

                res['arch'] = etree.tostring(doc)

        return res

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
