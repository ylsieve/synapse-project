from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# 1. Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///synapse_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. The Data Model
class ResearchEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.Integer, nullable=False)
    usage = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    total_count = ResearchEntry.query.count()
    return render_template('index.html', count=total_count)

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/research', methods=['GET', 'POST'])
def research():
    if request.method == 'POST':
        mood_score = request.form.get('mood_score')
        usage_time = request.form.get('usage_time')
        new_entry = ResearchEntry(mood=int(mood_score), usage=usage_time)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('thank_you', score=mood_score))
    return render_template('research.html')

@app.route('/thank_you/<score>')
def thank_you(score):
    return render_template('thank_you.html', score=score)

@app.route('/about')
def about():
    return render_template('about.html')

# SECRET ROUTE: Only you know this URL exists!
@app.route('/admin_dashboard_99') 
def results():
    entries = ResearchEntry.query.all()
    if not entries:
        return "<h1>No data yet!</h1>"
    
    total_mood = sum([e.mood for e in entries])
    avg_mood = round(total_mood / len(entries), 1)
    
    return render_template('results.html', entries=entries, avg_mood=avg_mood)

if __name__ == '__main__':
    app.run(debug=True)