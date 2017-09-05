# Usage: python archi-xml-to-markdown.py <xml-input-path> <markdown-output-path>

import sys
import re
import xml.etree.ElementTree as ET

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

camelCaseRegex = re.compile(r"([a-z])([A-Z])")

def escapetext(text):
	return text.replace("\n", "<br>").replace("\r", "")

# Read the file paths from the command-line.
xmlInputPath = sys.argv[1]
mdOutputPath = sys.argv[2]

# Read input XML file.
tree = ET.parse(xmlInputPath)
root = tree.getroot()

# Create output Markdown file.
with open(mdOutputPath, mode='w', encoding='utf-8') as mdout:

	# Write out model-level metadata.
	mdout.writelines([
		"# **Archimate Model Facts**\n",
		"| Property | Value |\n",
		"| ---- | ---- |\n",
		"| **Model Name** | {0} |\n".format(elemtext(root.find('m:name', ns))),
		"| **Model ID** | {0} |\n".format(root.attrib['identifier']),
		"\n"
	])

	# Write out element properties.
	elements = root.findall('m:elements/m:element', ns)
	for element in elements:
		elemtype = camelCaseRegex.sub(r"\1 \2", element.attrib[xsitype])
		elemid = element.attrib['identifier']
		mdout.writelines([
			"## <a name='{0}'></a>{1}: {2}\n".format(elemid, elemtype, elemtext(element.find('m:name',ns))),
			"| Property | Value |\n",
			"| ---- | ---- |\n",
			"| **Name** | {0} |\n".format(elemtext(element.find('m:name',ns))),
			"| **Type** | {0} |\n".format(elemtype),
			"| **Documentation** | {0} |\n".format(escapetext(elemtext(element.find('m:documentation',ns)))),
			"| **ID** | {0} |\n".format(element.attrib['identifier']),
			"\n"
		])
		relationships = root.findall("m:relationships/m:relationship[@source='%s']" % elemid, ns)
		if (len(relationships) >= 1):
			mdout.writelines([
				"| Relationship Type | Relationship Name | Target Name | Target Type | Relationship Documentation |\n"
				"| ---- | ---- | ---- | ---- | ---- |\n"
			])
			for relationship in relationships:
				relntype = camelCaseRegex.sub(r"\1 \2", relationship.attrib[xsitype])
				targetid = relationship.attrib['target']
				target = root.findall("m:elements/m:element[@identifier='%s']" % targetid, ns)[0]
				targettype = camelCaseRegex.sub(r"\1 \2", target.attrib[xsitype])
				mdout.write(
					"| {0} | {1} | [{2}]({3}) | {4} | {5} |\n".format(
						relntype,
						elemtext(relationship.find('m:name',ns)),
						elemtext(target.find('m:name',ns)),
						"#%s" % targetid,
						targettype,
						escapetext(elemtext(relationship.find('m:documentation',ns)))
					)
				)
