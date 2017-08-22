# Usage: python archi-excel-to-xml.py <excel-input-path> <xml-output-path>

import sys
import xml.etree.ElementTree as ET
import pandas as pd

ns = {
	'': 'http://www.opengroup.org/xsd/archimate/3.0/',
	'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
	'xml': 'http://www.w3.org/XML/1998/namespace'
}

for prefix in ns.keys():
	ET.register_namespace(prefix, ns[prefix])

def makecurie(ns, prefix, localname):
	return "{%s}%s" % (ns[prefix], localname)

xsischemalocation = makecurie(ns, 'xsi', 'schemaLocation')
xsitype = makecurie(ns, 'xsi', 'type')
xmllang = makecurie(ns, 'xml', 'lang')

# Return the number of rows in a pandas DataFrame.
def numrows(df): return df.shape[0]

# Create 'is_..._item' functions for categorising model elements.
business_types = [
	'BusinessActor',
	'BusinessRole',
	'BusinessCollaboration',
	'BusinessInterface',
	'BusinessProcess',
	'BusinessFunction',
	'BusinessInteraction',
	'BusinessEvent',
	'BusinessService',
	'BusinessObject',
	'Contract',
	'Representation',
	'Product'
]
def is_business_item(type): return type in business_types

application_types = [
	'ApplicationComponent',
	'ApplicationCollaboration',
	'ApplicationInterface',
	'ApplicationFunction',
	'ApplicationInteraction',
	'ApplicationProcess',
	'ApplicationEvent',
	'ApplicationService',
	'DataObject'
]
def is_application_item(type): return type in application_types

technology_types = [
	'Node',
	'Device',
	'SystemSoftware',
	'TechnologyCollaboration',
	'TechnologyInterface',
	'Path',
	'CommunicationNetwork',
	'TechnologyFunction',
	'TechnologyProcess',
	'TechnologyInteraction',
	'TechnologyEvent',
	'TechnologyService',
	'Artifact'
]
def is_technology_item(type): return type in technology_types

physical_types = [
	'Equipment',
	'Facility',
	'DistributionNetwork',
	'Material'
]
def is_physical_item(type): return type in physical_types

motivation_types = [
	'Stakeholder',
	'Driver',
	'Assessment',
	'Goal',
	'Outcome',
	'Principle',
	'Requirement',
	'Constraint',
	'Meaning',
	'Value'
]
def is_motivation_item(type): return type in motivation_types

strategy_types = [
	'Resource',
	'Capability',
	'CourseOfAction'
]
def is_strategy_item(type): return type in strategy_types

implementation_types = [
	'WorkPackage',
	'Deliverable',
	'ImplementationEvent',
	'Plateau',
	'Gap'
]
def is_implementation_item(type): return type in implementation_types

def is_other_item(type):
	return not (
		is_business_item(type)
		or is_application_item(type)
		or is_technology_item(type)
		or is_physical_item(type)
		or is_motivation_item(type)
		or is_strategy_item(type)
		or is_implementation_item(type)
	)

# Read the file paths from the command-line.
excelInputPath = sys.argv[1]
xmlOutputPath = sys.argv[2]

# Read the data from the Excel file
reader = pd.ExcelFile(excelInputPath)
metadatadf = reader.parse("metadata")
elementsdf = reader.parse("elements")
relationshipsdf = reader.parse("relationships")

# Contruct output XML
root = ET.Element(
	makecurie(ns, '', 'model'),
	attrib={
		xsischemalocation: 'http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.0/archimate3_Diagram.xsd',
		'identifier': metadatadf['model_identifier'][0]
	}
)

name = ET.SubElement(
	root,
	makecurie(ns, '', 'name'),
	attrib={ xmllang: 'en' }
)
name.text = metadatadf['model_name'][0]

# Write 'element' elements.
elements = ET.SubElement(
	root,
	makecurie(ns, '', 'elements')
)
elementtag = makecurie(ns, '', 'element')
nametag = makecurie(ns, '', 'name')
documentationtag = makecurie(ns, '', 'documentation')
elementcount = numrows(elementsdf)
for elementidx in range(0, elementcount):
	element = ET.SubElement(
		elements,
		elementtag,
		attrib={
			'identifier': elementsdf['element_identifier'][elementidx],
			xsitype: elementsdf['element_type'][elementidx]
		}
	)
	elementname = ET.SubElement(
		element,
		nametag,
		attrib={ xmllang: 'en' }
	)
	elementname.text = elementsdf['element_name'][elementidx]
	documentationtext = elementsdf['element_documentation'][elementidx]
	if (not pd.isnull(documentationtext)):
		elementdocumentation = ET.SubElement(
			element,
			documentationtag,
			attrib={ xmllang: 'en' }
		)
		elementdocumentation.text = documentationtext.replace("\r\n", "\n")

# Write 'relationship' elements.
relationships = ET.SubElement(
	root,
	makecurie(ns, '', 'relationships')
)
relationshiptag = makecurie(ns, '', 'relationship')
relationshipcount = numrows(relationshipsdf)
for relationshipidx in range(0, relationshipcount):
	relationship = ET.SubElement(
		relationships,
		relationshiptag,
		attrib={
			'identifier': relationshipsdf['relationship_identifier'][relationshipidx],
			'source': relationshipsdf['relationship_source_identifier'][relationshipidx],
			'target': relationshipsdf['relationship_target_identifier'][relationshipidx],
			xsitype: relationshipsdf['relationship_type'][relationshipidx]
		}
	)

# Write 'organization' and 'item' elements.
organizations = ET.SubElement(
	root,
	makecurie(ns, '', 'organizations')
)
itemtag = makecurie(ns, '', 'item')
labeltag = makecurie(ns, '', 'label')

def write_organization_items(organizations_root, label, is_category_item):
	parentitem = ET.SubElement(
		organizations_root,
		itemtag
	)
	parentitemlabel = ET.SubElement(
		parentitem,
		labeltag,
		attrib={ xmllang: 'en' }
	)
	parentitemlabel.text = label

	for elementidx in range(0, elementcount):
		if (is_category_item(elementsdf['element_type'][elementidx])):
			item = ET.SubElement(
				parentitem,
				itemtag,
				{ 'identifierRef': elementsdf['element_identifier'][elementidx]}
			)
write_organization_items(organizations, 'Strategy', is_strategy_item)
write_organization_items(organizations, 'Business', is_business_item)
write_organization_items(organizations, 'Application', is_application_item)
write_organization_items(organizations, 'Technology & Physical', is_technology_item)
write_organization_items(organizations, 'Motivation', is_motivation_item)
write_organization_items(organizations, 'Implementation & Migration', is_implementation_item)
write_organization_items(organizations, 'Other', is_other_item)

# Write relationship items.
relationshipsitem = ET.SubElement(
	organizations,
	itemtag
)
relationshipsitemlabel = ET.SubElement(
	relationshipsitem,
	labeltag,
	attrib={ xmllang: 'en' }
)
relationshipsitemlabel.text = 'Relations'

for relationshipidx in range(0, relationshipcount):
	item = ET.SubElement(
		relationshipsitem,
		itemtag,
		{ 'identifierRef': relationshipsdf['relationship_identifier'][relationshipidx]}
	)

# Note: this script does not write view items.

# Save XML
ET.ElementTree(root).write(xmlOutputPath, encoding="UTF-8", xml_declaration=True)
