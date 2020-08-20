#!/bin/bash
#

function community_track() {
cd src
python manage.py shell << EOF

from ext2020.models import Venue
Venue.objects.all().delete()
venue_list = [
    {'name':'古蹟出張所','photo':'pycontw-2020/assets/community-track/b16tainan.jpg'},
    {'name':'Tsang Fong Coffee','photo':'pycontw-2020/assets/community-track/tsang-fong-coffee.jpg'},
    {'name':'Masa Loft','photo':'pycontw-2020/assets/community-track/masaloft.jpg'},
    {'name':'Angry Burger','photo':'pycontw-2020/assets/community-track/angry-burger.jpg'},
    {'name':'Three Doors Brunch','photo':'pycontw-2020/assets/community-track/three-doors-brunch.jpg'}
]

for i in venue_list:
   Venue.objects.create(**i)

EOF
}

community_track
