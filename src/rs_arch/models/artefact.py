from dataclasses import dataclass

from rs_arch.models.material import MaterialAmount


@dataclass
class Artefact:
    """A damaged artefact in archaeology that requires materials to restore."""

    name: str
    requirements: list[MaterialAmount]
