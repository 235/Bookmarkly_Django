from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


class CollectItem(models.Model):
    user        = models.ForeignKey(User)

    title       = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    url         = models.URLField(max_length=450, null=True, blank=True)

    timestamp   = models.DateTimeField(auto_now_add=True)
    private     = models.BooleanField(default=True)

    img_url     = models.URLField(max_length=450, null=True, blank=True, \
                  verbose_name='Image URL', \
                  help_text='link to the product''s image')
    price       = models.FloatField(null=True, blank=True)
    quantity    = models.FloatField(null=True, blank=True)
    date_expire = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('collectItem', args=[self.id])


class CollectTag(models.Model):
    user        = models.ForeignKey(User)
    item        = models.ForeignKey(CollectItem)
    tag         = models.CharField(max_length=255)

    def __unicode__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('collectTag', args=[self.tag])
