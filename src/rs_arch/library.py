from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any
from rs_arch.models.artefact import Artefact
from rs_arch.models.collection import Collection
from rs_arch.models.material import Material, MaterialAmount


class Library(ABC):
    """Data store and central knowledge base of known objects."""

    def __init__(self):
        self.artefacts: dict[str, Artefact] = {}
        self.collections: dict[str, Collection] = {}
        self.materials: dict[str, Material] = {}

    @abstractmethod
    def commit(self) -> None:
        """Commit the library to persistent storage."""
        ...

    @abstractmethod
    def load(self) -> None:
        """Load the library from persistent storage."""
        ...

    def add_artefact(self, artefact: Artefact) -> None:
        """Add an artefact to the library."""
        if artefact.name not in self.artefacts:
            self.artefacts[artefact.name] = artefact
        for material_req in artefact.requirements:
            self.add_material(material_req.material)

    def add_collection(self, collection: Collection) -> None:
        """Add a collection to the library."""
        if collection.name not in self.collections:
            self.collections[collection.name] = collection
        for artefact in collection.artefacts:
            self.add_artefact(artefact)

    def add_material(self, material: Material) -> None:
        """Add a material to the library."""
        if material.name not in self.materials:
            self.materials[material.name] = material

    def get_artefact(self, artefact_name: str) -> Artefact:
        """Get an artefact by name from the library."""
        return self.artefacts[artefact_name]

    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection by name from the library."""
        return self.collections[collection_name]

    def get_material(self, material_name: str) -> Material:
        """Get a material by name from the library."""
        return self.materials[material_name]


class JSONLibrary(Library):
    """Program library stored as a JSON file on disk."""

    def __init__(self, fpath: Path):
        super().__init__()
        self.fpath = fpath

    def commit(self) -> None:
        data = {
            'artefacts': [
                self._artefact_as_dict(artefact) for artefact in self.artefacts.values()
            ],
            'collections': [
                self._collection_as_dict(collection)
                for collection in self.collections.values()
            ],
            'materials': [
                self._material_as_dict(material) for material in self.materials.values()
            ],
        }

        with self.fpath.open('w', encoding='utf-8') as f:
            json.dump(obj=data, fp=f, indent=4)

    def load(self) -> None:
        """Load the store from file."""
        with self.fpath.open('r', encoding='utf-8') as f:
            data = json.load(f)

        for material in data['materials']:
            self.add_material(self._material_from_dict(material))
        for artefact in data['artefacts']:
            self.add_artefact(self._artefact_from_dict(artefact))
        for collection in data['collections']:
            self.add_collection(self._collection_from_dict(collection))

    def _artefact_as_dict(self, artefact: Artefact) -> dict[str, Any]:
        """Convert an artefact to a dictionary representation for JSON output."""
        return {
            'name': artefact.name,
            'requirements': [
                {
                    'material': requirement.material.name,
                    'quantity': requirement.quantity,
                }
                for requirement in artefact.requirements
            ],
        }

    def _collection_as_dict(self, collection: Collection) -> dict[str, Any]:
        """Convert a collection to a dictionary representation for JSON output."""
        return {
            'name': collection.name,
            'artefacts': [artefact.name for artefact in collection.artefacts],
        }

    def _material_as_dict(self, material: Material) -> dict[str, Any]:
        """Convert a material to a dictionary representation for JSON output."""
        return {'name': material.name, 'location': material.location}

    def _artefact_from_dict(self, artefact_data: dict[str, Any]) -> Artefact:
        """Convert artefact data from JSON to an object instance."""
        return Artefact(
            name=artefact_data['name'],
            requirements=[
                MaterialAmount(
                    material=self.get_material(requirement['material']),
                    quantity=requirement['quantity'],
                )
                for requirement in artefact_data['requirements']
            ],
        )

    def _collection_from_dict(self, collection_data: dict[str, Any]) -> Collection:
        """Convert collection data from JSON to an object instance."""
        return Collection(
            name=collection_data['name'],
            artefacts=[
                self.get_artefact(artefact) for artefact in collection_data['artefacts']
            ],
        )

    def _material_from_dict(self, material_data: dict[str, Any]) -> Material:
        """Convert material data from JSON to an object instance."""
        return Material(**material_data)
