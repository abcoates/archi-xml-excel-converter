# Usage: python archi-xml-to-excel.py <xml-input-path> <excel-output-path>

import sys
import xml.etree.ElementTree as ET
import pandas as pd

ns = {
	'm': 'http://www.opengroup.org/xsd/archimate/3.0/',
	'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
	'xml': 'http://www.w3.org/XML/1998/namespace'
}

def makecurie(ns, prefix, localname):
	return "{%s}%s" % (ns[prefix], localname)

def elemtext(e):
	return e.text if e is not None else ''

xsitype = makecurie(ns, 'xsi', 'type')

# Read the file stem(s) from the command-line.
xmlInputPath = sys.argv[1]
excelOutputPath = sys.argv[2]

# Read input XML file.
tree = ET.parse(xmlInputPath)
root = tree.getroot()

# Create output Excel file.
writer = pd.ExcelWriter(excelOutputPath)

# Write out model-level metadata sheet.
metadatacolumns = ['model_name', 'model_identifier']
metadatadf = pd.DataFrame({
	'model_name': [ elemtext(root.find('m:name', ns)) ],
	'model_identifier': [ root.attrib['identifier'] ]
})
metadatadf.to_excel(writer, sheet_name='metadata', columns=metadatacolumns, index=False)

# Write out element properties sheet.
elementcolumns = ['element_type', 'element_name', 'element_documentation', 'element_identifier']
elements = root.findall('m:elements/m:element', ns)
elementsdf = pd.DataFrame({
	'element_type': list(map(lambda e: e.attrib[xsitype], elements)),
	'element_name': list(map(lambda e: elemtext(e.find('m:name',ns)), elements)),
	'element_documentation': list(map(lambda e: elemtext(e.find('m:documentation',ns)), elements)),
	'element_identifier': list(map(lambda e: e.attrib['identifier'], elements))
})
elementsdf.to_excel(writer, sheet_name='elements', columns=elementcolumns, index=False)

# Write out relationship properties sheet.
relationshipcolumns = ['relationship_type', 'relationship_identifier', 'relationship_source_identifier', 'relationship_target_identifier']
relationships = root.findall('m:relationships/m:relationship', ns)
relationshipsdf = pd.DataFrame({
	'relationship_type': list(map(lambda e: e.attrib[xsitype], relationships)),
	'relationship_identifier': list(map(lambda e: e.attrib['identifier'], relationships)),
	'relationship_source_identifier': list(map(lambda e: e.attrib['source'], relationships)),
	'relationship_target_identifier': list(map(lambda e: e.attrib['target'], relationships))
})
relationshipsdf.to_excel(writer, sheet_name='relationships', columns=relationshipcolumns, index=False)

# Save and close the Excel file.
writer.save()
writer.close()
