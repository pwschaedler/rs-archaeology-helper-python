from dataclasses import dataclass


@dataclass
class Material:
    """An individual type of material used in archaeology."""

    name: str
    location: str | None = None

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class MaterialAmount:
    """A material and its associated quantity."""

    material: Material
    quantity: int
