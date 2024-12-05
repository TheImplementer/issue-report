from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    """Initialize the database."""
    with sqlite3.connect("issues.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                description TEXT NOT NULL,
                duration TEXT NOT NULL,
                issue_date TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def submit_issue():
    if request.method == 'POST':
        username = request.form['username']
        description = request.form['description']
        duration = request.form['duration']
        issue_date = request.form['issue_date']

        # Save to database
        with sqlite3.connect("issues.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO issues (username, description, duration, issue_date) VALUES (?, ?, ?, ?)",
                           (username, description, duration, issue_date))
            conn.commit()

        return redirect(url_for('view_issues'))

    return render_template('form.html')

@app.route('/issues', methods=['GET'])
def view_issues():
    with sqlite3.connect("issues.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, description, duration, issue_date FROM issues")
        issues = cursor.fetchall()

    return render_template('issues.html', issues=issues)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)