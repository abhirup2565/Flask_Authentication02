from marshmallow import fields,Schema

class TokenBlockListSchema(Schema):
    id = fields.String()
    jti = fields.String()
    created_at = fields.DateTime()