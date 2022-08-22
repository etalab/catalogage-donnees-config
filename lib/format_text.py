from functools import partial

import click

format_error_message = partial(click.style, fg="red", bold=True)
format_success_message = partial(click.style, fg="bright_green", bold=True)
