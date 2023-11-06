import datetime as dt


class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<Person(name={self.name!r})>".format(self=self)
