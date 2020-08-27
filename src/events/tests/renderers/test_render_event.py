import pytest

from events import renderers


def test_render_customevent(parser, utils, custom_partial_belt_event):
    rendered = renderers.render_customevent(custom_partial_belt_event)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        <div class="slot-item__content">
          <div class="slot-item__title">Job Fair</div>
        </div>
    """)


def test_render_keynoteevent(parser, utils, keynote_belt_event):
    rendered = renderers.render_keynoteevent(keynote_belt_event)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        <div class="slot-item__content talk">
          <div class="slot-item__title">Keynote</div>
          <a href="/en-us/conference/keynotes/#keynote-speaker-amber-brown"
               class="talk__speaker">
            Amber Brown
          </a>
        </div>
    """)


def test_render_proposedtalkevent(parser, utils, proposed_talk_block_event):
    rendered = renderers.render_proposedtalkevent(proposed_talk_block_event)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        <div class="slot-item__content talk">
          <a href="/en-us/conference/talk/42/" class="talk__title">
            Beyond the Style Guides&lt;br&gt;
          </a>
          <a href="/en-us/conference/talk/42/#speaker-content"
              class="talk__speaker">
            User and Misaki Mei
          </a>
          <div class="talk__lang">EN Slides</div>
        </div>
    """)


def test_render_sponsoredevent(parser, utils, sponsored_block_event):
    rendered = renderers.render_sponsoredevent(sponsored_block_event)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        <div class="slot-item__content sponsored talk">
          <a href="/en-us/conference/talk/sponsored/camera-engine/"
              class="talk__title">
            Camera engine office woman lights
          </a>
          <a href="/en-us/conference/talk/sponsored/camera-engine/#speaker-content"
              class="talk__speaker">
            User
          </a>
          <div class="talk__lang">ZH</div>
        </div>
    """)


@pytest.mark.parametrize('event_key', [
    'custom_event', 'keynote_event', 'proposed_talk_event', 'sponsored_event',
])
def test_render_event(parser, utils, events, event_key):
    event = events[event_key]
    rendered = renderers.render_event(event)
    assert utils.is_safe(rendered)

    expected = {
        'custom_event': """
            <div class="slot-item__content">
              <div class="slot-item__title">Job Fair</div>
            </div>""",
        'keynote_event': """
            <div class="slot-item__content talk">
              <div class="slot-item__title">Keynote</div>
              <a href="/en-us/conference/keynotes/#keynote-speaker-amber-brown"
                   class="talk__speaker">
                Amber Brown
              </a>
            </div>""",
        'proposed_talk_event': """
            <div class="slot-item__content talk">
              <a href="/en-us/conference/talk/42/" class="talk__title">
                Beyond the Style Guides&lt;br&gt;
              </a>
              <a href="/en-us/conference/talk/42/#speaker-content"
                  class="talk__speaker">
                User and Misaki Mei
              </a>
              <div class="talk__lang">EN Slides</div>
            </div>""",
        'sponsored_event': (
            '<div class="slot-item__content sponsored talk">'
            '  <a href="/en-us/conference/talk/sponsored/camera-engine/"'
            '      class="talk__title">'
            '    Camera engine office woman lights'
            '  </a>'
            '  <a href="/en-us/conference/talk/sponsored/camera-engine/'
            '#speaker-content" class="talk__speaker">'
            '    User'
            '  </a>'
            '  <div class="talk__lang">ZH</div>'
            '</div>'),
    }[event_key]
    assert parser.arrange(rendered) == parser.arrange(expected)


def test_render_event_fail(user):
    with pytest.raises(ValueError) as ctx:
        renderers.render_event(user)
    assert str(ctx.value) == (
        "No suitable renderer for <User: user@user.me> "
        "of <class 'users.models.User'>"
    )
