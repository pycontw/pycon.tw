from unicodedata import east_asian_width as eaw

from django.core.validators import MaxLengthValidator


# We duplicate the mapping used in the JavaScript library for consistency.
# N(eutral) class is counted as 1, and A(mbiguous) as 2.
# http://d.hatena.ne.jp/takenspc/20111126#1322252878
_EAW_LEN_MAP = {
    'Na': 1,    # Narrow    - 1
    'H': 1,    # Halfwidth - 1
    'W': 2,    # Wide      - 2
    'F': 2,    # Fullwidth - 2

    'N': 1,    # Neutral   - 1
    'A': 2,    # Ambiguous - 2
}


class EAWMaxLengthValidator(MaxLengthValidator):
    def clean(self, value):
        return sum(_EAW_LEN_MAP.get(eaw(c)) for c in value)
