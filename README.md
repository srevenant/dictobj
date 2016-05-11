Represent a dictionary in object form.  Recursive, robust.

Not python zen because it provides an alternate way to use dictionaries.
But I'm okay with this, becuase it is handy.

Limitations:

   * raises error if there is a name conflict with reserved words
   * reserves the prefix \f$\f for internal use (also raises error)
   * because of namespace conflict problems, this is a deal breaker
     for universal use--you must be cautious on what keys are input.

There are more elegant implementations to do similar things, but this
has better functionality and is more robust, imho.

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

