from emailactivation.views import send_activation_email, signature_serialize
from flask.app import Flask
from flask.ext.mail import Mail
from flask.helpers import url_for
from mock import patch
from unittest.case import TestCase
import emailactivation
import unittest

def my_callback(data):
    return url_for('index')

class EmailActivationTest(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(emailactivation.views.app)
        self.app.config['SECRET_KEY'] = 'SECRET'
        self.mail = Mail(self.app)
        
        @self.app.route('/index')
        def index():
            return 'index'
        
    def testSendEmail(self):
        callback = my_callback
        
        data = {'mail':'test@example.com'}
        email = {'subject':'subject', 
                 'sender':'sender@example.com'}
        with patch('test_activation.my_callback') as c:
            with self.app.test_request_context():
                c.return_value = url_for('index') 
                signature = signature_serialize(callback, data)
                with self.mail.record_messages() as outbox:
                    send_activation_email(self.mail,
                                          'test@example.com',
                                          callback=callback,
                                          data=data,
                                          email_context=email,
                                          template_context={},
                                          body_template='test.html')
                                      
                self.assertEquals(1, len(outbox), 'Email was sent')
                self.assertIn(url_for('emailactivation.activation', 
                                      signature=signature, _external=True),
                              outbox[0].body)
                
                with self.app.test_client() as client:
                    response = client.get(url_for('emailactivation.activation', 
                                                   signature=signature,))
                    self.assertEquals(302, response.status_code)
                    self.assertEquals(url_for('index', _external=True), 
                                      response.location)
                    
#                c.assert_called_with(data)
            
        
if __name__ == '__main__':
    unittest.main()
