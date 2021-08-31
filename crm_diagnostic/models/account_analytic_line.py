# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from lxml import etree
# from datetime import datetime
# from datetime import date
import json
import logging


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    stage_state =  fields.Selection(
        string='Estado de la Mentoria',
        selection=[('en_espera', 'En Espera'),
                   ('en_proceso', 'En Proceso'),
                   ('finalizado', 'Finalizado')],
    )

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


    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False,submenu=False):
        res = super(AccountAnalyticLine, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
        if view_type == 'tree':
            doc = etree.XML(res['arch'])
            if self.is_mentor():
                for node in doc.xpath("//field[@name='stage_state']"):

                    if 'modifiers' in node.attrib:
                        modifiers = json.loads(node.attrib['modifiers'])
                        modifiers['readonly'] = False
                        node.attrib['modifiers'] = json.dumps(modifiers)
                res['arch'] = etree.tostring(doc)
            else:
                for node in doc.xpath("//field[@name='stage_state']"):
                    if 'modifiers' in node.attrib:
                        modifiers = json.loads(node.attrib['modifiers'])
                        modifiers['readonly'] = True
                        node.attrib['modifiers'] = json.dumps(modifiers)
                res['arch'] = etree.tostring(doc)

        elif view_type == 'form':
            doc = etree.XML(res['arch'])
            if self.is_mentor():
                for node in doc.xpath("//field[@name='stage_state']"):
                    if 'modifiers' in node.attrib:
                        modifiers = json.loads(node.attrib['modifiers'])
                        modifiers['readonly'] = False
                        node.attrib['modifiers'] = json.dumps(modifiers)
                res['arch'] = etree.tostring(doc)
            else:
                for node in doc.xpath("//field[@name='stage_state']"):
                    if 'modifiers' in node.attrib:
                        modifiers = json.loads(node.attrib['modifiers'])
                        modifiers['readonly'] = True
                        node.attrib['modifiers'] = json.dumps(modifiers)
                res['arch'] = etree.tostring(doc)

        return res

    def validate_parte_horas(self, data, context):
        parte_horas = self.env['account.analytic.line'].search([])
        if context.get('active_ids'):
            for record in parte_horas.filtered(lambda rec: rec.task_id.lead_id.id == context.get('active_ids')[0]):
                if record.stage_state != 'finalizado':
                    raise ValidationError(
                        _(
                            "No se puede crear un registro nuevo. "
                            "Debe terminar antes la mentoria pendiente."
                        )
                    )
        else:
            for record in parte_horas.filtered(lambda rec: rec.task_id.id == data.get('task_id') and rec.task_id.project_id.id == data.get('project_id')):
                if record.stage_state != 'finalizado':
                    raise ValidationError(
                        _(
                            "No se puede crear un registro nuevo. "
                            "Debe terminar antes la mentoria pendiente."
                        )
                    )

        return True

    @api.model
    def create(self, values):
        
        context = self._context
        self.validate_parte_horas(values, context)
        result = super(AccountAnalyticLine, self).create(values)
        
        if result:
            self.create_event(result)

        return result


    def create_event(self, data):
        import datetime
        from datetime import date
        event = self.env['calendar.event']
        start_date = data.create_date + datetime.timedelta(days=1)
        values = {
                'name': data.name,
                'duration': data.unit_amount,
                # 'user_id': product_line.get('qty'),
                'opportunity_id': data.task_id.lead_id.id,
                'start': start_date,
                'stop': start_date + datetime.timedelta(hours=data.unit_amount)
            }
        event.create(values)
