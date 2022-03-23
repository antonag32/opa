from odoo import fields, models


class Session(models.Model):
    _name = 'session'
    _description = 'Session from an Open Academy course'
    _rec_name = 'title'

    title = fields.Char(required=True)
    starts_on = fields.Date(required=True)
    duration = fields.Float(string='Duration (hours)')
    seats = fields.Integer()
    course_id = fields.Many2one(comodel_name='course', required=True)
    instructor_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[
            '|',
            ('instructor', '=', True),
            ('category_id.parent_id.name', '=', 'Teacher')
        ]
    )
    attendee_ids = fields.Many2many(
        string='Attendees',
        comodel_name='res.partner',
        relation='session_res_partner_rel',
        column1='session_id',
        column2='res_partner_id'
    )
