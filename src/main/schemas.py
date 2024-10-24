# src/main/schemas.py

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Email(required=True)

class HealthDataSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    heart_rate = fields.Int(required=True)
    blood_pressure = fields.Str(required=True)
    temperature = fields.Float(required=True)
