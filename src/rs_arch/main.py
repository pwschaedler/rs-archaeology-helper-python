"""RuneScape Archaeology helper to track goals and materials needed to restore artefacts."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, NamedTuple, TypeAlias

MaterialQuantity: TypeAlias = tuple[str, int]


class Material(NamedTuple):
    """A single material used to restore artefacts."""

    name: str


class Artefact(NamedTuple):
    """An artefact and the materials needed to restore it."""

    name: str
    required_materials: set[MaterialQuantity]


class Collection(NamedTuple):
    """A collection of artefacts."""

    name: str
    artefacts: set[str]


class KnowledgeBase:
    """Knowledge base to store and query information about collections and
    artefacts.

    Functionality acts as a global database.
    """

    materials: dict[str, Material] = {}
    artefacts: dict[str, Artefact] = {}
    collections: dict[str, Collection] = {}

    @classmethod
    def add_material(cls, material_name: str) -> None:
        """Add a material to the knowledge base."""
        cls.materials[material_name] = Material(material_name)

    @classmethod
    def add_artefact(
        cls, artefact_name: str, required_materials: set[MaterialQuantity]
    ) -> None:
        """Add an artefact to the knowledge base."""
        cls.artefacts[artefact_name] = Artefact(artefact_name, required_materials)

    @classmethod
    def add_collection(cls, collection_name: str, artefacts: set[str]) -> None:
        """Add a collection to the knowledge base."""
        cls.collections[collection_name] = Collection(collection_name, artefacts)

    @classmethod
    def get_material(cls, material_name: str) -> Material | None:
        """Get a material by name."""
        return cls.materials.get(material_name)

    @classmethod
    def get_artefact(cls, artefact_name: str) -> Artefact | None:
        """Get an artefact by name."""
        return cls.artefacts.get(artefact_name)

    @classmethod
    def get_collection(cls, collection_name: str) -> Collection | None:
        """Get a collection by name."""
        return cls.collections.get(collection_name)

    @classmethod
    def clear(cls) -> None:
        """Clear the knowledge base."""
        cls.materials = {}
        cls.artefacts = {}
        cls.collections = {}

    @classmethod
    def save(cls, filename: str) -> None:
        """Save the knowledge base to file as JSON. Everything is sorted for reproducibility."""
        data: dict[str, Any] = {}

        data['materials'] = sorted([material[0] for material in cls.materials.values()])
        data['artefacts'] = sorted(
            [
                {
                    'name': artefact.name,
                    'required_materials': sorted(list(artefact.required_materials)),
                }
                for artefact in cls.artefacts.values()
            ],
            key=lambda item: item['name'],
        )
        data['collections'] = sorted(
            [
                {
                    'name': collection.name,
                    'artefacts': sorted(list(collection.artefacts)),
                }
                for collection in cls.collections.values()
            ],
            key=lambda item: item['name'],
        )

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, filename: str) -> None:
        """Load knowledge base from JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for material in data['materials']:
            cls.add_material(material)
        for artefact in data['artefacts']:
            cls.add_artefact(
                artefact['name'],
                set((req[0], req[1]) for req in artefact['required_materials']),
            )
        for collection in data['collections']:
            cls.add_collection(collection['name'], set(collection['artefacts']))


class Goal:
    """Represents a goal of artefact restorations to achieve."""

    def __init__(self) -> None:
        self.artefacts: dict[str, int] = defaultdict(int)

    def add_artefact(self, artefact_name: str) -> None:
        """Add an artefact to the goal."""
        self.artefacts[artefact_name] += 1

    def add_collection(self, collection_name: str) -> None:
        """Add all artefacts in a collection to the goal."""
        collection = KnowledgeBase.get_collection(collection_name)
        if collection is None:
            raise ValueError(f'Collection "{collection_name}" does not exist.')
        for artefact in collection.artefacts:
            self.add_artefact(artefact)

    def get_artefacts(self) -> set[tuple[str, int]]:
        """Get all artefacts in the goal."""
        return set(self.artefacts.items())

    def get_materials_needed(
        self, material_storage: MaterialStorage | None = None
    ) -> set[MaterialQuantity]:
        """Get all materials needed to achieve the goal."""
        materials_needed: dict[str, int] = defaultdict(int)

        # Get all materials needed from goals
        for artefact_name, artefact_quantity in self.artefacts.items():
            artefact = KnowledgeBase.get_artefact(artefact_name)
            if artefact is None:
                raise ValueError(f'Artefact "{artefact_name}" does not exist.')
            for material_name, material_quantity in artefact.required_materials:
                materials_needed[material_name] += material_quantity * artefact_quantity

        # Take out what we have in material storage
        if material_storage is not None:
            for material_name, material_quantity in material_storage.get_materials():
                materials_needed[material_name] -= material_quantity

        # Remove materials with counts <= 0
        materials_needed = {
            name: quantity
            for name, quantity in materials_needed.items()
            if quantity > 0
        }

        return set(materials_needed.items())


class MaterialStorage:
    """Represents a player's material storage."""

    def __init__(self, initial_materials: set[MaterialQuantity] | None = None) -> None:
        if initial_materials is None:
            initial_materials = set()
        self.storage: dict[str, int] = defaultdict(int, initial_materials)

    def add(self, name: str, quantity: int) -> None:
        """Add a single material to the storage."""
        self.storage[name] += quantity

    def add_batch(self, materials: set[MaterialQuantity]) -> None:
        """Add multiple materials to the storage."""
        for name, quantity in materials:
            self.storage[name] += quantity

    def get_materials(self) -> set[MaterialQuantity]:
        """Get the current material storage contents."""
        return set(self.storage.items())
