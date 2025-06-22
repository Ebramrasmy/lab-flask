from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'super_secret_key_iti'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    employees = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Company {self.name}>"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='jobs')

    def __repr__(self):
        return f"<Job {self.title}>"



@app.route('/', methods = ['GET'])
def list_jobs():
    return render_template('jobs.html', jobs = jobs)


@app.route('/job/<int:job_id>', methods = ['GET'])
def job_details(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if not job:
        return "Job not found", 404
    return render_template('job_detail.html', job=job)

@app.route('/companies', methods = ['GET'])
def list_companes():
        return render_template("companies.html", companies=companies)

@app.route('/company/<int:id>', methods = ['GET'])
def company_detail(id):
    company = next((c for c in companies if c['id'] == id), None)
    if company:
        return render_template('company_detail.html', company=company)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)