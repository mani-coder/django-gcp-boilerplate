# Standard Library Imports
import logging
import time
import traceback
from functools import wraps
from inspect import getcallargs


def _log_start(log_level, func, *func_args, **func_kwargs):
    try:
        func_module, func_name = func.__module__, func.__name__
        params = getcallargs(func, *func_args, **func_kwargs)
        logger = logging.getLogger(func_module)
        logger.log(
            log_level,
            "{}.{} is invoked with params - {}".format(
                func_module, func_name, ", ".join("{}={}".format(field, param) for (field, param) in params.items())
            ),
        )
    except Exception:
        pass


def _log_finish(log_level, func, result):
    try:
        func_module, func_name = func.__module__, func.__name__
        logger = logging.getLogger(func_module)
        logger.log(log_level, "{}.{} completed successfully. Result: {}".format(func_module, func_name, result))
    except Exception:
        pass


def log_call_invocation_only(log_level=logging.INFO):
    """
    Log the function invocation call along with it's parameters as key value pairs.
    """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*func_args, **func_kwargs):
            _log_start(log_level, func, *func_args, **func_kwargs)
            return func(*func_args, **func_kwargs)

        return inner_wrapper

    return wrapper


def log_call(log_level=logging.INFO):
    """
    Log the function call along with it's parameters as key value pairs. This also logs the result at the end of
    the successful function call completion.
    """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*func_args, **func_kwargs):
            start_time = time.time()
            _log_start(log_level, func, *func_args, **func_kwargs)
            result = func(*func_args, **func_kwargs)
            end_time = time.time()
            duration = end_time - start_time
            _log_finish(log_level, func, result, duration)

            return result

        return inner_wrapper

    return wrapper


def fail_safe(log_level=logging.CRITICAL):
    """
    Handle the exception if any raised from this function gracefully.
    """

    def wrapper(func):
        @wraps(func)
        def fail_safe_wrapper(*func_args, **func_kwargs):
            func_module, func_name = func.__module__, func.__name__
            try:
                return func(*func_args, **func_kwargs)
            except Exception:
                call_args = getcallargs(func, *func_args, **func_kwargs)
                params = ", ".join("{}={}".format(field, param) for (field, param) in call_args.items())

                logger = logging.getLogger(func_module)
                parent_stack_trace = get_stack_trace()

                # sys.exc_info will return only the traceback starting from the top of this decorator, so adding the
                # parent stacktrace in the extra.
                logger.log(
                    log_level,
                    f"Error while executing {func_module}.{func_name}, parentStack: {parent_stack_trace}, params: {params}",
                )

        return fail_safe_wrapper

    return wrapper


def get_stack_trace() -> str:
    """
    Get the current stack trace as a string. Used for logging purposes.
    """
    stack = traceback.extract_stack()
    return "".join(traceback.format_list(stack)) if stack else "couldn't retrieve a valid stack!"
