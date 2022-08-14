"""Tests for instantiating and basic usage of model classes."""

from rs_arch.models import Artefact, Collection, Material


def test_create_arterfact() -> None:
    """Test creating an artefact with a few materials."""
    bronze = Material('Warforged bronze')
    bone = Material('Fossilised bone')
    mark = Material('Mark of the Kyzaj')
    axe = Artefact('Ogre Kyzaj axe', [(bronze, 28), (mark, 20), (bone, 24)])

    assert axe.required_materials[0].material.name == 'Warforged bronze'
    assert axe.required_materials[2].amount == 24
    assert set(axe.material_names) == set(
        ['Warforged bronze', 'Fossilised bone', 'Mark of the Kyzaj']
    )


def test_create_collection() -> None:
    """Test creating a collection with artefacts."""
    bronze = Material('Warforged bronze')
    bone = Material('Fossilised bone')
    mark = Material('Mark of the Kyzaj')
    sword = Artefact('Ork cleaver sword', [(bronze, 36), (bone, 36)])
    axe = Artefact('Ogre Kyzaj axe', [(bronze, 28), (mark, 20), (bone, 24)])
    coll = Collection('Red Rum Relics I/2', [sword, axe])

    assert coll.artefacts[0].name == 'Ork cleaver sword'
    assert coll.artefacts[1].required_materials[1].material.name == 'Mark of the Kyzaj'
    assert set(coll.artefact_names) == set(['Ork cleaver sword', 'Ogre Kyzaj axe'])


def test_collection_materials() -> None:
    """Test getting all materials needed for a collection."""
    bronze = Material('Warforged bronze')
    bone = Material('Fossilised bone')
    mark = Material('Mark of the Kyzaj')
    sword = Artefact('Ork cleaver sword', [(bronze, 36), (bone, 36)])
    axe = Artefact('Ogre Kyzaj axe', [(bronze, 28), (mark, 20), (bone, 24)])
    coll = Collection('Red Rum Relics I/2', [sword, axe])

    expected_materials = [(bronze, 64), (bone, 60), (mark, 20)]
    assert set(coll.get_all_materials_required()) == set(expected_materials)
