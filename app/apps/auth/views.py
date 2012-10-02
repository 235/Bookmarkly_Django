from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json


def register(request):  # Register a new user
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
                user.save()
            except IntegrityError:
                return HttpResponse("{ error: 'There is already an account with that e-mail or username' }", content_type="application/javascript")
            #login(request, user)
            response = {'id': user.id, 'username': user.username, 'email': user.email}
            return HttpResponse(json.dumps(response), content_type="application/javascript")
        else:
            #TBD: show errors
            response = {'error': 'There are errors in the form',
                        'errors': [(k, v[0]) for k, v in form.errors.items()]}
            return HttpResponse(json.dumps(response), status=400, content_type="application/javascript")
    else:
        return HttpResponse("{ error: 'No register form' }", status=400, content_type="application/javascript")


@login_required
def update(request):
    """ Update a user's profile """
    print 'updating'
    if request.method == 'PUT':
        print 'put'
        formdata = request.read()  # no request.PUT in django, manual processing
        import urlparse
        formdata = urlparse.parse_qs(formdata)
        print formdata
        formdata = dict([(x, y[0]) for x, y in formdata.iteritems()])
        print 'request read'
        print formdata
        form = RegisterForm(formdata)
        print 'form initialised'
        if form.is_valid():
            print 'form is is_valid'
            user = User.objects.get(pk=request.user.id)
            user.username, user.email, user.password = form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']
            user.save()
        else:
            #TBD: show errors
            print 'form unvalid'
            response = {'error': 'There are errors in the form',
                        'errors': [(k, v[0]) for k, v in form.errors.items()]}
            return HttpResponse(json.dumps(response), content_type="application/javascript")
    return HttpResponse("{'error': 'Wrong request'}", status=400, content_type="application/json")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = {'id': user.id, 'username': user.username, 'email': user.email}
                    return HttpResponse(json.dumps(response), content_type="application/javascript")

                    # client.query('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', [req.session.user_id]);
                else:
                    # Return a 'disabled account' error message
                    return HttpResponse("{ error: 'Disabled account' }", status=401, content_type="text/html")
            else:
                # Return an 'invalid login' error message.
                return HttpResponse("{ error: 'Invalid Login' }", status=401, content_type="text/html")
    return HttpResponse("{ error: 'Invalid Login Method' }", status=400, content_type="text/html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponse('', status=200, content_type="text/html")
