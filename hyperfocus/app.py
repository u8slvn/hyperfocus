# import functools
# import sys
# from pathlib import Path
#
# import click
# import typer
#
# from hyperfocus import __app_name__
# from hyperfocus.exceptions import HyperfocusException
#
#
# def app_error_handler(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except HyperfocusException as error:
#             typer.secho(str(error), fg=typer.colors.RED)
#             raise typer.Exit(1)
#         except typer.Exit as error:
#             sys.exit(error.exit_code)
#         except Exception as error:
#             typer.secho(str(error), fg=typer.colors.RED)
#             raise typer.Exit(1)
#
#     return wrapper
#
