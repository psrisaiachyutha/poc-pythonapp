from marshmallow import Schema, fields


class CreatePersonRequestSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    #created_at = fields.DateTime()
