import glob

from lxml import etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import make_entity_label
from acdh_tei_pyutils.utils import get_xmlid


listplace = {}
listorg = {}
listperson = {}
keywords = {}
for x in glob.glob("./data/editions/*xml"):
    doc = TeiReader(x)
    for y in doc.any_xpath(".//tei:keywords"):
        keywords[y.text] = y.text
    for y in doc.any_xpath(".//tei:person[@xml:id]"):
        label = make_entity_label(y.xpath("./*[1]")[0])[0]
        y.xpath("./*[1]")[0].attrib["key"] = label
        listperson[get_xmlid(y)] = y
    for y in doc.any_xpath(".//tei:place[@xml:id]"):
        label = make_entity_label(y.xpath("./*[1]")[0])[0]
        y.xpath("./*[1]")[0].attrib["key"] = label
        listplace[get_xmlid(y)] = y
    for y in doc.any_xpath(".//tei:org[@xml:id]"):
        label = make_entity_label(y.xpath("./*[1]")[0])[0]
        y.xpath("./*[1]")[0].attrib["key"] = label
        listorg[get_xmlid(y)] = y
    doc.tree_to_file(x)

dummy = """
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title type="main"/>
            <title type="sub">Die Große Transformation</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body/>
  </text>
</TEI>

"""

doc = TeiReader(dummy)
doc.any_xpath(".//tei:title[@type='main']")[0].text = "Personenregister"
body = doc.any_xpath(".//tei:body")[0]
cur_list = ET.Element("{http://www.tei-c.org/ns/1.0}listPerson")
body.append(cur_list)
for key, value in listperson.items():
    cur_list.append(value)
doc.tree_to_file("data/indices/listperson.xml")

doc = TeiReader(dummy)
doc.any_xpath(".//tei:title[@type='main']")[0].text = "Ortsregister"
body = doc.any_xpath(".//tei:body")[0]
cur_list = ET.Element("{http://www.tei-c.org/ns/1.0}listPlace")
body.append(cur_list)
for key, value in listplace.items():
    cur_list.append(value)
doc.tree_to_file("data/indices/listplace.xml")

doc = TeiReader(dummy)
doc.any_xpath(".//tei:title[@type='main']")[0].text = "Institutionsregister"
body = doc.any_xpath(".//tei:body")[0]
cur_list = ET.Element("{http://www.tei-c.org/ns/1.0}listOrg")
body.append(cur_list)
for key, value in listorg.items():
    cur_list.append(value)
doc.tree_to_file("data/indices/listorg.xml")
