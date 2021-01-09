__all__ = ('APIHooker', 'form', 'Config')


import functools
import json
import re
import textwrap

from typing import Iterable

from flask import render_template, request, redirect


class APIHooker:
    def __init__(self, app):
        self._app = app
        self._apis = dict()

    def run(self, **kwargs):
        @self._app.route('/')
        def index():
            return render_template('index.html', data=self._apis)

        self._app.run(**kwargs)

    def add(self, api, name, description, arguments, post=str):
        '''
        Argument:
            api: Callable
            name: str, api name
            description: str, api description
            arguments: dict, {argument: (function, kwargs)}
            post: Callable, post-processing
        '''
        self._apis[name] = textwrap.dedent(description)

        @self._app.route(f'/api/{name}', endpoint=f'_{name}')
        def _():
            return redirect(f'/api/{name}/x')

        @self._app.route(f'/api/{name}/x', endpoint=f'_{name}_x')
        def x():
            return render_template(
                'x.html', data=arguments, name=name, description=self._apis[name],
            )

        @self._app.route(f'/api/{name}/y', methods=['POST', 'GET'], endpoint=f'_{name}_y')
        def y():
            if request.method == 'POST':
                return post(api(**form.post(request.form, arguments)))
            else:
                return redirect(f'/api/{name}/x')

        return self


def indent(string, prefix=' '*4):
    return textwrap.indent(string, prefix)


def p(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return '<p>\n{}\n</p>'.format(indent(func(*args, **kwargs)))
    return wrapper


class form:
    @classmethod
    @p
    def text(cls, name:str) -> str:
        return f'{name}: <input type="text" name="{name}" />'

    @classmethod
    @p
    def date(cls, name:str) -> str:
        return f'{name}: <input type="date" name="{name}" />'

    @classmethod
    @p
    def month(cls, name:str) -> str:
        return f'{name}: <input type="month" name="{name}" />'

    @classmethod
    @p
    def range(cls, name:str, min:int, max:int, step:[int, float]=1, default:int=None) -> str:
        default = default or min
        return f'{name}: \n<input type="range" name="{name}" ' \
            f'value="{default}" min="{min}" max="{max}" step="{step}" ' \
            'oninput="this.nextElementSibling.value=this.value" />\n' \
            f'<output>{default}</output>'

    @classmethod
    @p
    def datalist(cls, name:str, options:[dict, Iterable]) -> str:
        string = '\n'.join(
            f'<option value="{value}">{text}</option>'
            for value, text in (
                options.items() if isinstance(options, dict) else
                map(lambda x: (x, x), options)
            )
        )
        return f'{name}: \n<input list="{name}-datalist" name="{name}">\n' \
            f'<datalist id="{name}-datalist">\n' \
            f'{indent(string)}\n' \
            '</datalist>'

    @classmethod
    @p
    def group(cls, name:str, options:dict) -> str:
        '''
        Argument:
            - options: {group: {name: description} or (name, )}
        '''
        string = '\n'.join(
            f'<optgroup label="{group}">\n' + indent('\n'.join(
                f'<option value="{value}">{text}</option>'
                for value, text in (
                    values.items() if isinstance(values, dict) else
                    map(lambda x: (x, x), values)
                )
            )) + '\n</optgroup>'
            for group, values in options.items()
        )
        return f'{name}: \n<select name="{name}">\n{indent(string)}\n</select>'

    @classmethod
    @p
    def checkbox(cls, name:str, options:[dict, Iterable]) -> str:
        return f'{name}: \n' + '\n'.join(
            f'<input type="checkbox" name="{name}.{ith}" value="{value}">{text}</input>'
            for ith, (value, text) in enumerate(
                options.items() if isinstance(options, dict) else
                map(lambda x: (x, x), options)
            )
        )

    @classmethod
    @p
    def multiple(cls, name:str, options:[dict, Iterable]) -> str:
        string = '\n'.join(
            f'<option value="{value}">{text}</option>'
            for value, text in (
                options.items() if isinstance(options, dict) else
                map(lambda x: (x, x), options)
            )
        )
        return f'{name}: \n<select name="{name}" multiple>\n{indent(string)}\n</select>'

    @classmethod
    @p
    def radio(cls, name:str, options:[dict, Iterable]) -> str:
        return f'{name}: ' + '\n'.join(
            f'<input type="radio" name="{name}" value="{value}">{text}</input>'
            for value, text in (
                options.items() if isinstance(options, dict) else
                map(lambda x: (x, x), options)
            )
        )

    @classmethod
    def boolean(cls, name:str) -> str:
        return cls.radio(name, {'_': 'True', '': 'False'})

    @classmethod
    def post(cls, x, arguments):
        '''Post-processing

        Argument:
            - x: dict
            - arguments: dict, {name: (function, kwargs)}
        '''
        y = dict()
        for name, (function, kwargs) in arguments.items():
            if function in (cls.text, cls.datalist, cls.radio, cls.date, cls.month, cls.group):
                y[name] = x[name]
            elif function in (cls.range, cls.boolean):
                Ts = {
                    cls.range: type(kwargs.get('step', 1)), cls.boolean: bool,
                }
                y[name] = Ts[function](x[name])
            elif function == cls.multiple:
                y[name] = x.getlist(name)
            elif function == cls.checkbox:
                pattern = re.compile(fr'^{name}\.\d+$')
                y[name] = tuple(
                    value for key, value in x.items()
                    if pattern.match(key)
                )
        return y


class Config:
    def __init__(self, filename='config.json', encoding='utf-8'):
        with open(filename, 'r', encoding=encoding) as f:
            self._data = json.load(f)

    def __getitem__(self, key):
        return self._data.get(key, None)

    @property
    def data(self):
        return self._data
