from psycopg2.errors import CheckViolation, NotNullViolation, UniqueViolation

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase
from odoo.tools import mute_logger


class TestOpa(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.course = cls.env.ref("opa.course_3_demo")
        cls.session_instructor_id = cls.env.ref("opa.res_partner_1_demo").id

    def test_session_instructor_not_attendee(self):
        """Validate that a session's instructor can't be in the attendees list."""
        with self.assertRaisesRegex(ValidationError, "The instructor can't be an attendee"):
            self.env["session"].create(
                {
                    "title": "Instructor teaches itself",
                    "course_id": self.course.id,
                    "starts_on": fields.Date.today(),
                    "instructor_id": self.session_instructor_id,
                    "attendee_ids": [fields.Command.set([self.session_instructor_id])],
                }
            )

        test_session = self.env["session"].create(
            {
                "title": "Sneaky Instructor",
                "course_id": self.course.id,
                "starts_on": fields.Date.today(),
                "instructor_id": self.session_instructor_id,
            }
        )
        with self.assertRaisesRegex(ValidationError, "The instructor can't be an attendee"):
            test_session.write({"attendee_ids": [fields.Command.set([self.session_instructor_id])]})

        test_session = self.env["session"].create(
            {
                "title": "Sneaky Attendee",
                "course_id": self.course.id,
                "starts_on": fields.Date.today(),
                "attendee_ids": [fields.Command.set([self.session_instructor_id])],
            }
        )
        with self.assertRaisesRegex(ValidationError, "The instructor can't be an attendee"):
            test_session.write({"instructor_id": self.session_instructor_id})

    def test_session_required_course(self):
        """Ensure a course is required when creating a session."""
        with mute_logger("odoo.sql_db"):
            with self.assertRaisesRegex(NotNullViolation, 'null value in column "course_id"'):
                self.env["session"].create(
                    {
                        "title": "Incorrectly creating sessions",
                        "starts_on": fields.Date.today(),
                    }
                )

    def test_course_same_title_description(self):
        """Validate that courses can't have their description be the same as their title."""
        test_string = "This is about to blow up!"
        with mute_logger("odoo.sql_db"):
            with self.assertRaisesRegex(CheckViolation, "course_dif_course_title_descript"):
                self.env["course"].create({"title": test_string, "description": test_string})

    def test_course_repeated_title(self):
        """Ensure courses must have unique titles."""
        with mute_logger("odoo.sql_db"):
            with self.assertRaisesRegex(UniqueViolation, "course_unique_course_title"):
                self.env["course"].create(
                    {
                        "title": self.course.title,
                        "description": "I don't want to be unique!",
                    }
                )

    def test_course_duplication(self):
        """Validate that courses can be duplicated."""
        course_2 = self.course.copy()
        self.assertEqual(course_2.description, self.course.description)
        self.assertEqual(course_2.responsible_id, self.course.responsible_id)
        self.assertNotEqual(course_2.title, self.course.title)
