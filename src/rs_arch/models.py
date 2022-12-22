"""Core data structures describing archaeology objects."""

from collections import defaultdict
from typing import NamedTuple


class Material(NamedTuple):
    """An individual type of material used in archaeology."""

    name: str


class MaterialAmount(NamedTuple):
    """A material and an associated quantity."""

    material: Material
    amount: int


class Artefact(NamedTuple):
    """A damaged artefact in archaeology that requires materials to restore."""

    name: str
    required_materials: list[MaterialAmount]

    @property
    def material_names(self) -> list[str]:
        """Names of all materials required to restore this artefact."""
        return [material_req.material.name for material_req in self.required_materials]


class Collection(NamedTuple):
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
