import os
from flask import Flask

from dotenv import load_dotenv
load_dotenv()

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.twitter_routes import twitter_routes
from web_app.routes.stats_routes import stats_routes


DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = "temporary secret value. todo read from env var and customize on production to keep sessions secure"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(home_routes)
    app.register_blueprint(twitter_routes)
    app.register_blueprint(stats_routes)
    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
