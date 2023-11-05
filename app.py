from flask import Flask, render_template, request
from pymongo import MongoClient

from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

print("test")


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        entries = []
        print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.strptime(
                datetime.today().strftime("%Y.%m.%d"), "%Y.%m.%d"
            ).strftime("%b %d")
            app.db.entries.insert_one(
                {"content": entry_content, "date": formatted_date}
            )
        entries = [e for e in app.db.entries.find({})]
        return render_template("home.html", entries=entries)

    return app


# @app.route("/fancy")
# def fancy():
#     return """
#     <html>
#     <body>
#     <h1>Greetings!</h1>
#     <p>Hello, World from Flask!</p>
#     </body>
#     </html>
#     """
