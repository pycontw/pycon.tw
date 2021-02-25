from core.utils import collect_language_codes, split_css_class


def test_collect_language_codes():
    assert collect_language_codes('zh-tw') == [
        'zh-tw', 'zh', 'en-us', 'en', '_default',
    ]
    assert collect_language_codes('zh') == ['zh', 'en-us', 'en', '_default']
    assert collect_language_codes('en-us') == [
        'en-us', 'en', 'en-us', 'en', '_default',
    ]
    assert collect_language_codes('en') == ['en', 'en-us', 'en', '_default']


def test_split_css_class():
    class_str = ' foo bar baz spam-egg foo '
    assert split_css_class(class_str) == {'foo', 'bar', 'baz', 'spam-egg'}
