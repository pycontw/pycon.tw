import os

import pytest

from django.test import override_settings
from django.utils.translation import activate

from core.utils import collect_language_codes, split_css_class


def test_locale_fallback_middleware(client, settings):
    response = client.get('/en/', follow=True)
    assert response.redirect_chain == [('/en-us/', 302)]


@override_settings(USE_I18N=False)
def test_locale_fallback_middleware_no_i18n(client, settings):
    response = client.get('/en/')
    assert response.status_code == 404


def test_collect_language_codes():
    assert collect_language_codes('zh-tw') == ['zh-tw', 'zh', 'en-us', 'en']
    assert collect_language_codes('zh') == ['zh', 'en-us', 'en']
    assert collect_language_codes('en-us') == ['en-us', 'en', 'en-us', 'en']
    assert collect_language_codes('en') == ['en', 'en-us', 'en']


def test_split_css_class():
    class_str = ' foo bar baz spam-egg foo '
    assert split_css_class(class_str) == {'foo', 'bar', 'baz', 'spam-egg'}


def test_index_page(client):
    response = client.get('/en-us/')
    assert response.status_code == 200
    assert 'PyCon' in response.content.decode('utf-8')


@pytest.mark.parametrize('path,expected', [
    ('/en-us/speaking/cfp/',   200),
    ('/en-us/speaking/talk/',  200),
    ('/en-us/speaking/base/',  404),
    ('/en-us/speaking/_base/', 404),
])
def test_speaking_pages(client, path, expected):
    assert client.get(path).status_code == expected


def content_page_path_gen():
    from django.conf import settings
    checked = set()
    for template_setting in settings.TEMPLATES:
        for template_dir in template_setting['DIRS']:
            for lang in ['en', 'zh']:
                contents_path = os.path.join(template_dir, 'contents', lang)
                os.chdir(contents_path)
                for dirpath, _, filenames in os.walk('.'):
                    if os.path.basename(dirpath).startswith('_'):
                        continue
                    for filename in filenames:
                        if filename.startswith('_'):
                            continue
                        root, ext = os.path.splitext(filename)
                        if ext != '.html':
                            continue
                        comps = [c for c in dirpath.split(os.sep) if c != '.']
                        path = '/'.join([''] + comps + [root, ''])
                        if path in checked:
                            continue
                        yield path
                        checked.add(path)


@pytest.fixture(params=content_page_path_gen())
def content_page_path(request):
    return request.param


def language_gen():
    from django.conf import settings
    for lang_code, _ in settings.LANGUAGES:
        yield lang_code


@pytest.fixture(params=language_gen())
def language(request, settings):
    lang = request.param

    def activate_default_language():
        activate(settings.LANGUAGE_CODE)

    request.addfinalizer(activate_default_language)
    activate(lang)
    return lang


def test_content_pages(client, language, content_page_path):
    path = '/' + language + '/' + content_page_path
    response = client.get(path)
    assert response.status_code == 200, path
