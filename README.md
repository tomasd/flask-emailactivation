flask-emailactivation
=====================

Blueprint for email activation. Provides method send_activation_email 
for sending an email with activation link. You are passing callback and data 
parameters. When user visits the link callback is called with data as parameter.

You need to setup Flask-mail (http://packages.python.org/flask-mail/) and 
flask app SECRET_KEY.

== Installation
```
	$ pip install git+git://github.com/tomasd/flask-emailactivation.git
```

== Usage
```python
from flask.app import Flask
from emailactivation.views import send_activation_email
from flask.ext.mail import Mail

app = Flask(__name__)
app.register_blueprint(emailactivation.views.app)
app.config['SECRET_KEY'] = 'SECRET'
mail = Mail(self.app)

def callback(data):
	'''
		process data, in this case
		{'data1':'this will be passed as an argument'}
	'''
	return url_for('index')

data = {'data1':'this will be passed as an argument'}
email = {'subject':'subject', 'sender':'sender@example.com'}

send_activation_email(self.mail,
                      'test@example.com',
                      callback=callback,
                      data=data,
                      email_context=email,
                      template_context={'customer_id':1},
                      body_template='test.html')

```