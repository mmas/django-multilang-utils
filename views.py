from django.http import HttpResponseRedirect
from django.utils import translation


LANGUAGE_COOKIE_KEY = 'mysite_language'
# TODO: increase domain language map.
DOMAIN_LANGUAGE_MAP = {'uk': 'en',
                       'au': 'en'}


def change_language(request, lang):
    """View to change the language and redirect back."""
    lang = lang.lower()
    # TODO: Set a proper url if not referer (use reverse(url) instead of '/').
    url = request.META.get('HTTP_REFERER', '/')
    resp = HttpResponseRedirect(url)
    if lang in [i.code.lower() for i in Language.objects.available()]:
        resp.set_cookie(LANGUAGE_COOKIE_KEY, lang)
    return resp


class LanguageMixin(object):
    """View mixin to activate the language and set language cookie."""

    def dispatch(self, request, *args, **kwargs):
        lang, lang_method = self._get_language(request)
        translation.activate(lang)
        resp = super(LanguageMixin, self).dispatch(request, *args, **kwargs)
        if lang_method in ('meta', 'default'):
            resp.set_cookie(LANGUAGE_COOKIE_KEY, lang)
        return resp

    def _get_language(self, request):
        """
        Returns a tuple with the language and the method used to obtain it.
        Methods:
            'domain': obtained from domain
            'cookie': obtained from a cookie
            'meta': obtained from http_accepted_language
            'default': unable to obtain language, use the default
        """
        lang_list = [i.code.lower() for i in Language.objects.available()]
        is_available = lambda x: x in lang_list

        lang = request.META['HTTP_HOST'].split('.')[-1]
        if lang:
            lang = lang.lower()
            lang = DOMAIN_LANGUAGE_MAP.get(lang, lang)
            if is_available(lang):
                return lang, 'domain'

        lang = request.COOKIES.get(LANGUAGE_COOKIE_KEY)
        if lang:
            lang = lang.lower()
            if is_available(lang):
                return lang, 'cookie'

        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang:
            try:
                lang = lang.split('-')[0]
            except:
                lang = None
            else:
                lang = lang.lower()
                if is_available(lang):
                    return lang, 'meta'
        return lang_list[0], 'default'
