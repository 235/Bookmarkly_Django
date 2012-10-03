from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
import json
import os
import re


def index(request):
    """ Render index page with information about User.
        Cannot use django templates due to a conflict with javascript,
        no way to solve this in django v1.4 """
    try:
        response = {'id': request.user.id, 'username': request.user.username, 'email': request.user.email}
        init = "$(document).ready(function() { App.user = " + json.dumps(response) + "; App.initialize(); });"
    except AttributeError:  # better than another query and checking User.DoesNotExist. AnonymousUser does not have those fields
        init = "$(document).ready(function() { App.initialize(); });"

    filename = os.path.join(settings.STATIC_ROOT, 'templates/index.html')
    fstatic = open(filename)
    content = fstatic.read()
    content = content.replace("{{init}}", init)
    fstatic.close()
    return HttpResponse(content)


def bundle(request, scripts, path):
    """ Creates a bundle of scripts """
    content = ""
    for fl in scripts:
        fstatic = open(path + fl + '.js')
        content += "\n/**\n* " + fl + ".js\n*/\n\n" + fstatic.read() + "\n\n"
        fstatic.close()
    #TBD: comression & caching
    return HttpResponse(content)


def templates(request, templates, path):
    """ Creates a bundle of templates """
    content = "Templates = {};\n"
    for fl in templates:
        fstatic = open(path + fl + '.html')
        html = fstatic.read()
        #html = html.replace(/(\r\n|\n|\r)/gm, ' ').replace(/\s+/gm, ' ').replace(/'/gm, "\\'")
        html = re.sub('(\r\n|\n|\r)', ' ', html, re.MULTILINE)
        html = re.sub('\s+', ' ', html)
        html = re.sub("'", "\\'", html)
        content += "Templates." + fl + " = '" + html + "';\n"
        fstatic.close()
    return HttpResponse(content)
