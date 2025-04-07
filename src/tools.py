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



# kwarg_profile format:
# - 'mandatory': List of mandatory parameter names (strings).
# - 'optional': List of optional parameters, which can either be:
#     - Strings (parameter names), or
#     - Dictionaries with 'param' (parameter name) and optionally 'default' (default value).
# - 'exclusive': List of exclusive parameter groups. Each group is a list of dictionaries with:
#     - 'param' (parameter name),
#     - 'mandatory' (True/False indicating if the parameter is mandatory),
#     - 'default' (optional default value if 'mandatory' is False).
# The function ensures that the provided arguments adhere to the defined profile.

# Example:
# @validate_kwargs_ext({
#     'mandatory': ['param1', 'param2'],
#     'optional': [
#         'param3', 
#         {'param': 'param4', 'default': 'default_value'}
#     ],
#     'exclusive': [
#         [{'param': 'param5', 'mandatory': True}, {'param': 'param6', 'mandatory': True}],
#         [{'param': 'param7', 'mandatory': False, 'default': 'default_param7'}, {'param': 'param8', 'mandatory': True}]
#     ]
# })
# In this example:
# - 'param1' and 'param2' are mandatory.
# - 'param3' is optional.
# - 'param4' is optional with a default value of 'default_value'.
# - 'param5' and 'param6' must both be provided together (exclusive group).
# # - 'param7' is optional with a default value and 'param8' is mandatory in another exclusive group.
# def validate_kwargs_ext(kwarg_profile):          # list of expected profiles for kwargs
#     def decorator(fct):
#         def inner(*args,**kwargs):
#             mandatory = set(kwarg_profile.get('mandatory', []))
#             optional = {x['param'] if isinstance(x, dict) else x for x in kwarg_profile.get('optional', [])}
#             exclusive = [{x['param'] for x in group} for group in kwarg_profile.get('exclusive', [])]
#             conflict_mandatory_optional = mandatory & optional
#             if conflict_mandatory_optional: raise Exception(f"Validator arguments conflict: mandatory / optional: {conflict_mandatory_optional}")
#             conflict_mandatory_exclusive = set.union(*exclusive) & mandatory
#             if conflict_mandatory_exclusive: raise Exception(f"Validator arguments conflict: mandatory / exclusive: {conflict_mandatory_exclusive}")
#             conflict_optional_exclusive = set.union(*exclusive) & optional
#             if conflict_optional_exclusive: raise Exception(f"Validator arguments conflict: optional / exclusive: {conflict_optional_exclusive}")

#             all_profile = list(mandatory | optional | set().union(*exclusive))
#             unknown_keys = set(kwargs.keys()) - set(all_profile)
#             if unknown_keys: raise Exception(f"Unknown argument(s): {', '.join(unknown_keys)}")

#             if kwarg_profile.get('mandatory'):
#                 missing = set(kwarg_profile['mandatory']) - kwargs.keys()
#                 if missing: raise Exception(f"Missing mandatory argument(s): {', '.join(missing)}")

#             for param in (p for p in kwarg_profile.get('optional', []) if isinstance(p, dict)):
#                 param_name = param['param']
#                 if param_name not in kwargs and 'default' in param:
#                     kwargs[param_name] = param.get('default')                    

#             exclusive_profiles = kwarg_profile.get('exclusive', [])
#             valid_profiles = [] 

#             all_mandatory_and_optional = {p['param'] if isinstance(p, dict) else p for p in kwarg_profile.get('mandatory', [])} | {p['param'] if isinstance(p, dict) else p for p in kwarg_profile.get('optional', [])}

#             for profile in exclusive_profiles:
#                 profile_params = {p['param'] for p in profile}
#                 provided_params = set(kwargs.keys())

#                 exclusive_params = provided_params - all_mandatory_and_optional
#                 if not exclusive_params.issubset(profile_params): continue
#                 missing = {p['param'] for p in profile if p.get('mandatory', False)} - provided_params
#                 if missing: continue
#                 valid_profiles.append(profile)

#             if len(valid_profiles) > 1: raise Exception(f"Conflicting exclusive profiles: {len(valid_profiles)} profiles match the provided arguments.")
#             if len(valid_profiles) == 0: raise Exception(f"Arguments do not match any exclusive profile: {kwargs.keys()}")

#             for param in valid_profiles[0]:
#                 if param['param'] not in kwargs and not param.get('mandatory', False) and 'default' in param:
#                     kwargs[param['param']] = param['default']

#             return fct(*args,**kwargs)
#         return inner
#     return decorator






