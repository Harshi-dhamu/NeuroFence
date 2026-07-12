"""
utils.py

Shared helper utilities.
"""


def module_name(module):
    """
    Return module class name.

    Parameters
    ----------
    module

    Returns
    -------
    str
    """
    return module.__class__.__name__