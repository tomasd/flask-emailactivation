from flask.blueprints import Blueprint
from flask.ext.mail import Message
from flask.globals import current_app
from flask.helpers import url_for
from flask.templating import render_template
from itsdangerous import URLSafeSerializer, BadSignature
from werkzeug.exceptions import abort
from werkzeug.utils import import_string, redirect

app = Blueprint('emailactivation', __name__, template_folder='templates')

def send_activation_email(flaskmail, 
                          email,
                          callback, 
                          data, 
                          email_context, 
                          template_context, 
                          body_template=None, 
                          html_template=None): 
    '''
        Send activation email to the email address specified. When user visits
        the activation link, callback method is called as this callback(data)
        
        Callback returns url where user will be redirected to.
        
        Email contains either plaintext or html version or both. These are
        rendered from the provided template and context with additional parameter
        activation_email_url .
        
        Parameters:
            flaskmail - Instance of flask.ext.mail.Mail
            email - email address
            callback - function which will be called with data, 
                        e.g. callback(data). You can also provide string which 
                        is the full import path for the function:
                        'module1.sub.my_function'. This function cannot be 
                        method or lambda.
            data - json serializable structure passed to the callback
            email_context - dictionary passed to the 
                        flask.ext.mail.message.Message constructor, 
                        note that body, html and recipients will be replaced
                        with values from parameters
            template_context - dictionary used as context for body and html
                        templates, activation_email_url variable will be inserted.
                        This is the activation link
            body_template - name of the template which will be used for body
                        rendering with template_context as context
            html_template - name of the template which will be used for html
                        rendering with template_context as context
    '''

    email_context = email_context.copy()
    
    template_context = template_context.copy()
    signature = signature_serialize(callback, data)
    url = url_for('emailactivation.activation', 
                  signature=signature, 
                  _external=True)
    template_context['activation_email_url'] = url
    
    if body_template:
        email_context['body'] = render_template(body_template, 
                                                       **template_context)
        
    if html_template:
        email_context['html'] = render_template(html_template, 
                                                       **template_context)
    email_context['recipients'] = [email]
    Message(**email_context).send(flaskmail)
    
    
@app.route('/activation/<signature>/', endpoint="activation")
def _activation(signature):
    try:
        callback_str, data = signature_deserialize(signature)
    except BadSignature:
        abort(400)
    
    callback = import_string(callback_str)
    return redirect(callback(data))
    
    
def signature_serialize(callback, data):
    if not isinstance(callback, basestring):
        callback = '%s.%s' % (callback.__module__, callback.__name__)
        
    s = URLSafeSerializer(current_app.secret_key,
                          salt='activation_email')
    return s.dumps((callback, data))

def signature_deserialize(signature):
    s = URLSafeSerializer(current_app.secret_key,
                          salt='activation_email')
    return s.loads(signature)