#! /usr/bin/env python

import click
import os
import logging
import sys

plugin_folder = os.path.join(os.path.dirname(__file__), 'subcommands')

class MyCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            ns = {}
            fn = os.path.join(plugin_folder, name + '.py')
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['cli']
        except Exception as err:
            logging.error(err)

@click.command(cls=MyCLI)
def cli():
    '''Command-line tool for ease the execution of batch jobs with Spark.'''
    pass

def main(**kwargs):
    try:
        sys.tracebacklimit = 0 #Evitamos xerar demasiado ruido na saída dos erros quitando o traceback
        cli(**kwargs)
    except KeyboardInterrupt:
        logging.error("""
WARNING: execution interrupted by the user!
""")
    except Exception as err:
        logging.error(f"{err}")
        return 1


if __name__ == "__main__":
    main()