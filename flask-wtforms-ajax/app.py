from flask import Flask, render_template, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import NumberRange, Length

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False # Don't do this in the real world!


class Form(FlaskForm):
    username = StringField('Username', [
        Length(min=3, max=15, message='Username must be at least %(min)s but no more than %(max)s characters')
    ])
    age = IntegerField('Age', [
        NumberRange(min=14, message='You must be %(min)s or older to sign up')
    ])


@app.route('/traditional', methods=['GET', 'POST'])
def traditional():
    form = Form()
    if form.validate_on_submit():
        return 'WOOT WOOT!'
    return render_template('traditional.html', form=form)


@app.route('/withajax', methods=['GET', 'POST'])
def withajax():
    form = Form()
    if request.method == 'POST':
        if form.validate():
            return 'WOOT WOOT!'
        return jsonify(form.errors), 400
    return render_template('withajax.html', form=form)
