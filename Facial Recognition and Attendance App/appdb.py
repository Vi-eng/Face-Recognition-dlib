from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from image_rec import database
import urllib

app = Flask(__name__)

"""
# Configure the SQLAlchemy connection string
params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-BJNEMLC;DATABASE=Flask_FaRec;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://<username>:<password>@<dsn>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""

db = database(app)


# Define a simple model (replace this with your actual database model)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    try:
        """
        # Create a sample user and add it to the database
        new_user = User(username='john_doe')
        db.session.add(new_user)
        db.session.commit()
        """
        # Query the database to retrieve the user
        user = User.query.first()

        return render_template('indexdb.html', username=user.username)

    except Exception as e:
        # Handle exceptions gracefully
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
