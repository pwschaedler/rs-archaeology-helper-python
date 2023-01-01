"""Tests for the main functionality of the package."""

from typing import Generator

import pytest

from rs_arch import main as rs


@pytest.fixture
def setup_saradominist_iii() -> Generator[None, None, None]:
    """Setup sample collection in knowledge base."""
    kb = rs.KnowledgeBase

    kb.add_material('White marble')
    kb.add_material('Leather scraps')
    kb.add_material('Keramos')
    kb.add_material('Goldrune')
    kb.add_material('Star of Saradomin')
    kb.add_material('Clockwork')
    kb.add_material('Third Age iron')
    kb.add_material('Everlight silvthril')

    kb.add_artefact(
        'Dominarian device',
        {
            ('Everlight silvthril', 30),
            ('Keramos', 22),
            ('Third Age iron', 22),
            ('Clockwork', 1),
        },
    )
    kb.add_artefact(
        'Fishing trident',
        {
            ('Star of Saradomin', 22),
            ('Third Age iron', 30),
            ('Goldrune', 22),
        },
    )
    kb.add_artefact(
        'Amphora',
        {('Everlight silvthril', 34), ('Keramos', 46)},
    )
    kb.add_artefact(
        'Rod of Asclepius',
        {
            ('White marble', 30),
            ('Star of Saradomin', 24),
            ('Goldrune', 26),
        },
    )
    kb.add_artefact(
        'Kopis dagger',
        {('Everlight silvthril', 50), ('Leather scraps', 42)},
    )
    kb.add_artefact(
        'Xiphos short sword',
        {('Everlight silvthril', 46), ('Leather scraps', 46)},
    )

    kb.add_collection(
        'Saradominist III',
        {
            'Dominarian device',
            'Fishing trident',
            'Amphora',
            'Rod of Asclepius',
            'Kopis dagger',
            'Xiphos short sword',
        },
    )

    yield


@pytest.fixture(autouse=True)
def teardown_kb() -> Generator[None, None, None]:
    """Reset knowledge base global data."""
    yield
    rs.KnowledgeBase.clear()


def test_kb_get_material_nonexistent() -> None:
    """Test that non-existent materials return None."""
    kb = rs.KnowledgeBase
    assert kb.get_material('asdf') is None


def test_kb_get_artefact_nonexistent() -> None:
    """Test that non-existent artefacts return None."""
    kb = rs.KnowledgeBase
    assert kb.get_artefact('asdf') is None


def test_kb_get_collection_nonexistent() -> None:
    """Test that non-extistent collections return None."""
    kb = rs.KnowledgeBase
    assert kb.get_collection('asdf') is None


def test_kb_add_material() -> None:
    """Test adding a material to the knowledge base."""
    kb = rs.KnowledgeBase
    kb.add_material('Everlight silvthril')
    material = kb.get_material('Everlight silvthril')
    assert material is not None
    assert material.name == 'Everlight silvthril'


def test_kb_add_artefact() -> None:
    """Test adding an artefact to the knowledge base."""
    kb = rs.KnowledgeBase
    kb.add_artefact(
        'Dominarian device',
        {
            ('Everlight silvthril', 30),
            ('Keramos', 22),
            ('Third Age iron', 22),
            ('Clockwork', 1),
        },
    )
    artefact = kb.get_artefact('Dominarian device')
    assert artefact is not None
    assert artefact.name == 'Dominarian device'
    assert artefact.required_materials == {
        ('Everlight silvthril', 30),
        ('Keramos', 22),
        ('Third Age iron', 22),
        ('Clockwork', 1),
    }


def test_kb_add_collection() -> None:
    """Test adding a collection to the knowledge base."""
    kb = rs.KnowledgeBase
    kb.add_collection(
        'Saradominist III',
        {
            'Dominarian device',
            'Fishing trident',
            'Amphora',
            'Rod of Asclepius',
            'Kopis dagger',
            'Xiphos short sword',
        },
    )
    collection = kb.get_collection('Saradominist III')
    assert collection is not None
    assert collection.name == 'Saradominist III'
    assert collection.artefacts == {
        'Dominarian device',
        'Fishing trident',
        'Amphora',
        'Rod of Asclepius',
        'Kopis dagger',
        'Xiphos short sword',
    }


