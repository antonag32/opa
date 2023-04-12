from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean()
    session_ids = fields.Many2many(
        string="Sessions",
        comodel_name="session",
        relation="session_res_partner_rel",
        column1="res_partner_id",
        column2="session_id",
    )
