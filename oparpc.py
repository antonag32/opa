#!/usr/bin/env python3

import logging
import sys
from getpass import getpass
from xmlrpc import client

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_logger = logging.getLogger()


class OpaRpc:
    def __init__(self, database, user, password, target="http://localhost:8069"):
        self.uid = None
        self.target = target
        self.database = database
        self.user = user
        self.password = password
        self.common = client.ServerProxy(f"{target}/xmlrpc/2/common")
        self.object = client.ServerProxy(f"{target}/xmlrpc/2/object")

    def server_info(self):
        return self.common.version()

    def login(self):
        self.uid = self.common.authenticate(self.database, self.user, self.password, {})
        return isinstance(self.uid, int)

    def _execute(self, *args):
        return self.object.execute_kw(self.database, self.uid, self.password, *args)

    def get_sessions(self):
        return self._execute(
            "session", "search_read", [[]], {"fields": ["id", "title", "seats"]}
        )

    def get_courses(self):
        return self._execute("course", "search_read", [[]], {"fields": ["id", "title"]})

    def add_session(self, title, course_id, start):
        return self._execute(
            "session",
            "create",
            [{"title": title, "course_id": course_id, "starts_on": start}],
        )


def main():
    _logger.info("Starting OPA-RPC v1.0")
    target = input(" - Server's address. Empty for default (localhost:8069): ")
    target = target.strip()
    database = input(" - Database: ")
    user = input(" - Username: ")
    password = getpass(" - Password: ")
    if target:
        opa_client = OpaRpc(database, user, password, target)
    else:
        opa_client = OpaRpc(database, user, password)

    _logger.info("Gathering server's info...")
    _logger.info(opa_client.server_info())

    _logger.info("Attempting login...")
    if opa_client.login():
        _logger.info("Successful login")
    else:
        _logger.error("Error authenticating. Exiting now")
        sys.exit(1)

    while True:
        command = input("$> ").strip()
        if command == "sessions":
            for session in opa_client.get_sessions():
                _logger.info(session)
        elif command == "courses":
            for course in opa_client.get_courses():
                _logger.info(course)
        elif command == "add":
            title = input(" - Title: ")
            course_id = int(input(" - Course ID: "))
            date = input(" - Start date (YYYY-mm-dd): ")
            _logger.info(
                "Course created with ID of %d",
                opa_client.add_session(title, course_id, date),
            )
        elif command == "exit":
            sys.exit(0)


if __name__ == "__main__":
    main()
