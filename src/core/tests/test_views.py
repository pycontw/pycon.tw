import itertools
import os

import pytest

from django.utils.translation import activate

from events.models import Schedule


@pytest.mark.django_db
def test_index_page(client):
    response = client.get('/en-us/')
    assert response.status_code == 200
    assert 'PyCon' in response.content.decode('utf-8')


@pytest.mark.xfail(strict=True, reason='TODO: speaking pages not implemented')
@pytest.mark.parametrize('path,expected', [
    ('/en-us/speaking/cfp/',  200),
    ('/en-us/speaking/talk/', 200),
])
def test_speaking_pages(client, path, expected):
    assert client.get(path).status_code == expected


@pytest.mark.parametrize('path,expected', [
    ('/en-us/speaking/base/',  404),
    ('/en-us/speaking/_base/', 404),
])
def test_speaking_bases(client, path, expected):
    assert client.get(path).status_code == expected


def content_page_path_gen():
    # Caon't do module-level import because settings are not configured when
    # the module is imported, only when the code runs.
    from django.conf import settings

    checked = set()
    template_dirs = itertools.chain.from_iterable(
        template_setting['DIRS'] for template_setting in settings.TEMPLATES
    )
    for template_dir in template_dirs:
        for lang in ['en', 'zh']:
            contents_path = os.path.join(template_dir, 'contents', lang)
            if not os.path.exists(contents_path):
                continue
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


@pytest.fixture
def content_page_full_path(language, content_page_path):
    return '/{}{}'.format(language, content_page_path)


def test_content_pages(client, parser, content_page_full_path):
    response = client.get(content_page_full_path)
    assert response.status_code == 200, content_page_full_path


@pytest.fixture
def schedule(db):
    """Generate a schedule to prevent the schedule page from returning 404.
    """
    return Schedule.objects.create(html='<div></div>')


def test_content_pages_links(client, parser, schedule, content_page_full_path):
    """Test to make sure all in-site links in a content page work.
    """
    if '/surveys/conference/' in content_page_full_path:
        pytest.skip("Skip for surveys/conference/ by purpose (or ask TP).")

    body = parser.parse(client.get(content_page_full_path))
    link_tags = body.cssselect('a[href^="/"]:not(a[href^="//"])')

    def get_link_status_pair(tag):
        link = tag.get('href')
        try:
            status = client.get(tag.get('href'), follow=True).status_code
        except Exception:   # Catch internal server error for better reporting.
            status = 500
        return (link, status)

    link_status_codes = [
        get_link_status_pair(tag)
        for tag in link_tags
    ]
    assert link_status_codes, 'isolated page: no links found'

    def get_error_message():
        errors = [
            '    {1} {0!r}'.format(*p)
            for p in link_status_codes
            if p[1] != 200
        ]
        if len(errors) == 1:
            return errors[0].lstrip()
        return 'Links do not return 200 status code\n' + '\n'.join(errors)

    assert all(p[1] == 200 for p in link_status_codes), get_error_message()


def test_content_pages_noopener(client, parser, content_page_full_path):
    body = parser.parse(client.get(content_page_full_path))
    external_link_tags = body.cssselect(
        'a[href^="//"], a[href^="http://"], a[href^="https://"]',
    )

    def get_link_safty_pair(tag):
        link = tag.get('href')
        safe = not tag.get('target') or tag.get('rel') == 'noopener'
        return (link, safe)

    link_noopener_pairs = [
        get_link_safty_pair(tag)
        for tag in external_link_tags
    ]

    def get_error_message():
        errors = [
            '    {0!r}'.format(*p)
            for p in link_noopener_pairs
            if p[1] is not True
        ]
        if len(errors) == 1:
            return errors[0].lstrip()
        return 'External links do not set rel="noopener"\n' + '\n'.join(errors)

    assert all(p[1] is True for p in link_noopener_pairs), get_error_message()
