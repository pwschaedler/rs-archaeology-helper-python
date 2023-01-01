"""
Web scraping utilities to get collection, artefact, and material information
from the RS Wiki.
"""

from typing import Iterator

import requests
from bs4 import BeautifulSoup, Tag

from rs_arch.main import KnowledgeBase as kb


def get_collections() -> Iterator[tuple[str, str]]:
    """
    Get a list of all archaeology collections. Return as an iterator of (name,
    link to wiki page) tuples.
    """
    collections_url = 'https://runescape.wiki/w/Archaeology_collections'
    rs_wiki_root = 'https://runescape.wiki'
    name_col_idx = 1

    collections_html = requests.get(collections_url, timeout=30).text
    parser = BeautifulSoup(collections_html, 'html.parser')
    table = parser.find('table')
    assert isinstance(table, Tag)

    # Skip the header row
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        name = cols[name_col_idx].get_text(strip=True)
        link = rs_wiki_root + cols[name_col_idx].find('a')['href']
        yield (name, link)


def get_collection_information(collection_name: str, collection_link: str) -> None:
    """Get all artefacts and required material quantities for a collection."""
    name_col_idx = 0
    materials_col_idx = 5

    collection_html = requests.get(collection_link, timeout=30).text
    parser = BeautifulSoup(collection_html, 'html.parser')

    # Skip the first table, which is the page infobox
    table = parser.find_all('table')[1]
    artefacts: set[str] = set()

    # Skip header and sum rows
    for row in table.find_all('tr')[1:-1]:
        cols = row.find_all('td')
        artefact_name = cols[name_col_idx].get_text(strip=True)
        material_col = str(cols[materials_col_idx])
        required_materials = extract_material_information(material_col)
        kb.add_artefact(artefact_name, set(required_materials))
        artefacts.add(artefact_name)

    kb.add_collection(collection_name, set(artefacts))


def extract_material_information(material_col_html: str) -> list[tuple[str, int]]:
    """Extract information about materials from column."""
    required_materials: list[tuple[str, int]] = []
    material_lines = material_col_html.split('<br/>')

    # Skip the first material, which is the damaged artefact
    for material_line in material_lines[1:]:
        material_text = BeautifulSoup(material_line, 'html.parser').get_text()
        quantity, material = material_text.split(' × ')
        kb.add_material(material)
        required_materials.append((material, int(quantity)))

    return required_materials


def scrape_wiki_collections() -> int:
    """Scrape RS Wiki for information about collections and add to a databse."""
    for name, link in get_collections():
        get_collection_information(name, link)
    kb.save('kb.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(scrape_wiki_collections())
