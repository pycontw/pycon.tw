

def get_sponsors():
    from sponsors.models import Sponsor
    return Sponsor.objects.all()


EXTRA_DATA = {}
EXTRA_DATA[''] = {
    'sponsors': get_sponsors,
}
