from __future__ import print_function
import sqlparse
from parseutils import last_word, extract_tables


def suggest_type(full_text, text_before_cursor):
    """Takes the full_text that is typed so far and also the text before the
    cursor to suggest completion type and scope.

    Returns a tuple with a type of entity ('table', 'column' etc) and a scope.
    A scope for a column category will be a list of tables.
    """

    tables = extract_tables(full_text)

    parsed = sqlparse.parse(strip_partial_word(text_before_cursor))

    if parsed:
        last_token = parsed[0].token_prev(len(parsed[0].tokens))
        last_token_v = last_token.value if last_token else ''

    if last_token_v.lower().endswith('('):
        return ('columns', tables)
    if last_token_v.lower() in ('set', 'by', 'distinct'):
        return ('columns', tables)
    elif last_token_v.lower() in ('select', 'where', 'having'):
        return ('columns-and-functions', tables)
    elif last_token_v.lower() in ('from', 'update', 'into', 'describe'):
        return ('tables', tables)
    elif last_token_v in ('d',):  # \d
        return ('tables', tables)
    elif last_token_v.lower() in ('c', 'use'):  # \c
        return ('databases', tables)
    else:
        return ('keywords', tables)

def strip_partial_word(text):
    word_before_cursor = last_word(text, include_special_chars=True)

    # word_before_cursor will be empty if no partial word was typed.
    if word_before_cursor:
        return text[:-len(word_before_cursor)]
    else:
        return text
