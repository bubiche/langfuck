'''
Heavily influenced by https://github.com/wanqizhu/pyfuck
'''
import re


def encode_py3(text, is_eval_wrap=True):
    # eval+str and friends
    base_char_set = set("eval+str[]'()")

    # except from 0, everything else is x times the value of 1
    encoded_string_by_digit = {
        0: '+all([[]])',
        1: '+all([])',
        2: 'all([])+all([])',
        3: 'all([])+all([])+all([])',
        4: 'all([])+all([])+all([])+all([])',
        5: 'all([])+all([])+all([])+all([])+all([])',
        6: 'all([])+all([])+all([])+all([])+all([])+all([])',
        7: 'all([])+all([])+all([])+all([])+all([])+all([])+all([])',
        8: 'all([])+all([])+all([])+all([])+all([])+all([])+all([])+all([])',
        9: 'all([])+all([])+all([])+all([])+all([])+all([])+all([])+all([])+all([])'
    }

    encoded_string_by_char = {
        'c': 'str(str)[+all([])]',
        'f': 'str(eval)[eval(str(+all([]))+str(+all([[]])))]',
        'n': 'str(eval)[all([])+all([])+all([])+all([])+all([])+all([])+all([])+all([])]',
        'o': 'str(eval)[eval(str(+all([]))+str(all([])+all([])+all([])+all([])+all([])+all([])))]',
        'u': 'str(eval)[all([])+all([])]',
        "'": 'str(str)[all([])+all([])+all([])+all([])+all([])+all([])+all([])]',
        '.': "eval('str('+str(eval)[eval(str(+all([]))+str(+all([[]])))]+'l'+str(eval)[eval(str(+all([]))+str(all([])+all([])+all([])+all([])+all([])+all([])))]+'at(+all([])))[+all([])]')",
        'h': "eval('str(str'+eval('str('+str(eval)[eval(str(+all([]))+str(+all([[]])))]+'l'+str(eval)[eval(str(+all([]))+str(all([])+all([])+all([])+all([])+all([])+all([])))]+'at(+all([])))[+all([])]')+str(str)[+all([])]+str(eval)[eval(str(+all([]))+str(all([])+all([])+all([])+all([])+all([])+all([])))]+str(eval)[all([])+all([])]+str(eval)[all([])+all([])+all([])+all([])+all([])+all([])+all([])+all([])]+'t)[all([])+all([])+all([])+all([])]')"
    }

    # replace the character ' in ''' that will break things
    APOSTROPHE_STANDIN = '\x02'

    def encoded_string_from_num_match_obj(matchobj):
        num_str = matchobj.group(0)
        if len(num_str) == 1:
            return encoded_string_by_digit[int(num_str)]
        else:
            return "'+" + "+".join(['str(' + encoded_string_by_digit[int(i)] + ')' for i in num_str]) + "+'"

    tmp_result = ''

    for c in text:
        if not c.isdigit() and c not in base_char_set and c not in encoded_string_by_char:
            tmp_result += "'+eval('chr(" + str(ord(c)) + ")')+'"
        else:
            if c == "'":
                tmp_result += "'+" + APOSTROPHE_STANDIN + "+'"  # fix triple-quote issue
            else:
                tmp_result += c

    tmp_result = "'" + tmp_result + "'"

    tmp_result_2 = ''

    for c in tmp_result:
        if c in base_char_set or c.isdigit() or c == APOSTROPHE_STANDIN:
            tmp_result_2 += c
        else:
            if c in ['.', 'h']:
                tmp_result_2 += "'+" + encoded_string_by_char[c] + "+'"
            else:
                tmp_result_2 += "'+eval('" + encoded_string_by_char[c] + "')+'"


    pre_processed_text = re.sub(r'\d+', encoded_string_from_num_match_obj, tmp_result_2)
    pre_processed_text = pre_processed_text.replace(APOSTROPHE_STANDIN, encoded_string_by_char["'"])

    # trim leading/trailing empty strings
    pre_processed_text = pre_processed_text.replace("+''+", "+")
    if pre_processed_text[:3] == "''+":
        pre_processed_text = pre_processed_text[3:]
    if pre_processed_text[-3:] == "+''":
        pre_processed_text = pre_processed_text[:-3]

    return ('eval(' + pre_processed_text + ')') if is_eval_wrap else pre_processed_text
