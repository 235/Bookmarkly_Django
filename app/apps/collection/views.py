from django.http import HttpResponse
#from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from models import CollectItem, CollectTag
#from forms import CollectItemForm
import json
import time


# TBD: rewrite to django-piston later
@login_required
def collect_item(request, id):
    if request.method == 'DELETE':
        """ Delete item """
        CollectItem.objects.filter(user=User.objects.get(pk=request.user.id), id=id).delete()
        return HttpResponse('', content_type="application/json")
    elif request.method == 'PUT':
        """ Update item """
        try:
            item = CollectItem.objects.filter(user=User.objects.get(pk=request.user.id)).get(id=id)
        except CollectItem.DoesNotExist:
            return HttpResponse("{'error': 'The Item that is being updated does not exist!'}", status=400, content_type="application/json")

        formdata = request.read()  # no request.PUT in django, manual processing
        formdata = json.loads(formdata)
        item.url, item.title, item.description = formdata['url'], formdata['title'], formdata['description']
        item.save()

        CollectTag.objects.filter(item=item).delete()
        for t in formdata['tags']:
            tag = CollectTag(item=item, tag=t)
            tag.save()

        formdata['id'] = item.id
        return HttpResponse(json.dumps(formdata), content_type="application/json")
    return HttpResponse("{'error': 'Wrong request'}", status=400, content_type="application/json")


@login_required
def collect_items(request):
    if request.method == 'GET':
        """ Get items """
        if 'tag' in request.GET:
            tags = CollectTag.objects.select_related().filter(tag__exact=request.GET['tag'])
            collection = [t.item for t in tags]
        elif 'search' in request.GET:
            search = request.GET['search']
            collection = CollectItem.objects.filter(user=User.objects.get(pk=request.user.id))\
                        .filter(Q(url__search=search) | Q(title__search=search) | Q(description__search=search))\
                        .order_by('-timestamp')
        else:
            collection = CollectItem.objects.filter(user=User.objects.get(pk=request.user.id))\
                        .order_by('-timestamp')

        if 'offset' in request.GET:
            offset = int(request.GET['offset'])
            collection = collection[offset:offset + 50]
        else:
            collection = collection[:50]

        items = []
        for i in collection:
            tags = CollectTag.objects.filter(item=i).all()
            tags_list = [t.tag for t in tags]
            items.append({'id': i.id,
                          'url': i.url,
                          'title': i.title,
                          'description': i.description,
                          'timestamp': time.mktime(i.timestamp.timetuple()),
                          'tags': tags_list
                        })

        #TBD: cache control
        return HttpResponse(json.dumps(items), content_type="application/json")
    elif request.method == 'POST':
        """ Create a new Item """
        #TBD: fix this dirty hack! Cannot use forms since we have a list value and data not in proper format
        formdata = request.POST.keys()[0]
        formdata = json.loads(formdata)
        #form = CollectItemForm(formdata)
        #if form.is_valid():
        #    item = CollectItem(user=request.user.id,
        #                       ulr=form.cleaned_data['url'],
        #                       title=form.cleaned_data['title'],
        #                       description=form.cleaned_data['description'])
        item = CollectItem(user=User.objects.get(pk=request.user.id),
                           url=formdata['url'],
                           title=formdata['title'],
                           description=formdata['description'])
        item.save()
        for t in formdata['tags']:
            tag = CollectTag(item=item, tag=t)
            tag.save()
        #serializers.serialize('json', [item, ])  # no, I don't want to expose all fiels
        formdata['id'] = item.id
        return HttpResponse(json.dumps(formdata), content_type="application/json")
        #else:
        #    response = {'error': 'Wrong item form',
        #                'errors': [(k, v[0]) for k, v in form.errors.items()]}
        #    return HttpResponse(json.dumps(response), status=400, content_type="application/json")


@login_required
def collect_tags(request):
    """ Retrieve a user's tags """
    #TBD: retrive tags only of a current user, not for all users!
    tags = CollectTag.objects.values('tag').annotate(Count('tag')).order_by('-tag__count')
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
    #TBD: retrive tags only of a current user, not for all users!
    #tags = CollectTag.objects.values('tag').distinct('tag').filter(tag__icontains=term)
    tags = CollectTag.objects.values('tag').filter(tag__icontains=term)
    response = [t['tag'] for t in tags]
    #TBD: turn on distinct for MySQL, remove manual
    response = list(set(response))
    return HttpResponse(json.dumps(response), content_type="application/json")
