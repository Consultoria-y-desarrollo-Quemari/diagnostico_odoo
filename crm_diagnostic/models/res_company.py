from odoo import _, api, fields, models, tools
 
class ResCompany(models.Model):
    _inherit = "res.company"

    fechalimite = fields.Date("Fecha limite del periodo semestral")
    fechalimite4 = fields.Date("Fecha limite del periodo cuatrimestral")