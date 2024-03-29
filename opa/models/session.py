from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = "session"
    _description = "Session from an Open Academy course"
    _rec_name = "title"

    title = fields.Char(required=True)
    starts_on = fields.Date(required=True)
    ends_on = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(string="Duration (hours)")
    seats = fields.Integer()
    course_id = fields.Many2one(comodel_name="course", required=True)
    instructor_id = fields.Many2one(
        comodel_name="res.partner",
        domain=[
            "|",
            ("instructor", "=", True),
            ("category_id.parent_id.name", "=", "Teacher"),
        ],
    )
    attendee_ids = fields.Many2many(
        string="Attendees",
        comodel_name="res.partner",
        relation="session_res_partner_rel",
        column1="session_id",
        column2="res_partner_id",
    )
    attendee_count = fields.Integer(compute="_compute_attendee_count", store=True)
    taken_seats = fields.Float(string="Taken Seats (%)", compute="_compute_taken_seats")
    active = fields.Boolean(default=True)

    @api.depends("attendee_ids")
    def _compute_attendee_count(self):
        for record in self:
            record.attendee_count = len(record.attendee_ids)

    @api.depends("attendee_ids", "seats")
    def _compute_taken_seats(self):
        for record in self:
            if record.seats > 0:
                record.taken_seats = round((100 / record.seats) * len(record.attendee_ids), 2)
            else:
                record.taken_seats = 0

    @api.onchange("seats")
    def _onchange_seats(self):
        if self.seats < 0:
            return {
                "warning": {
                    "title": _("Invalid number of seats"),
                    "message": _("Negative seats don't exist!"),
                }
            }

    @api.onchange("attendee_ids", "seats")
    def _onchange_attendee_ids(self):
        if len(self.attendee_ids) > self.seats:
            return {
                "warning": {
                    "title": _("Not enough seats!"),
                    "message": _(
                        "You can't have more attendees (%d) than seats (%d).", (len(self.attendee_ids), self.seats)
                    ),
                }
            }

    @api.constrains("attendee_ids", "instructor_id")
    def _check_instructor_id(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise ValidationError(_("The instructor can't be an attendee"))
