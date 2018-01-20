from __future__ import absolute_import

import copy
import datetime
import six
from dateutil.parser import parse as parse_date


class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]


class AddressableList(list):
    """ List of items addressable either by id or by name """
    def __init__(self, items, name='items'):
        super(AddressableList, self).__init__(items)
        self.name = name

    def __getitem__(self, key):
        if isinstance(key, int):
            return super(AddressableList, self).__getitem__(key)
        else:
            matches = [item for item in self if item.title == key or item.id == key]
            count = len(matches)
            if count > 1:
                matches = list(map(repr, matches))
                error = "Found multiple matches for {key}: {matches}. ".format(
                    key=key, matches=", ".join(matches))
                advice = "Use the identifier instead."
                raise KeyError(error + advice)
            elif count == 1:
                return matches[0]
            else:
                raise KeyError("Cannot find {key} among the available {name}"
                               .format(key=key, name=self.name))

    def _repr_html_(self):
        """ HTML formating for iPython users """
        html = "<table>"
        html += "<tr><td><b>{0}</b></td><td><b>{1}</b></td></tr>".format("ID", "Title")
        for i in self:
            html += "<tr>"
            html += i._repr_html_()
            html += "</tr>"
        html += "</table>"
        return html

    def __str__(self):
        string = ""
        for i in self:
            string += i.__str__()
        return string

    def __repr__(self):
        return "<AddressableList>"


def date(obj):
    # used to ensure compatibility with Python3 without having to use six
    try:
        basestring
    except NameError:
        basestring = str

    if obj is None:
        return None
    elif isinstance(obj, datetime.date):
        if hasattr(obj, 'date'):
            return obj.date()
        else:
            return obj
    elif isinstance(obj, six.string_types):
        return parse_date(obj).date()
    elif isinstance(obj, six.text_type):
        return parse_date(str(obj)).date()
    else:
        raise ValueError("Can only convert strings into dates, received {}"
                         .format(obj.__class__))


def wrap(obj):
    if isinstance(obj, list):
        return obj
    else:
        return [obj]


def affix(base, prefix="", suffix="", connector="_"):
    parts = [part for part in [prefix, base, suffix] if part != ""]
    return connector.join(parts)


def translate(d, mapping):
    d = copy.copy(d)

    for src, dest in mapping.items():
        if src in d:
            d[dest] = d[src]
            del d[src]
    return d