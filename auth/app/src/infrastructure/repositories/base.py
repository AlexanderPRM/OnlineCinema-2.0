"""Module with base code for all Repositories."""


def decorate_all_methods(decorator, *args, **kwargs):
    """Decorate all methods.

    Args:
        decorator (def): Decorator to be applied.
        args: Optional arguments for decorator.
        kwargs: Optional key value arguments for decorator.

    Returns:
        wrapper (def): Function which decorate.
    """
    def wrapper(cls):
        """Decorate all methods in class.

        Args:
            cls (class): Class for decorate.

        Returns:
            cls (class): Return class with decorated methods.
        """
        for attr_name, attr_value in cls.__dict__.items():
            if (  # noqa: WPS337 (Multiple condition, but it's a best solve)
                callable(attr_value)
                and not attr_name.startswith('__')
                and not attr_name.startswith('_')
            ):
                setattr(cls, attr_name, decorator(*args, **kwargs)(attr_value))
        return cls
    return wrapper
