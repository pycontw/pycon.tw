import pytest

from sponsors.models import OpenRole, Sponsor


@pytest.fixture(autouse=True, scope='function')
def test_data():
    # sponsors
    # # platinum
    sponsor_1 = Sponsor.objects.create(name='1', level=1, is_shown=True)
    # # gold
    sponsor_2 = Sponsor.objects.create(name='2', level=2, order=2, is_shown=True)
    sponsor_3 = Sponsor.objects.create(name='3', level=2, order=None, is_shown=True)  # noqa
    sponsor_4 = Sponsor.objects.create(name='4', level=2, order=1, is_shown=True)  # noqa
    sponsor_5 = Sponsor.objects.create(name='5', level=2, order=3, is_shown=False)  # noqa

    # roles
    OpenRole.objects.create(sponsor=sponsor_1, name='11', description='...')
    OpenRole.objects.create(sponsor=sponsor_2, name='21', description='...')
    OpenRole.objects.create(sponsor=sponsor_2, name='22', description='...')


@pytest.mark.django_db
class TestSponsorAPIView:
    def test_should_get_sponsor_data(self, api_client):
        # arrange: test_data fixture
        # action
        resp = api_client.get('/api/sponsors/')

        # assert
        assert resp.status_code == 200

        data = {level_data['level_name']: level_data['sponsors'] for level_data in resp.data['data']}
        assert list(data.keys()) == ['platinum', 'gold']

        # assert: should have correct sponsor count
        platinum_sponsors = data['platinum']
        assert len(platinum_sponsors) == 1

        gold_sponsors = data['gold']
        assert len(gold_sponsors) == 3

        # assert: gold sponsors should be in correct sequence
        # small-order > large-order > null-order
        gold_sponsor_names = [s['name_en_us'] for s in gold_sponsors]
        assert gold_sponsor_names == ['4', '2', '3']

    def test_should_get_role_data(self, api_client):
        # arrange: test_data fixture
        # action
        resp = api_client.get('/api/sponsors/jobs/')

        # assert
        assert resp.status_code == 200

        data = resp.json()['data']
        assert len(data) == 2

        # assert: sponsor 1
        assert data[0]['sponsor_name'] == '1'

        jobs_1 = data[0]['jobs']
        assert len(jobs_1) == 1
        assert jobs_1[0]['job_name_en_us'] == '11'

        # assert: sponsor 2
        assert data[1]['sponsor_name'] == '2'

        jobs_2 = data[1]['jobs']
        assert len(jobs_2) == 2

        job_names = [j['job_name_en_us'] for j in jobs_2]
        assert set(job_names) == {'21', '22'}
