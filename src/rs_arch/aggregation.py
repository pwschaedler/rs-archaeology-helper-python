from typing import Iterable

from rs_arch.models.artefact import Artefact
from rs_arch.models.material import Material, MaterialAmount


def aggregate_materials_over_artefacts(
    artefacts: Iterable[Artefact]
) -> list[MaterialAmount]:
    """
    Given a list of artefacts, aggregate a list of material requirements such
    that artefacts requiring a common material will be combined into a single
    requirement.
    """
    requirements: dict[Material, int] = {}

    for artefact in artefacts:
        for material_req in artefact.requirements:
            material = material_req.material
            if material not in requirements:
                requirements[material] = 0
            requirements[material] += material_req.quantity

    return [MaterialAmount(*requirement) for requirement in requirements.items()]
