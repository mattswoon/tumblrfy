OPERATIONS = {}
DESCRIPTIONS = {}

def op(op_name='', description=''):
    def decorator(func):
        def new_op(*args, **kwargs):
            return func(*args, **kwargs)

        OPERATIONS[op_name] = new_op
        DESCRIPTIONS[op_name] = description
        return new_op

    return decorator
