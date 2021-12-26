from flask import Flask, request, render_template, session
import psychics
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()


@app.route('/', methods=['GET'])
def index():
    if not('history_digit' in session):
        session['history_digit'] = []
    if not ('proxy_list' in session):
        session['proxy_list'] = [0, 0]
    if not('history_psychic1' in session):
        session['history_psychic1'] = []
    if not('history_psychic2' in session):
        session['history_psychic2'] = []

    return render_template('index.html', session=session)


@app.route('/predict', methods=['GET'])
def predict():
    answer_1 = psychics.random_psychic.predict()

    if len(session['history_psychic2']) == 0:
        answer_2 = 10
    else:
        answer_2 = psychics.range_psychic.predict(session['history_psychic2'][-1])

    if (len(session['history_psychic1']) - len(session['history_digit'])) == 1:
        session['history_psychic1'][-1] = answer_1
        session['history_psychic2'][-1] = answer_2
    else:
        session['history_psychic1'].append(answer_1)
        session['history_psychic2'].append(answer_2)

    if not session.modified:
        session.modified = True

    return render_template('predict.html', session=session, len=len(session['history_digit']))


@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if request.method == "POST":
        digit = int(request.form['digit'])
        session['history_digit'].append(digit)

        if session['history_psychic1'][-1] == digit:
            session['proxy_list'][0] += 1
        else:
            session['proxy_list'][0] -= 1

        if session['history_psychic2'][-1] == digit:
            session['proxy_list'][1] += 1
        else:
            session['proxy_list'][1] -= 1

        if not session.modified:
            session.modified = True

        return render_template('index.html', session=session)
    return render_template('answer.html', session=session)


if __name__ == '__main__':
    app.run()

