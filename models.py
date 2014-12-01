from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class IsoManager(models.Manager):

    def available(self):
        return self.get_queryset().filter(available=True)


class IsoAbstract(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    available = models.BooleanField(default=False)

    objects = IsoManager()

    class Meta:
        abstract = True
        ordering = ('-available', 'code',)

    def __unicode__(self):
        return '(%s) %s' % (self.code, self.name)


class Language(IsoAbstract):
    pass


class Country(IsoAbstract):
    currency = models.CharField(max_length=3)


class MultilangMixin(object):

    def __unicode__(self):
        try:
            contents = self.contents.get(language__code='EN')
        except ObjectDoesNotExist:
            contents = self.contents.first()
        if contents:
            return contents.name
        return ''

    def contents_in_language(self, language):
        try:
            return self.contents.get(language__code=language.upper())
        except ObjectDoesNotExist:
            return None


class ContentsAbstract(models.Model):
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
