from marshmallow import Schema, fields


class ProjectCreateSchema(Schema):
    title = fields.Str(required=True)
    guide_name = fields.Str(required=False, allow_none=True)
    template = fields.Str(required=False)


class ProjectPatchSchema(Schema):
    title = fields.Str(required=False)
    guide_name = fields.Str(required=False)
    status = fields.Str(required=False)
    document = fields.Dict(required=False)
