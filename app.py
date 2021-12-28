from flask import Flask, request, render_template, session
from flask.views import View
import logic
import os
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()


class IndexView(View):
    methods = ['GET']

    def __init__(self, template_name):
        self.template_name = template_name
        if not ('Player' in session):
            session['Player'] = pickle.dumps(logic.Player())

    def dispatch_request(self):
        return render_template(self.template_name, session=session)


class PredictView(View):
    context = logic.Player()
    methods = ['GET']

    def __init__(self, template_name):
        self.template_name = template_name
        self.context = pickle.loads(session['Player'])

    def dispatch_request(self):
        self.context.ask_psychics()
        session['Player'] = pickle.dumps(self.context)
        return render_template(self.template_name, Player=self.context, len=len(self.context.history))


class AnswerView(View):
    context = logic.Player()
    methods = ['POST', 'GET']

    def __init__(self, template_name):
        self.template_name = template_name
        self.context = pickle.loads(session['Player'])

    def dispatch_request(self):
        if request.method == "POST":
            digit = int(request.form['digit'])
            self.context.check_predict(digit)
            session['Player'] = pickle.dumps(self.context)
            return render_template('index.html')

        return render_template('answer.html')


app.add_url_rule('/', view_func=IndexView.as_view('index_page', template_name='index.html'))
app.add_url_rule('/predict', view_func=PredictView.as_view('predict_page', template_name='predict.html'))
app.add_url_rule('/answer', view_func=AnswerView.as_view('answer_page', template_name='answer.html'))

if __name__ == '__main__':
    app.run()
