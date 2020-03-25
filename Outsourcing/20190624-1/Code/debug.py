# -*- encode: utf-8 -*-
from IPython import embed

from color import color


def debug(locals_=None):
    for k,v in locals_.items():
        locals()[k] = v
    print("\n\n\n")
    hint = "`Enter` if not debug: "
    if input(color(hint, "蓝")):
        del k, v, locals_, hint
        embed(colors="Neutral")
