import os
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from lxml import etree

listperson = os.path.join("data", "indices", "listperson.xml")
df = pd.read_csv("gtrans-personen-csv.csv")
doc = TeiReader(listperson)
id_to_gnd = dict(zip(df["id"], df["gnd"]))
print(len(id_to_gnd))

for x in doc.any_xpath(".//tei:person"):
    xmlid = get_xmlid(x)
    if xmlid in id_to_gnd:
        gnd = id_to_gnd[xmlid]
        if pd.notna(gnd):
            gnd_url = f"https://d-nb.info/gnd/{gnd}"
            try:
                existing_idno = x.xpath("./tei:idno", namespaces=doc.nsmap)[0]
                existing_idno.text = gnd_url
            except IndexError:
                existing_idno = etree.SubElement(x, f"{{{doc.nsmap['tei']}}}idno")
                existing_idno.text = gnd_url

doc.tree_to_file(listperson)
