from app import create_app
from app.config import Config

app = create_app(Config)


def init_db():
    from app.models import db
    db.create_all(app=create_app(Config))


if __name__ == '__main__':
    init_db()
    app.run()
