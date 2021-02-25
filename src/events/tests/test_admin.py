import pytest

from django.contrib.admin import site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import AnonymousUser
from django.utils.encoding import force_str

from events.admin import (
    CustomEventAdmin, KeynoteEventAdmin, ProposedTalkEventAdmin,
    SponsoredEventAdmin, TimeAdmin,
)
from events.models import (
    CustomEvent, KeynoteEvent, ProposedTalkEvent, SponsoredEvent, Time,
)


@pytest.fixture
def choices_factory():

    def build_changelist_choices(request, model_class, modeladmin, index=0):
        request.user = AnonymousUser()
        # yychen 2020-02-02: the request factory does not support middleware,
        # so no user would be set in request.
        # However, a check of request.user is performed in ChangeList()
        # which will cause error.
        # So we inject AnonymousUser here
        # https://stackoverflow.com/questions/54183451
        # https://docs.djangoproject.com/en/3.0/topics/testing/advanced/#the-request-factory
        changelist = ChangeList(
            request, model_class, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
            modeladmin.sortable_by,
        )
        filterspec = changelist.get_filters(request)[0][index]
        choices = filterspec.choices(changelist)
        return choices

    return build_changelist_choices


def conv_choice(choice):
    """Helper to convert choices dict to comparable value.
    """
    return (
        choice['query_string'],
        force_str(choice['display']),
        choice['selected'],
    )


@pytest.fixture
def time_admin():
    return TimeAdmin(Time, site)


@pytest.mark.django_db
def test_time_range_filter(rf, djutils, time_admin, choices_factory):
    choices = choices_factory(rf.get('/'), Time, time_admin)
    assert djutils.to_list(choices, conv_choice) == [
        ('?', 'All', True),
        ('?time-range=day1', 'Day 1', False),
        ('?time-range=day2', 'Day 2', False),
    ]


@pytest.mark.django_db
def test_time_range_filter_selection(rf, djutils, time_admin, choices_factory):
    request = rf.get('/', {'time-range': 'day2'})
    choices = choices_factory(request, Time, time_admin)
    assert djutils.to_list(choices, conv_choice) == [
        ('?', 'All', False),
        ('?time-range=day1', 'Day 1', False),
        ('?time-range=day2', 'Day 2', True),
    ]


@pytest.mark.parametrize('model_class,admin_class', [
    (CustomEvent, CustomEventAdmin),
    (KeynoteEvent, KeynoteEventAdmin),
    (ProposedTalkEvent, ProposedTalkEventAdmin),
    (SponsoredEvent, SponsoredEventAdmin),
])
@pytest.mark.django_db
def test_begin_time_range_filter(
        rf, djutils, model_class, admin_class, choices_factory):
    admin = admin_class(model_class, site)
    choices = choices_factory(rf.get('/'), model_class, admin)
    assert djutils.to_list(choices, conv_choice) == [
        ('?', 'All', True),
        ('?begin-time=day1', 'Day 1', False),
        ('?begin-time=day2', 'Day 2', False),
    ]


@pytest.mark.parametrize('model_class,admin_class', [
    (CustomEvent, CustomEventAdmin),
    (KeynoteEvent, KeynoteEventAdmin),
    (ProposedTalkEvent, ProposedTalkEventAdmin),
    (SponsoredEvent, SponsoredEventAdmin),
])
@pytest.mark.django_db
def test_begin_time_range_filter_selection(
        rf, djutils, model_class, admin_class, choices_factory):
    admin = admin_class(model_class, site)
    request = rf.get('/', {'begin-time': 'day2'})
    choices = choices_factory(request, model_class, admin)
    assert djutils.to_list(choices, conv_choice) == [
        ('?', 'All', False),
        ('?begin-time=day1', 'Day 1', False),
        ('?begin-time=day2', 'Day 2', True),
    ]


@pytest.mark.parametrize('model_class,admin_class', [
    (CustomEvent, CustomEventAdmin),
    (KeynoteEvent, KeynoteEventAdmin),
    (ProposedTalkEvent, ProposedTalkEventAdmin),
    (SponsoredEvent, SponsoredEventAdmin),
])
@pytest.mark.django_db
def test_end_time_range_filter(
        rf, djutils, model_class, admin_class, choices_factory):
    admin = admin_class(model_class, site)
    choices = choices_factory(rf.get('/'), model_class, admin, 1)
    assert djutils.to_list(choices, conv_choice) == [
        ('?', 'All', True),
        ('?end-time=day1', 'Day 1', False),
        ('?end-time=day2', 'Day 2', False),
    ]


@pytest.mark.parametrize('model_class,admin_class', [
    (CustomEvent, CustomEventAdmin),
    (KeynoteEvent, KeynoteEventAdmin),
    (ProposedTalkEvent, ProposedTalkEventAdmin),
    (SponsoredEvent, SponsoredEventAdmin),
])
@pytest.mark.django_db
def test_end_time_range_filter_selection(
        rf, djutils, model_class, admin_class, choices_factory):
    admin = admin_class(model_class, site)
    request = rf.get('/', {'end-time': 'day1'})
    choices = choices_factory(request, model_class, admin, 1)
    assert djutils.to_list(choices, conv_choice) == [
        ('?', 'All', False),
        ('?end-time=day1', 'Day 1', True),
        ('?end-time=day2', 'Day 2', False),
    ]
