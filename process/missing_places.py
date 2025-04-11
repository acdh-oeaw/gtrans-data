import os

from lxml import etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid, check_for_hash, normalize_string


listplace_xml = os.path.join("data", "indices", "listplace.xml")
listplace_doc = TeiReader(listplace_xml)

listperson_xml = os.path.join("data", "indices", "listperson.xml")
listperson_doc = TeiReader(listperson_xml)

places_places = set()
for x in listplace_doc.any_xpath(".//tei:place[@xml:id]"):
    places_places.add(get_xmlid(x))

print(len(places_places))

places_persons = set()
for x in listperson_doc.any_xpath(".//tei:placeName[@key]"):
    places_persons.add(check_for_hash(x.attrib["key"]))

missing_places = places_persons - places_places
print(f"{len(missing_places)} missing places")


to_create = {}
for x in listperson_doc.any_xpath(".//tei:placeName[@key]"):
    xml_id = check_for_hash(x.attrib["key"])
    if xml_id in places_places:
        print(xml_id)
        continue
    else:
        to_create[xml_id] = normalize_string(x.text)


listplace_node = listplace_doc.any_xpath(".//tei:listPlace")[0]

for key, value in to_create.items():
    place = ET.Element(
        "{http://www.tei-c.org/ns/1.0}place",
        attrib={"{http://www.w3.org/XML/1998/namespace}id": key},
    )
    place_name = ET.Element(
        "{http://www.tei-c.org/ns/1.0}placeName", attrib={"key": value}
    )
    place_name.text = value
    place.append(place_name)
    listplace_node.append(place)
listplace_doc.tree_to_file(listplace_xml)
