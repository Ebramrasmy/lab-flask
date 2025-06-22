from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField ,SelectField
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

class CompanyCreationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    industry = StringField("Industry", validators=[DataRequired()])
    employees = IntegerField("Employees Count", validators=[DataRequired()])
    submit = SubmitField("Create Company")

class JobCreationForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    company_id = SelectField("Company", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Create Job")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/companies')
def list_companes():
    companies = Company.query.all()
    return render_template("companies.html", companies=companies)

@app.route('/company/<int:id>')
def company_detail(id):
    company = Company.query.get_or_404(id)
    return render_template('company_detail.html', company=company)

@app.route('/companies/create', methods=['GET', 'POST'])
def create_company():
    form = CompanyCreationForm()
    if form.validate_on_submit():
        new_company = Company(
            name=form.name.data,
            location=form.location.data,
            industry=form.industry.data,
            employees=form.employees.data
        )
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('list_companes'))
    return render_template('create_company.html', form=form)

@app.route('/jobs')
def list_jobs():
    jobs = Job.query.all()
    return render_template("jobs.html", jobs=jobs)

@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    form = JobCreationForm()
    companies = Company.query.all()
    form.company_id.choices = [(company.id, company.name) for company in companies]

    if form.validate_on_submit():
        new_job = Job(
            title=form.title.data,
            location=form.location.data,
            company_id=form.company_id.data
        )
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('list_jobs'))
    return render_template('create_job.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
