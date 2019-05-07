import datetime

import requests
from bs4 import BeautifulSoup

URLS = {
    "schemes": "https://app.bto.org/euringcodes/schemes.jsp?check1=Y&check2=Y&check3=Y&check4=Y&orderBy=SCHEME_CODE",
    "species": "https://app.bto.org/euringcodes/species.jsp",
    "countries": "https://app.bto.org/euringcodes/place.jsp?inactive=on",
    "circumstances": "https://app.bto.org/euringcodes/circumstances.jsp",
}

SCHEME_FIELDS = [
    ["code", "string"],
    ["country", "string"],
    ["ringing_centre", "string"],
    ["is_euring", "bool"],
    ["is_current", "bool"],
    ["updated", "date"],
    ["notes", "string"],
]

SPECIES_FIELDS = [
    ["code", "string"],
    ["name", "string"],
    ["updated", "date"],
    ["notes", "string"],
]

COUNTRY_FIELDS = [
    ["code", "string"],
    ["region", "string"],
    ["place_code", "string"],
    ["is_current", "bool"],
    ["notes", "string"],
    ["updated", "date"],
]

CIRCUMSTANCES_FIELDS = [
    ["code", "string"],
    ["name", "string"],
    ["description", "string"],
    ["updated", "date"],
]


def _field_value(cell, field_type):
    if field_type == "bool":
        return bool(cell.find("img", alt="Y"))
    content = cell.string or ""
    content = content.replace("\xad", "")
    if field_type == "string":
        return content.strip()
    if field_type == "date":
        parts = content.strip()
        if parts:
            parts = parts.split("/")
            day = int(parts[2])
            month = int(parts[1])
            year = int(parts[0]) + 2000
            if year > datetime.date.today().year:
                year -= 100
            return datetime.date(year, month, day)
        return None
    raise ValueError(f"Parameter `field_type` should be `string`, '`date`, or `bool`.")


def _record(cells, fields):
    data = {}
    for index, field in enumerate(fields):
        data[field[0]] = _field_value(cells[index], field[1])
    return data


def _fetch(url, fields):
    response = requests.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, features="html.parser")
    table = soup.find("div", id="divAll")
    result = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) == len(fields):
            result.append(_record(cells, fields))
    return result


def fetch_schemes():
    return _fetch(URLS["schemes"], SCHEME_FIELDS)


def fetch_species():
    return _fetch(URLS["species"], SPECIES_FIELDS)


def fetch_countries():
    return _fetch(URLS["countries"], COUNTRY_FIELDS)


def fetch_circumstances():
    return _fetch(URLS["circumstances"], CIRCUMSTANCES_FIELDS)
