# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError

class ResUser(models.Model):
    _inherit = 'res.users'

    def create(self, values):
        email = values['email']
        if email: #verifica si se tiene un email
            separator_position = email.find('@')
            domain = email[separator_position+1:] #se obtiene el dominio con el substring mediante el separator '@'
            if domain == 'uniminuto.edu.co': #Si el dominio del email es 'uniminuto.edu.co'
                default_role_id = self.env['res.company'].search([('id', '=', values['company_id'])]).role_id.id #se obtiene el rol asignado por defecto para nuevos usuarios
                if 'role_line_ids' in values: #si existen roles agregados de forma manual al momento de crear el usuario
                    role_line_ids = values['role_line_ids'] #se obtienen los roles asignados
                    role_deault_in_role_line_ids = 0
                    for role_line_id in role_line_ids: #se itera sobre los roles asignados
                        if role_line_id[2]['role_id'] == default_role_id: #si el id del rol actual del bucle es igual al id del rol por defecto en la configuración...
                            role_deault_in_role_line_ids = 1 #Se cambia el valor a la variable que verifica si los id de los roles de setings y del bucle son iguales a 1
                            break; #Se finaliza el bucle sin realizar ninguna acción
                    if role_deault_in_role_line_ids == 0: #Si NO se encontró el id del rol por defecto dentro de los roles asignados al crear el usuario...
                        role_line_ids.append((0, 0,{'company_id' : values['company_id'], 'role_id' : default_role_id})) #Se agrega el rol por defacto a la lista de roles
                else : #Si no existen roles agregados de forma manual al momento de crear el usuario...
                    values['role_line_ids'] = [(0, 0,{'company_id' : values['company_id'], 'role_id' : default_role_id})] #Se agrega el key 'role_lines_id' y se pasa el rol por defecto de la condiguracion
        return super(ResUser, self).create(values)