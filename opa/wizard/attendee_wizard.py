from odoo import fields, models


class AttendeeWizard(models.TransientModel):
    _name = 'attendee.wizard'
    _description = 'Attendee Wizard for Open Academy sessions'

    session_ids = fields.Many2many(
        string='Sessions',
        comodel_name='session',
        default=lambda s: s.env['session'].browse(s._context.get('active_ids')),
        required=True
    )
    attendee_ids = fields.Many2many(string='Attendees', comodel_name='res.partner', required=True)

    def add_attendees(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
