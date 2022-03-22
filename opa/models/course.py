from odoo import fields, models


class Course(models.Model):
    _name = 'course'
    _description = 'Open Academy course'
    _rec_name = 'title'

    title = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(comodel_name='res.users')
    session_ids = fields.One2many(string='Sessions', comodel_name='session', inverse_name='course_id')
