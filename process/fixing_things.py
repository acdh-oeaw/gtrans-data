import os

from acdh_tei_pyutils.tei import TeiReader
from acdh_xml_pyutils.xml import NSMAP

from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

file = os.path.join("data", "indices", "listperson.xml")

doc = TeiReader(file)
for x in doc.any_xpath(".//tei:person[@xml:id]"):
    for y in x.xpath(".//tei:idno", namespaces=NSMAP):
        text = y.text
        text = text.split(";")[0]
        text = text.split()[0]
        text = get_normalized_uri(text)
        y.text = text
doc.tree_to_file(file)
