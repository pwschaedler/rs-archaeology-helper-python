from pathlib import Path
from rs_arch.models.artefact import Artefact
from rs_arch.models.collection import Collection
from rs_arch.models.material import Material, MaterialAmount
from rs_arch.library import JSONLibrary


MAIN_MENU = '''
[1] Add material
[2] Add artefact
[3] Material info
[4] Artefact info
[5] Exit
'''.strip()


def cli():
    """The main command line interface."""
    debug_populate_library()


def debug_populate_library():
    lib = JSONLibrary(Path('./data.json'))
    lib.add_collection(
        Collection(
            'Red Rum Relics I',
            [
                Artefact(
                    'Ork cleaver sword',
                    [
                        MaterialAmount(Material('Warforged bronze'), 36),
                        MaterialAmount(Material('Fossilised bone'), 36),
                    ],
                ),
                Artefact(
                    'Ogre Kyzaj axe',
                    [
                        MaterialAmount(Material('Warforged bronze'), 28),
                        MaterialAmount(Material('Mark of the Kyzaj'), 20),
                        MaterialAmount(Material('Fossilised bone'), 24),
                    ],
                ),
                Artefact(
                    'Beastkeeper helm',
                    [
                        MaterialAmount(Material('Warforged bronze'), 16),
                        MaterialAmount(Material('Vulcanised rubber'), 24),
                        MaterialAmount(Material('Animal furs'), 20),
                        MaterialAmount(Material('Fossilised bone'), 24),
                    ],
                ),
                Artefact(
                    "'Nosorog!' sculpture",
                    [
                        MaterialAmount(Material("Yu'biusk clay"), 30),
                        MaterialAmount(Material('Malachite green'), 24),
                        MaterialAmount(Material('Warforged bronze'), 30),
                    ],
                ),
            ],
        )
    )
    lib.commit()

    lib.load()
    print(lib.get_collection('Red Rum Relics I'))
