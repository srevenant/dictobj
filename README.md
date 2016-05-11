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

