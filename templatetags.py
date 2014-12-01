from django import template


register = template.Library()


def get_contents(obj, lang, attr=None):
    try:
        contents = obj.contents.get(language__code=lang.upper())
    except obj.DoesNotExist:
        return ''
    else:
        if attr:
            return getattr(contents, attr, '')
        return contents


def get_contents_name(obj, lang):
    return get_contents(obj, lang, 'name')


def get_contents_description(obj, lang):
    return get_contents(obj, lang, 'description')


register.filter('contents', get_contents)
register.filter('name', get_contents_name)
register.filter('description', get_contents_description)
