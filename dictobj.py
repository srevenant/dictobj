# vim:set et ts=4 sw=4 ai ft=python:

"""
Dictionary Object

Copyright 2016 Brandon Gillespie

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import copy

class DictObj(dict):
    """
    Represent a dictionary in object form.  Recursive.

    Not pythonic because it provides an alternate way to use dictionaries.
    But I'm okay with this, becuase it is handy.

    Limitations:

       * raises error if there is a name conflict with reserved words
       * reserves the prefix \f$\f for internal use (also raises error)

    There are simpler ways of doing this, but this is the most functional imho.

    >>> test_dict = {"\f$\fbogus":1}
    >>> test_obj = DictObj(**test_dict) # doctest: +ELLIPSIS
    Traceback (most recent call last):
     ...
    ValueError: Key may not begin with \\f$\\f
    >>> test_obj = DictObj(copy='test') # doctest: +ELLIPSIS
    Traceback (most recent call last):
     ...
    ValueError: Key 'copy' conflicts with reserved word
    >>> test_dict = {"a":{"b":1,"ugly var!":2}, "c":3}
    >>> test_obj = DictObj(**test_dict)
    >>> orig_obj = test_obj.copy() # test this later
    >>> test_obj.keys()
    ['a', 'c']
    >>> 'a' in test_obj
    True
    >>> for key in test_obj:
    ...     key
    'a'
    'c'
    >>> test_obj.get('c')
    3
    >>> test_obj['c']
    3
    >>> test_obj.c
    3
    >>> test_obj.c = 4
    >>> test_obj.c
    4
    >>> test_obj.a.b
    1
    >>> test_obj.a.ugly_var_
    2
    >>> test_obj.a['ugly var!']
    2
    >>> test_obj
    {'a': {'b': 1, 'ugly var!': 2, 'ugly_var_': 2}, 'c': 4}
    >>> test_obj.dict() # "ugly var!" is back
    {'a': {'b': 1, 'ugly var!': 2}, 'c': 4}
    >>> test_obj.a.ugly_var_ = 10
    >>> test_obj.a.ugly_var_
    10
    >>> orig_obj.dict()
    {'a': {'b': 1, 'ugly var!': 2}, 'c': 3}
    """

    __reserved__ = set(dir(dict) + ['dict', '__init__', '__repr__','export', '__iter__', '__contains__', 'copy', '__reserved__'])

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __init__(self, **attrs):
        for key in attrs:
            if key[:3] == '\f$\f':
                raise ValueError("Key may not begin with \\f$\\f")
            newkey = re.sub(r'[^a-zA-Z0-9_]', '_', key)
            if newkey in self.__reserved__:
                raise ValueError("Key '{}' conflicts with reserved word".format(newkey))

            value = attrs[key]
            if isinstance(value, dict) or isinstance(value, DictObj):
                value = DictObj(**value)
            setattr(self, newkey, value)
            if newkey != key: # set both
                setattr(self, '\f$\f' + newkey, key)
                setattr(self, key, value)

    def dict(self):
        """
        Return original dictionary form, not rewritten keys
        Alternate to self.export()
        """
        rewrite = {}
        exported = {}
        for key in self:
            if key[:3] == '\f$\f':
                rewrite[key[3:]] = self[key]
            else:
                value = self[key]
                if isinstance(value, DictObj):
                    value = value.dict()
                exported[key] = value
        for key in rewrite:
            exported[rewrite[key]] = exported[key]
            del exported[key]

        return exported

    def __repr__(self):
        return str(self.export())

    def export(self):
        """
        Export using rewritten keys, not original keys
        Alternate to self.dict()
        """
        exported = {}
        for key in self:
            if key[:3] != "\f$\f":
                value = self[key]
                if isinstance(value, DictObj):
                    value = value.export()
                exported[key] = value
        return exported

    def copy(self):
        return DictObj(**self.dict())

