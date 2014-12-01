#Django multilanguage utilities

Model, view and templatetags to build a multilanguage app with django. To start, fill the language and country tables with the json data provided (iso_languages.json and iso_countries.json). There's no need to set implicitly the language in the url (eg: mysite.com/en/), since the language will be taken from the http request.

##Example models

```
class BlogEntry(MultilangMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)


class BlogEntryContents(ContentsAbstract):
    blog_entry = models.ForeignKey(BlogEntry, related_name='contents')
```

##Example views

```
class BlogEntryDetail(LanguageMixin, DetailView):
    model = models.BlogEntry

    def get_context_data(self, **kwargs):
        ctx = super(BlogEntryDetail, self).get_context_data(**kwargs)
        ctx['available_language_list'] = Language.objects.available()
        return ctx
```

##Example urls

```
url(r'^lang/(?P<lang>\w{2})$', views.change_language, name='change_language'),
```

##Example templates

```
{% for entry in entry_list %}
<a href="{% url 'blog:entry' entry.pk %}">{{entry|name:LANGUAGE_CODE}}</a>
{% endfor %}

...

{% with entry|contents:LANGUAGE_CODE as entry_contents %}
<h1>{{entry_contents.name}}</h1>
<label>{% trans "Created" %}</label> <time datetime="{{entry.created|date:'c'}}">{{entry.created}}</time>
{{entry_contents.decription|linebreaks}}
{% endwith %}

...

{% with entry|contents:LANGUAGE_CODE as entry_contents %}
<meta name="description" content="{{entry_contents.description}}">
<meta name="tags" content="{{entry_contents.tags}}">
{% endwith %}

...

{% for i in available_language_list %}
<a href="{% url 'blog:change_language' i.code %}">{{i.name}}</a>
{% endfor %}
```