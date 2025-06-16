from flask import Flask, render_template

app = Flask(__name__)

jobs = [
    {
        'id': 1,
        'title': 'Software Engineer',
        'location': 'Cairo',
        'company': 'Tech Company'
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'Alexandria',
        'company': 'Data Corp'
    },
    {
        'id': 3,
        'title': 'Web Developer',
        'location': 'Zagazig',
        'company': 'Web Solutions'
    },
    {
        'id': 4,
        'title': 'Mobile Developer',
        'location': 'Cairo',
        'company': 'App Innovations'
    },
    {
        'id': 5,
        'title': 'DevOps Engineer',
        'location': 'Giza',
        'company': 'Cloud Services'
    }
]

companies = [
    {'id': 1, 'name': 'Tech Company', 'location': 'Cairo', 'industry': 'Software', 'employees': 120},
    {'id': 2, 'name': 'Data Corp', 'location': 'Alexandria', 'industry': 'Analytics', 'employees': 90},
    {'id': 3, 'name': 'Web Solutions', 'location': 'Zagazig', 'industry': 'Web Development', 'employees': 60},
    {'id': 4, 'name': 'App Innovations', 'location': 'Cairo', 'industry': 'Mobile Apps', 'employees': 75},
    {'id': 5, 'name': 'Cloud Services', 'location': 'Giza', 'industry': 'Cloud Computing', 'employees': 110}
]

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