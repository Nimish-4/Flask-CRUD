from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re

class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    @validates_schema
    def validate_password(self, data, **kwargs):
        if not re.findall(r'\d',data['password']):
            raise ValidationError("Password must contain atleast 1 digit!")