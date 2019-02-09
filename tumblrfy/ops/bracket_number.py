from num2words import num2words
from word2number import w2n
import re
import itertools

from .core import op

_w_zero_to_ten = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
                'nine', 'ten']
_w_eleven_to_nineteen = ['eleven', 'twelve', 'thirteen', 'fourteen',
                'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
_w_tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
        'eighty', 'ninety']
_w_bigger = ['hundred', 'thousand', 'million', 'billion']

r_0_10 = '({w})'.format(w='|'.join(_w_zero_to_ten))
r_11_19 = '({w})'.format(w='|'.join(_w_eleven_to_nineteen))
r_20_99 = '(({tens})'.format(tens='|'.join(_w_tens)) + f'(\s{r_0_10})?' + ')'
r_100_999 = f'(({r_0_10}\s(hundred))(\s(and)\s({r_20_99}|{r_11_19}|{r_0_10}))?)'
_r_1000_999999 = f'({r_100_999}|{r_20_99}|{r_11_19}|{r_0_10})'
_r_1000_999999_2 = f'({r_100_999}|(and {r_20_99})|(and {r_11_19})|(and {r_0_10}))'
r_1000_999999 = f'({_r_1000_999999})( thousand,?)(\s{_r_1000_999999_2})?'
_r_1mil_1bil = f'({r_1000_999999}|{_r_1000_999999})'
_r_1mil_1bil_2 = f'({r_1000_999999}|{_r_1000_999999_2})'
r_1mil_1bil = f'({_r_1mil_1bil})( million)(\s{_r_1mil_1bil_2})?'

num_pattern = re.compile(
    f'{r_1mil_1bil}|{r_1000_999999}|{r_100_999}|{r_20_99}|{r_11_19}|{r_0_10}'#||'
)

digit_pattern = re.compile(
    '(\d([,\s]*\d)*)+'
)

def _get_replacements(text, pattern, replacer_func):
    pos = 0
    replaces = {}
    splits = []
    while pos < len(text):
        num = pattern.search(text, pos)
        if num:
            pos = num.span()[1]
            replaces[num.group(0)] = replacer_func(num.group(0))
            splits.append(num.span())
        else:
            pos = len(text)
    return splits, replaces


def get_word_number_replacements(text):
    def replacer_func(num):
        num = num.replace(',', '')
        new_num = f'{num2words(w2n.word_to_num(num))}'.replace('-', ' ')
        return f'{new_num} ({w2n.word_to_num(num):,})'
    return _get_replacements(text, num_pattern, replacer_func)

def get_digit_number_replacements(text):
    def replacer_func(num):
        num = int(re.sub(r'(,|\s)', '', num))
        return f'{num2words(num).replace("-", " ")} ({num:,})'
    return _get_replacements(text, digit_pattern, replacer_func)

description = """Replaces numbers with the proper tumblr number format.
AKA if there are four (4) numbers written in text they get
replaced by four (4) numbers followed by the bracketed digit
version for those four (4) numbers."""

@op(op_name='bracket-number', description=description)
def bracket_number_process(text):
    num_splits, num_replaces = get_word_number_replacements(text)
    digit_splits, digit_replaces = get_digit_number_replacements(text)
    splits = num_splits + digit_splits
    replaces = {**num_replaces, **digit_replaces}
    new_text = ''
    splits = sorted(
        list(itertools.chain(*list(splits))) + [0, len(text)]
    )
    parts = [text[i:j] for i, j in zip(splits, splits[1:] + [None])]
    for ind in range(len(parts)):
        if ind % 2 == 1:
            new_text += replaces.get(parts[ind], '')
        else:
            new_text += parts[ind]
    return new_text
