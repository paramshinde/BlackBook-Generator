from marshmallow import Schema, fields, validate


class SectionSchema(Schema):
    id = fields.Str(required=True)
    heading = fields.Str(required=True)
    content = fields.Str(required=True)
    order = fields.Int(required=True)


class DiagramSchema(Schema):
    diagram_type = fields.Str(required=True)
    mermaid_code = fields.Str(required=True)


class CodeFileSchema(Schema):
    filename = fields.Str(required=True)
    language = fields.Str(required=True)
    content_text = fields.Str(required=True)


class FigureSchema(Schema):
    fileUrl = fields.Str(required=False, allow_none=True)
    caption = fields.Str(required=False, allow_none=True)


class TemplateSettingsSchema(Schema):
    template = fields.Str(required=True, validate=validate.OneOf(["ieee", "college", "custom"]))
    darkPreview = fields.Bool(required=True)
    margins = fields.Dict(required=False)
    fontFamily = fields.Str(required=False)
    fontSize = fields.Int(required=False)


class DocumentSchema(Schema):
    meta = fields.Dict(required=True)
    sections = fields.List(fields.Nested(SectionSchema), required=True)
    diagrams = fields.List(fields.Nested(DiagramSchema), required=True)
    codeBlocks = fields.List(fields.Nested(CodeFileSchema), required=True)
    figures = fields.List(fields.Nested(FigureSchema), required=True)
    toc = fields.List(fields.Dict(), required=True)
    templateSettings = fields.Nested(TemplateSettingsSchema, required=True)
