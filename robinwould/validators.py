"""Module that contains the field validators"""

from typing import Callable, Dict, Type
from robinwould.interfaces import Field


validators_dict: Dict[Type[Field], Callable[[Field], None]]
