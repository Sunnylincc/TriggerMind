"""A tiny offline-compatible subset of Typer used by this project.

This fallback exists so the project can run in restricted environments.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable, Optional, get_type_hints

import click

BadParameter = click.BadParameter


@dataclass
class ParameterInfo:
    default: Any
    param_decls: tuple[str, ...]
    help: str | None = None
    is_option: bool = False


def Argument(default: Any = ..., help: str | None = None) -> ParameterInfo:
    return ParameterInfo(default=default, param_decls=(), help=help, is_option=False)


def Option(default: Any = None, *param_decls: str, help: str | None = None) -> ParameterInfo:
    return ParameterInfo(default=default, param_decls=param_decls, help=help, is_option=True)


class Typer:
    def __init__(self, *, help: str | None = None, no_args_is_help: bool = False, rich_markup_mode: str | None = None) -> None:
        self.group = click.Group(help=help, invoke_without_command=False)
        self._no_args_is_help = no_args_is_help

    def command(self, name: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            cmd = _click_command_from_callable(func, name=name)
            self.group.add_command(cmd)
            return func

        return decorator

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.group(*args, **kwargs)

    @property
    def name(self) -> str | None:
        return self.group.name

    def main(self, *args: Any, **kwargs: Any) -> Any:
        return self.group.main(*args, **kwargs)

    def __getattr__(self, item: str) -> Any:
        return getattr(self.group, item)



def _click_command_from_callable(func: Callable[..., Any], name: Optional[str] = None) -> click.Command:
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    cmd_func: Callable[..., Any] = func

    for param in reversed(sig.parameters.values()):
        default = param.default
        annotation = type_hints.get(param.name, str)

        if isinstance(default, ParameterInfo):
            info = default
            if info.is_option:
                param_names = info.param_decls or (f"--{param.name.replace('_', '-')}",)
                cmd_func = click.option(*param_names, param.name, default=info.default, show_default=True, help=info.help, type=annotation)(cmd_func)
            else:
                required = info.default is ...
                default_val = None if required else info.default
                cmd_func = click.argument(param.name, required=required, type=annotation, default=default_val)(cmd_func)
        else:
            if default is inspect._empty:
                cmd_func = click.argument(param.name, required=True, type=annotation)(cmd_func)
            else:
                cmd_func = click.option(f"--{param.name.replace('_', '-')}", param.name, default=default, show_default=True, type=annotation)(cmd_func)

    return click.command(name=name or func.__name__.replace("_", "-"))(cmd_func)
