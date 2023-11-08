from marshmallow import Schema, fields, validates, ValidationError


class GenerateReportRequestValidator(Schema):
    competitor = fields.List(fields.String(), required=True)
    location = fields.List(fields.String(), required=True)
    demographic = fields.List(fields.String(), required=True)
    brand = fields.String(required=True)
    duration = fields.String(required=True)

    @validates("location")
    def validate_location_list(self, value):
        self._helper_list_validator(value, 'location')

    @validates("demographic")
    def validate_demographic_list(self, value):
        self._helper_list_validator(value, 'demographic')

    @validates("competitor")
    def validate_competitor_list(self, value):
        self._helper_list_validator(value, 'competitor')

    @staticmethod
    def _helper_list_validator(value, field_name):
        if not all(value):
            raise ValidationError("All elements in '{field_name}' must be non-empty".format(field_name=field_name))
        if len(value) == 0:
            raise ValidationError("{field_name} list must not be empty".format(field_name=field_name))

