# Football-Forum
A Flask web app where football fans can post, comment, and upvote in team-specific subforums — kind of like Reddit, but just for football.

##  Features

- User accounts (register, login, logout)
- Subforums for teams (e.g. Bayern, Dortmund)
- Create posts & comments
- Upvote posts and comments

## Setup

```bash
git clone https://github.com/yourusername/football-forum.git
cd football-forum
python3 -m venv venv
source venv/bin/activate         
pip install -r requirements.txt
export FLASK_APP=run.py         
flask db init
flask db migrate -m "init"
flask db upgrade
flask run
```
To add teams manually:
from app import create_app, db
from app.models import Team

app = create_app()
with app.app_context():
    db.session.add(Team(name="Bayern Munich"))
    db.session.add(Team(name="Borussia Dortmund"))
    db.session.commit()


