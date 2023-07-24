import param

class function1(param.ParameterizedFunction):
    some_param = param.Integer(1)

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)
        return {"key": p.some_param}

class function2(param.ParameterizedFunction):

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)
        return f"first key: {list(function1().values())[0]}"
