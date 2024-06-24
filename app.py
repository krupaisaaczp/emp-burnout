from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('burnout.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS survey (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 workload INTEGER,
                 job_satisfaction INTEGER,
                 stress_levels INTEGER,
                 work_life_balance INTEGER,
                 comments TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        workload = request.form['workload']
        job_satisfaction = request.form['job_satisfaction']
        stress_levels = request.form['stress_levels']
        work_life_balance = request.form['work_life_balance']
        comments = request.form['comments']
        
        conn = sqlite3.connect('burnout.db')
        c = conn.cursor()
        c.execute('''INSERT INTO survey (workload, job_satisfaction, stress_levels, work_life_balance, comments)
                     VALUES (?, ?, ?, ?, ?)''', (workload, job_satisfaction, stress_levels, work_life_balance, comments))
        conn.commit()
        conn.close()
        
        return redirect(url_for('results'))
    return render_template('survey.html')

@app.route('/results')
def results():
    conn = sqlite3.connect('burnout.db')
    c = conn.cursor()
    c.execute('SELECT * FROM survey')
    survey_data = c.fetchall()
    conn.close()
    return render_template('results.html', survey_data=survey_data)

if __name__ == '__main__':
    app.run(debug=True)
