def test_talk_proposal_admin_add(admin_client):
    response = admin_client.get('/admin/proposals/talkproposal/')
    assert response.status_code == 200
    response = admin_client.get('/admin/proposals/talkproposal/add/')
    assert response.status_code == 403


def test_tutorial_proposal_admin_add(admin_client):
    response = admin_client.get('/admin/proposals/tutorialproposal/')
    assert response.status_code == 200
    response = admin_client.get('/admin/proposals/tutorialproposal/add/')
    assert response.status_code == 403
