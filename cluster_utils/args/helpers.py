from typing import Iterable, Dict, List, DefaultDict, TypeVar, cast, Any, ItemsView
import itertools as it
from collections import defaultdict
import attr

from .arg_types import Arg

T = TypeVar("T")
C = TypeVar("C", bound=Arg[Any])


def group_by_type(items: Iterable[T]) -> Dict[type, List[T]]:
    groupedDict = cast(DefaultDict[type, List[T]], defaultdict(list))
    for key, value in it.groupby(items, type):
        groupedDict[key] += list(value)
    return groupedDict


def get_arg_list(models: object):
    if hasattr(models, "__attrs_attrs__"):
        return [
            cast(Arg[Any], arg.setid(name)) for name, arg in attr.asdict(models, recurse=False).items()
        ]
    elif isinstance(models, dict):
        return [
            arg.setid(name) for name, arg in cast(ItemsView[str, Arg[Any]], models.items() )
        ]
    else:
        raise Exception(f"{type(models)} is not a supported object for arg models")


def update_model(arg_updates: Iterable[Arg[Any]], model: T) -> T:
    update = { 
        arg.id: arg for arg in arg_updates
    }
    return model.__class__(**update)