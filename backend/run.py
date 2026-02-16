from app import create_app
from app.extensions import db
from app.models.template import Template

app = create_app()


@app.cli.command("seed_templates")
def seed_templates():
    templates = [
        {
            "name": "ieee",
            "type": "ieee",
            "style_jsonb": {"fontFamily": "Source Serif 4", "fontSize": 11},
            "cover_jsonb": {"titleAlign": "center"},
            "is_system": True,
        },
        {
            "name": "college",
            "type": "college",
            "style_jsonb": {"fontFamily": "Times New Roman", "fontSize": 12},
            "cover_jsonb": {"titleAlign": "center"},
            "is_system": True,
        },
    ]

    for item in templates:
        if not Template.query.filter_by(name=item["name"]).first():
            db.session.add(Template(**item))
    db.session.commit()
    print("Templates seeded")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
