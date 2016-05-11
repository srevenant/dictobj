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

class DictObj(object):
    """
    Represent a dictionary in object form.  Recursive.

    Allows:

    >>> test_dict = {"a":{"b":1,"ugly var!":2}, "c":3}
    >>> test_obj = DictObj(**test_dict)
    >>> print(test_obj.a.b)
    1
    >>> print(test_obj.a.ugly_var_)
    2
    >>> print(test_obj)
    {'a': {'b': 1, 'ugly_var_': 2}, 'c': 3}
    >>> print(test_obj.dict()) # "ugly var!" is back
    {'a': {'b': 1, 'ugly var!': 2}, 'c': 3}
    """

    def __init__(self, **attrs):
        for key in attrs:
            newkey = re.sub(r'[^a-zA-Z0-9_]', '_', key)
            value = attrs[key]
            if isinstance(value, dict):
                value = DictObj(**value)
            setattr(self, newkey, value)
            if newkey != key:
                setattr(self, '..old_key..' + newkey, key)

    def dict(self):
        """Return original dictionary form"""
        rewrite = {}
        exported = {}
        for key in self.__dict__:
            if key[:11] == "..old_key..":
                rewrite[key[11:]] = self.__dict__[key]
            else:
                value = self.__dict__[key]
                if isinstance(value, DictObj):
                    value = value.dict()
                exported[key] = value
        for key in rewrite:
            exported[rewrite[key]] = exported[key]
            del exported[key]

        return exported

    def __repr__(self):
        return str(self.__repr__r())

    def __repr__r(self):
        exported = {}
        for key in self.__dict__:
            if key[:11] != "..old_key..":
                value = self.__dict__[key]
                if isinstance(value, DictObj):
                    value = value.__repr__r()
                exported[key] = value
        return exported

    def __iter__(self):
        return iter(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def copy(self):
        """Make a copy"""
        return copy.deepcopy(self.__dict__)

