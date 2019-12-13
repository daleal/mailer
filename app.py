import os
from logging.config import dictConfig
from flask import Flask, request
from flask_mail import Mail, Message


# Logs configuration
dictConfig({
    "version": 1,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
        },
        "file": {
            "format": ("[%(asctime)s] [%(levelname)s] %(pathname)s - "
                       "line %(lineno)d: \n%(message)s\n")
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "console"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.getenv("LOGS_FILE", default="mailer.log"),
            "formatter": "file"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
})


app = Flask(__name__)


app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,  # 587 => TSL, 465 => SSL
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME")
)


mailer = Mail(app)


@app.route("/")
def index():
    return "https://www.github.com/daleal/mailer"


@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json(force=True)
        key = data["key"]

        if os.getenv("KEY") != key:
            app.logger.info(f"Invalid key {key} for sending mail")
            return jsonify({
                "success": False,
                "message": "Invalid key"
            }), 401

        if set(["email", "title", "body"]) != set(data.keys()):
            app.logger.info(f"Invalid request body keys {data.keys()}")
            return jsonify({
                "success": False,
                "message": "Invalid request body"
            }), 400

        message = Message(data["title"], recipients=[data["email"]])
        message.html = data["body"]

        app.logger.info(f"Sending mail to {data['email']}")
        mailer.send(message)
        app.logger.info(f"Mail sent to {data['email']}")

        return jsonify({"success": True}), 200

    except Exception as err:
        app.logger.error(err)
        return jsonify({"success": False}), 500
