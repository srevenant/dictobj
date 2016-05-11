Represent a dictionary in object form.  Recursive.

Allows:

    >>> test_dict = {"a":{"b":1,"ugly var!":2}, "c":3}
    >>> test_obj = DictObj(**test_dict)
    >>> test_obj.a.b
    1
    >>> test_obj.a.ugly_var_
    2
	>>> test_obj.a['ugly var!']
    2
	>>> test_obj.get('c')
    3
    >>> test_obj # shows expanded form
    {'a': {'b': 1, 'ugly_var_': 2, 'ugly var!': 2}, 'c': 3}
    >>> test_obj.dict() # back to original form
    {'a': {'b': 1, 'ugly var!': 2}, 'c': 3}

