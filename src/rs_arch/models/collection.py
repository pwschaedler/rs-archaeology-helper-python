from dataclasses import dataclass

from rs_arch import aggregation
from rs_arch.models.artefact import Artefact
from rs_arch.models.material import MaterialAmount


@dataclass
class Collection:
    """A collection of artefacts to donate."""

    name: str
    artefacts: list[Artefact]

    @property
    def material_requirements(self) -> list[MaterialAmount]:
        """Material requirements for the whole collection."""
        return aggregation.aggregate_materials_over_artefacts(self.artefacts)
