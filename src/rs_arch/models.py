"""Core data structures describing archaeology objects."""

from collections import defaultdict
from dataclasses import dataclass
from typing import NamedTuple, Sequence


@dataclass(frozen=True)
class Material:
    """An individual type of material used in archaeology."""
    name: str


class MaterialAmount(NamedTuple):
    """A material and an associated quantity."""
    material: Material
    amount: int


@dataclass(init=False)
class Artefact:
    """A damaged artefact in archaeology that requires materials to restore."""
    name: str
    required_materials: list[MaterialAmount]

    def __init__(self, name: str,
                 required_materials: Sequence[tuple[Material, int]]) -> None:
        self.name = name
        self.required_materials = [
            MaterialAmount(*t) for t in required_materials
        ]

    @property
    def material_names(self) -> list[str]:
        """Names of all materials required to restore this artefact."""
        return [
            material_req.material.name
            for material_req in self.required_materials
        ]


@dataclass
class Collection:
    """A collection of artefacts to donate."""
    name: str
    artefacts: list[Artefact]

    @property
    def artefact_names(self) -> list[str]:
        """Names of all artefacts required for this collection."""
        return [artefact.name for artefact in self.artefacts]

    def get_all_materials_required(self) -> list[MaterialAmount]:
        """
        Get a list of all materials required and their corresponding quantities
        to restore all artefacts in this collection.
        """
        materials: dict[Material, int] = defaultdict(int)
        for artefact in self.artefacts:
            for material, amount in artefact.required_materials:
                materials[material] += amount
        return [MaterialAmount(*kv) for kv in materials.items()]