# kwarg_profile format:
# - 'mandatory': List of mandatory parameter names (strings).
# - 'optional': List of optional parameters, which can either be:
#     - Strings (parameter names), or
#     - Dictionaries with 'name' (parameter name) and optionally 'default' (default value).
# - 'exclusive': List of exclusive parameter groups. Each group is a list of dictionaries with:
#     - 'name' (parameter name),
#     - 'mandatory' (True/False indicating if the parameter is mandatory),
#     - 'default' (optional default value if 'mandatory' is False).
# The function ensures that the provided arguments adhere to one of the defined profile.

# Example:
# @validate_kwargs_ext({
#     'mandatory': ['param1', 'param2'],
#     'optional': [
#         'param3', 
#         {'name': 'param4', 'default': 'default_value'}
#     ],
#     'exclusive': [
#         [{'name': 'param5', 'mandatory': True}, {'name': 'param6', 'mandatory': True}],
#         [{'name': 'param7', 'mandatory': False, 'default': 'default_param7'}, {'name': 'param8', 'mandatory': True}]
#     ]
# })
# In this example:
# - 'param1' and 'param2' are mandatory.
# - 'param3' is optional.
# - 'param4' is optional with a default value of 'default_value'.
# - 'param5' and 'param6' must both be provided together (exclusive group).
# - 'param7' is optional with a default value and 'param8' is mandatory in another exclusive group.
def validate_kwargs_ext(kwarg_profile):          
    def decorator(fct):
        def inner(*args, **kwargs):
            mandatory = set(kwarg_profile.get('mandatory', []))
            optional = {x['name'] if isinstance(x, dict) else x for x in kwarg_profile.get('optional', [])}
            exclusive = [{x['name'] for x in group} for group in kwarg_profile.get('exclusive', [])]
            conflict_mandatory_optional = mandatory & optional
            if conflict_mandatory_optional:
                raise Exception(f"Validator arguments conflict: mandatory / optional: {conflict_mandatory_optional}")
            conflict_mandatory_exclusive = set.union(*exclusive) & mandatory
            if conflict_mandatory_exclusive:
                raise Exception(f"Validator arguments conflict: mandatory / exclusive: {conflict_mandatory_exclusive}")
            conflict_optional_exclusive = set.union(*exclusive) & optional
            if conflict_optional_exclusive:
                raise Exception(f"Validator arguments conflict: optional / exclusive: {conflict_optional_exclusive}")
            for i, profile in enumerate(exclusive):
                for j, other_profile in enumerate(exclusive):
                    if i != j and profile.issubset(other_profile):
                        raise Exception(f"Exclusive profile {profile} is included in {other_profile}, which is redundant.")

            all_profile = list(mandatory | optional | set().union(*exclusive))
            unknown_keys = set(kwargs.keys()) - set(all_profile)
            if unknown_keys:
                raise Exception(f"Unknown argument(s): {', '.join(unknown_keys)}")

            if kwarg_profile.get('mandatory'):
                missing = set(kwarg_profile['mandatory']) - kwargs.keys()
                if missing:
                    raise Exception(f"Missing mandatory argument(s): {', '.join(missing)}")

            for param in (p for p in kwarg_profile.get('optional', []) if isinstance(p, dict)):
                param_name = param['name']
                if param_name not in kwargs and 'default' in param:
                    kwargs[param_name] = param.get('default')

            exclusive_profiles = kwarg_profile.get('exclusive', [])
            valid_profiles = []

            all_mandatory_and_optional = {p['name'] if isinstance(p, dict) else p for p in kwarg_profile.get('mandatory', [])} | {p['name'] if isinstance(p, dict) else p for p in kwarg_profile.get('optional', [])}

            for profile in exclusive_profiles:
                profile_params = {p['name'] for p in profile}
                provided_params = set(kwargs.keys())

                exclusive_params = provided_params - all_mandatory_and_optional
                if not exclusive_params.issubset(profile_params):
                    continue
                missing = {p['name'] for p in profile if p.get('mandatory', False)} - provided_params
                if missing:
                    continue
                valid_profiles.append(profile)

            if len(valid_profiles) > 1:
                raise Exception(f"Conflicting exclusive profiles: {len(valid_profiles)} profiles match the provided arguments.")
            if len(valid_profiles) == 0:
                raise Exception(f"Arguments do not match any exclusive profile: {kwargs.keys()}")

            for param in valid_profiles[0]:
                if param['name'] not in kwargs and not param.get('mandatory', False) and 'default' in param:
                    kwargs[param['name']] = param['default']

            return fct(*args, **kwargs)
        return inner
    return decorator


