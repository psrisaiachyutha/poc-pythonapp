from marshmallow import Schema, fields


class PersonSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()
