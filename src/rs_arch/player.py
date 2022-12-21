"""Data structures and functions representing the player character state."""

from collections import UserDict
from dataclasses import dataclass

from rs_arch.models import Material


class MaterialStorage(UserDict[Material, int]):
    """
    All materials the player has and their quantities.

    Implementation note: In the models, material amounts are represented as a
    list of tuples because they're likely to be iterated over and processed as a
    set. I imagine the material storage here will act more as a lookup of
    specific materials, so I made it a dict instead.
    """

    def __getitem__(self, key: Material | str) -> int:
        if isinstance(key, str):
            key = Material(key)
        return self.data[key]

    def __setitem__(self, key: Material | str, value: int) -> None:
        if isinstance(key, str):
            key = Material(key)
        self.data[key] = value


@dataclass
class Player:
    """The state of the player."""

    material_storage: MaterialStorage
    porter_charges: int
