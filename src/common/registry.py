"""A tiny generic registry mapping ``name -> callable``.

Each experiment axis (chunkers, retrievers, prompts) owns one instance. Strategies
register by decorator; callers select by name. Users can register their own
strategy from a notebook cell without touching the package:

    from chunking import CHUNKERS

    @CHUNKERS.register("my_chunker")
    def my_chunker(text, *, source, **params):
        ...

This module is fully implemented — it is the wiring the rest of the template
plugs into.
"""

from __future__ import annotations

from typing import Callable, Dict, Generic, Iterable, TypeVar

T = TypeVar("T", bound=Callable)


class Registry(Generic[T]):
    def __init__(self, kind: str) -> None:
        self.kind = kind
        self._items: Dict[str, T] = {}

    def register(self, name: str) -> Callable[[T], T]:
        """Decorator that registers ``fn`` under ``name``."""

        def deco(fn: T) -> T:
            if name in self._items:
                raise ValueError(f"{self.kind} strategy {name!r} already registered")
            self._items[name] = fn
            return fn

        return deco

    def get(self, name: str) -> T:
        try:
            return self._items[name]
        except KeyError:
            raise KeyError(
                f"unknown {self.kind} strategy {name!r}; available: {self.names()}"
            ) from None

    def names(self) -> list[str]:
        return sorted(self._items)

    def items(self) -> Iterable[tuple[str, T]]:
        return self._items.items()

    def __contains__(self, name: str) -> bool:
        return name in self._items
