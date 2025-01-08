def validate_kwargs(kwarg_profile):          # list of expected profiles for kwargs
    def decorator(fct):
        def inner(*args,**kwargs):
            if 'mandatory' in kwarg_profile and kwarg_profile['mandatory'] is not None:
                for item in kwarg_profile['mandatory']:
                    if item not in kwargs.keys(): raise Exception("Missing mandatory argument : "+str(item))
            if 'exclusive' in kwarg_profile and kwarg_profile['exclusive'] is not None:
                found = None
                for item in kwarg_profile['exclusive']:
                    if set(item) <= set(kwargs.keys()):
                        if found is not None: raise Exception("Exclusive arguments conflict : "+str(item)+" and "+str(found))
                        found = item
            return fct(*args,**kwargs)
        return inner
    return decorator
