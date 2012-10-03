from django.http import HttpResponse
#from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from models import CollectItem, CollectTag
import json
import time


# TBD: rewrite to django-piston later

def collect_item_create(request):
    """ Create item """
    #TBD: fix this dirty hack! Also, cannot use forms since we have a list value and data not in proper format
    formdata = request.POST.keys()[0]
    formdata = json.loads(formdata)

    item = CollectItem(user=request.user,
                       url=formdata['url'],
                       title=formdata['title'],
                       description=formdata['description'])
    item.save()

    for t in formdata['tags']:
        CollectTag(user=request.user, item=item, tag=t).save()
    #serializers.serialize('json', [item, ])  # no, I don't want to expose all fiels

    formdata['id'] = item.id  # Add ID field to identify a new item on frontend
    return HttpResponse(json.dumps(formdata), content_type="application/json")


def collect_item_delete(request, id):
    """ Delete item """
    CollectItem.objects.filter(user=request.user, id=id).delete()
    return HttpResponse('', content_type="application/json")


def collect_item_update(request, id):
    """ Update item """
    try:
        item = CollectItem.objects.filter(user=request.user).get(id=id)
    except CollectItem.DoesNotExist:
        return HttpResponse("{'error': 'The Item that is being updated does not exist!'}", status=400, content_type="application/json")

    formdata = request.read()  # no request.PUT in django, manual processing
    formdata = json.loads(formdata)
    item.url, item.title, item.description = formdata['url'], formdata['title'], formdata['description']
    item.save()

    CollectTag.objects.filter(item=item).delete()
    for t in formdata['tags']:
        tag = CollectTag(user=request.user, item=item, tag=t)
        tag.save()

    formdata['id'] = item.id
    return HttpResponse(json.dumps(formdata), content_type="application/json")


def collect_items_get(request):
    """ Get items """
    if 'tag' in request.GET:  # Form a Queryset
        tags = CollectTag.objects.select_related().filter(tag__exact=request.GET['tag'], user__exact=request.user)
        collection = [t.item for t in tags]
    elif 'search' in request.GET:  # does not work for sqllite
        search = request.GET['search']
        collection = CollectItem.objects.filter(user=request.user)\
                    .filter(Q(url__search=search) | Q(title__search=search) | Q(description__search=search))\
                    .order_by('-timestamp')
    else:
        collection = CollectItem.objects.filter(user=request.user)\
                    .order_by('-timestamp')

    if 'offset' in request.GET:
        offset = int(request.GET['offset'])
        collection = collection[offset:offset + 50]
    else:
        collection = collection[:50]

    items = []
    for i in collection:
        tags = CollectTag.objects.filter(item=i).all()
        items.append({'id': i.id,
                      'url': i.url,
                      'title': i.title,
                      'description': i.description,
                      'timestamp': time.mktime(i.timestamp.timetuple()),
                      'tags': [t.tag for t in tags]
                    })
    #TBD: cache control
    return HttpResponse(json.dumps(items), content_type="application/json")


@login_required
def collect_item(request, id):
    """ Binds update and delete to the same URL -- requests with item ID"""
    if request.method == 'DELETE':
        return collect_item_delete(request, id)
    elif request.method == 'PUT':
        return collect_item_update(request, id)
    return HttpResponse("{'error': 'Wrong request'}", status=400, content_type="application/json")


@login_required
def collect_items(request):
    """ Binds list and crate requests to the same URL"""
    if request.method == 'GET':
        return collect_items_get(request)
    elif request.method == 'POST':
        return collect_item_create(request)
    else:
        return HttpResponse("{'error': 'Wrong request'}", status=400, content_type="application/json")


# =========================================================================


@login_required
def collect_tags(request):
    """ Retrieve a user's tags """
    tags = CollectTag.objects.filter(user__exact=request.user)\
           .values('tag').annotate(Count('tag')).order_by('-tag__count')
    response = [{'tag': t['tag'], 'count': t['tag__count']}\
                for t in tags]
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def autocomplete(request):
    """ Autocomplete for tagging, returns tags matching input """
    try:
        term = request.GET['term']
    except KeyError:
        return HttpResponse(json.dumps({}), status=400, content_type="application/json")
    #tags = CollectTag.objects.values('tag').distinct('tag').filter(tag__icontains=term, user__exact=request.user)  # for advanced DB
    tags = CollectTag.objects.values('tag').filter(tag__icontains=term, user__exact=request.user)  # for sqllite
    response = [t['tag'] for t in tags]
    #TBD: turn on distinct for MySQL, remove manual
    response = list(set(response))  # for sqllite
    return HttpResponse(json.dumps(response), content_type="application/json")
