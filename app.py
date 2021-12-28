from flask import Flask, request, render_template, session
from flask.views import View
import logic
import os
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()


@app.route('/', methods=['GET'])
def index():
    if not('Player' in session):
        session['Player'] = pickle.dumps(logic.Player())
    return render_template('index.html', session=session)


@app.route('/predict', methods=['GET'])
def predict():
    pl = pickle.loads(session['Player'])
    pl.ask_psychics()
    session['Player'] = pickle.dumps(pl)

    if not session.modified:
        session.modified = True

    return render_template('predict.html', Player=pl, len=len(pl.history))


@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if request.method == "POST":
        pl = pickle.loads(session['Player'])
        digit = int(request.form['digit'])
        pl.check_predict(digit)
        session['Player'] = pickle.dumps(pl)

        if not session.modified:
            session.modified = True

        return render_template('index.html')
    return render_template('answer.html')


if __name__ == '__main__':
    app.run()

