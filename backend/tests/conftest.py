import pytest

from app import create_app
from app.extensions import db
from app.models.user import User


@pytest.fixture()
def app_instance():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )

    with app.app_context():
        db.create_all()
        user = User(name="Tester", email="student@blackbook.local", role="student")
        user.set_password("blackbook123")
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app_instance):
    return app_instance.test_client()
