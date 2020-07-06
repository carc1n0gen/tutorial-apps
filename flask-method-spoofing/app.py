from flask import Flask, render_template, request, Request as FlaskRequest
from werkzeug.formparser import parse_form_data


class InputProcessed():
    """A file like object that just raises an error when it is read."""

    def read(self, *args):
        raise EOFError(
            'The wsgi.input stream has already been consumed, check environ["wsgi._post_form"] \
             and environ["wsgi._post_files"] for previously processed form data.'
        )
    readline = readlines = __iter__ = read


class MethodSpooferMiddleware():
    """
    A WSGI middleware that checks for a method spoofing form field
    and overrides the request method accordingly.
    """

    def __init__(self, app, input_name='_method'):
        self.app = app
        self.input_name = input_name

    def __call__(self, environ, start_response):
        # We only want to spoof if the request method is POST
        if environ['REQUEST_METHOD'].upper() == 'POST':
            stream, form, files = parse_form_data(environ)

            # Replace the wsgi.input stream with an object that will raise an error if
            # it is read again, and explaining how to get previously processed form data.
            environ['wsgi.input'] = InputProcessed()

            # Set the processed form data on environ so it can be retrieved again inside
            # the app without having to process the form data again.
            environ['wsgi._post_form'] = form
            environ['wsgi._post_files'] = files

            method = form.get(self.input_name)
            if method:
                # Override the request method _if_ there was a method spoofing field.
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)


class Request(FlaskRequest):
    """
    A custom request object that checks for previously processed form data
    instead of possibly processing form data twice.
    """

    @property
    def form(self):
        if 'wsgi._post_form' in self.environ:
            # If cached form data exists.
            return self.environ['wsgi._post_form']
        # Otherwise return the normal dict like object you would usually use.
        return super().form

    @property
    def files(self):
        if 'wsgi._post_files' in self.environ:
            # If cached files data exists.
            return self.environ['wsgi._post_files']
        # Otherwise return the normal dict like object you would usually use.
        return super().files


app = Flask(__name__)
app.request_class = Request
app.wsgi_app = MethodSpooferMiddleware(app.wsgi_app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/delete', methods=['DELETE'])
def delete_the_thing():
    foo = request.form.get('foo')
    return f'We made it to the delete route and we can still get form data, foo: {foo}'
