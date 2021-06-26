# -*- coding: utf-8 -*-
"""handlers
   Implements the handlers for errors.
"""
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Show this page when user enter wrong url
    Args:
        error (object): Error
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    """Show this page when server have internal error
    Args:
        error (object): Error
    """
    return render_template('errors/500.html'), 500