def test_kb_global_behavior() -> None:
    """Test that the knowledge base acts as a global singleton."""
    kb1 = rs.KnowledgeBase
    kb2 = rs.KnowledgeBase
    kb1.add_material('Everlight silvthril')
    material = kb2.get_material('Everlight silvthril')
    assert material is not None
    kb1.clear()
    assert kb2.get_material('Everlight silvthril') is None


def test_material_storage_get_materials() -> None:
    """Test getting materials from material storage."""
    storage = rs.MaterialStorage({('Everlight silvthril', 100), ('Goldrune', 100)})
    materials = storage.get_materials()
    assert materials == {('Everlight silvthril', 100), ('Goldrune', 100)}


def test_material_storage_add_single_material() -> None:
    """Test adding materials to material storage after initialization."""
    storage = rs.MaterialStorage()
    storage.add('Everlight silvthril', 100)
    materials = storage.get_materials()
    assert materials == {('Everlight silvthril', 100)}


def test_material_storage_add_batch_materials() -> None:
    """Test adding multiple materials to storage."""
    storage = rs.MaterialStorage()
    storage.add_batch({('Everlight silvthril', 100), ('Goldrune', 100)})
    materials = storage.get_materials()
    assert materials == {('Everlight silvthril', 100), ('Goldrune', 100)}


def test_goal_get_artefacts_from_artefacts() -> None:
    """Test adding individual artefacts to goal."""
    goal = rs.Goal()
    goal.add_artefact('Dominarian device')
    goal_artefacts = goal.get_artefacts()
    assert goal_artefacts == {('Dominarian device', 1)}


@pytest.mark.usefixtures('setup_saradominist_iii')
def test_goal_get_goal_artefacts_from_collection() -> None:
    """Test adding an entire collection to goal."""
    goal = rs.Goal()
    goal.add_collection('Saradominist III')
    goal_artefacts = goal.get_artefacts()
    assert goal_artefacts == {
        ('Dominarian device', 1),
        ('Fishing trident', 1),
        ('Amphora', 1),
        ('Rod of Asclepius', 1),
        ('Kopis dagger', 1),
        ('Xiphos short sword', 1),
    }


@pytest.mark.usefixtures('setup_saradominist_iii')
def test_goal_get_goal_artefacts_from_mix() -> None:
    """Test adding individual artefacts and whole collections to goal."""
    goal = rs.Goal()
    goal.add_collection('Saradominist III')
    goal.add_artefact('Dominarian device')
    goal_artefacts = goal.get_artefacts()
    assert goal_artefacts == {
        ('Dominarian device', 2),
        ('Fishing trident', 1),
        ('Amphora', 1),
        ('Rod of Asclepius', 1),
        ('Kopis dagger', 1),
        ('Xiphos short sword', 1),
    }


@pytest.mark.usefixtures('setup_saradominist_iii')
def test_goal_get_materials_needed_no_storage() -> None:
    """Test getting needed materials for goal with no prior material storage."""
    goal = rs.Goal()
    goal.add_collection('Saradominist III')
    materials_needed = goal.get_materials_needed()
    assert materials_needed == {
        ('White marble', 30),
        ('Leather scraps', 88),
        ('Keramos', 68),
        ('Goldrune', 48),
        ('Star of Saradomin', 46),
        ('Clockwork', 1),
        ('Third Age iron', 52),
        ('Everlight silvthril', 160),
    }


@pytest.mark.usefixtures('setup_saradominist_iii')
def test_goal_get_materials_needed_with_storage() -> None:
    """Test getting needed materials for goal with existing material storage."""
    goal = rs.Goal()
    goal.add_collection('Saradominist III')

    materials = rs.MaterialStorage({('Everlight silvthril', 100), ('Goldrune', 100)})

    materials_needed = goal.get_materials_needed(materials)
    assert materials_needed == {
        ('White marble', 30),
        ('Leather scraps', 88),
        ('Keramos', 68),
        ('Star of Saradomin', 46),
        ('Clockwork', 1),
        ('Third Age iron', 52),
        ('Everlight silvthril', 60),
    }
