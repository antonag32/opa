from odoo import _, fields, models


class Course(models.Model):
    _name = "course"
    _description = "Open Academy course"
    _rec_name = "title"

    title = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(comodel_name="res.users")
    session_ids = fields.One2many(
        string="Sessions", comodel_name="session", inverse_name="course_id"
    )

    _sql_constraints = [
        ("unique_course_title", "UNIQUE(title)", "Courses must have unique titles"),
        (
            "dif_course_title_descript",
            "CHECK(title != description)",
            "Course titles and description must be different",
        ),
    ]

    def copy(self, default=None):
        return super().copy(
            default=dict(default or {}, title=_("%s (copy)", self.title))
        )
