from odoo import fields, models


class Course(models.Model):
    _name = 'course'
    _description = 'Open Academy course'
    _rec_name = 'title'

    title = fields.Char(required=True)
    description = fields.Text()
