from django.utils.translation import gettext_lazy as _

CATEGORY_CHOICES = (
    ('APPL', _('Application')),
    ('PRAC', _('Best Practices & Patterns')),
    ('COM', _('Community')),
    ('DB', _('Databases')),
    ('DATA', _('Data Analysis')),
    ('EDU', _('Education')),
    ('EMBED', _('Embedded Systems')),
    ('FIN', _('FinTech')),
    ('IOT', _('Internet of Things')),
    ('GAME', _('Gaming')),
    ('GRAPH', _('Graphics')),
    ('ML', _('Machine Learning')),
    ('NLP', _('Natural Language Processing')),
    ('CORE', _('Python Core (language, stdlib, etc.)')),
    ('TOOL', _('Project Tooling')),
    ('SCI', _('Science')),
    ('SEC', _('Security')),
    ('ADMIN', _('Systems Administration')),
    ('TEST', _('Testing')),
    ('WEB', _('Web Frameworks')),
    ('OTHER', _('Other')),
)

LANGUAGE_CHOICES = (
    ('ENEN', _('English talk')),
    ('ZHEN', _('Chinese talk w. English slides')),
    ('ZHZH', _('Chinese talk w. Chinese slides')),
    ('TAI', _('Taiwanese Hokkien')),
)

PYTHON_LVL_CHOICES = (
    ('NOVICE', _('Novice')),
    ('INTERMEDIATE', _('Intermediate')),
    ('EXPERIENCED', _('Experienced')),
)

RECORDING_POLICY_CHOICES = (
    (True, _('Yes')),
    (False, _('No'))
)

LIVING_IN_TAIWAN_CHOICES = (
    (True, _('Yes')),
    (False, _('No'))
)

LIVE_STREAM_POLICY_CHOICES = (
    (True, _('Yes')),
    (False, _('No'))
)

REFERRING_POLICY_CHOICES = (
    (True, _('Yes')),
    (False, _('No'))
)

ATTEND_IN_PERSON = (
    (True, _('Yes')),
    (False, _('No')),
)
