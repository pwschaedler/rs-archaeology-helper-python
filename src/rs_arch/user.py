from dataclasses import dataclass, field
from rs_arch.models.artefact import Artefact
from rs_arch.models.material import Material, MaterialAmount


@dataclass
class User:
    """Represents a user, their porter status, and their goals."""

    artefacts_to_restore: list[Artefact] = field(default_factory=list)
    material_storage: dict[str, MaterialAmount] = field(default_factory=dict)
    porter: int = 0

    def update_material_storage(self, material: Material, quantity: int):
        """Update material storage with a new value for a material."""
        self.material_storage[material.name] = MaterialAmount(material, quantity)
