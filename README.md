# archi-xml-excel-converter
XML &lt;--> Excel conversion scripts for 'Archi' Archimate models.

## Description
Archi (https://archimatetool.com/) is an open-source Archimate modelling tool.  It has its own file format,
but it can also import/export models using XML.

This project provides to convenience scripts written in Python 3 - one to transform the XML into Excel,
and the other to convert Excel into XML.  These scripts do not round trip - only some of the information
in the XML is converted to Excel, and you cannot create arbitrary Archi XML files from Excel.  Rather:

* XML to Excel conversion is focussed on getting the information out of an Archi model into Excel, e.g. so that you can get all names and descriptions from the model.
* Excel to XML conversion is focussed on being able to create an Archi model (without diagrams) based on model information created elsewhere.

Note that the scripts use the 'pandas' library, which comes with the 'Anaconda' Python distribution.

## Scripts
* archi-xml-to-excel.py:
  * Usage: ``python archi-xml-to-excel.py \<xml-input-path\> \<excel-output-path\>``
* \[TBD\] archi-excel-to-xml.py  

## Other files
* application-business-functions.archimate:
  * Small sample Archi model
* application-business-functions.xml
  * XML export of 'application-business-functions.archimate'
* application-business-functions.xlsx:
  * Archi model data in Excel, converted from 'application-business-functions.xml'
* archimate3\*.xsd (3 files):
  * Standard Archimate 3 XML Schemas for XML import/export format.   