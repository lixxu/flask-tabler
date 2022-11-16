# flask-tabler

flask-tabler is a collection of Jinja macros for [tabler](https://preview.tabler.io/) and Flask.

## Installation

```
$ pip install -U flask-tabler
```

## Example

Register the extension:

```python
from flask import Flask
from flask_tabler import Tabler

app = Flask(__name__)
tabler = Tabler(app)
```

Assuming you have a Flask-WTF form like this:

```python
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()
```

Now with the `render_form` macro:

```html
{% from 'helpers/form.html' import render_form %}
<html>
  <head>
    <!-- css area -->
  </head>
  <body>
    <h2>Login</h2>
    {{ render_form(form) }}

    <!-- js area -->
  </body>
</html>
```
