from odoo import api, fields, models


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
    taken_seats = fields.Float(string='Taken Seats (%)', compute='_compute_taken_seats')
    active = fields.Boolean(default=True)

    @api.depends('attendee_ids', 'seats')
    def _compute_taken_seats(self):
        for record in self:
            if record.seats > 0:
                record.taken_seats = round((100 / record.seats) * len(record.attendee_ids), 2)
            else:
                record.taken_seats = 0
