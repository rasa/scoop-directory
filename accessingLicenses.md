# **SPDX Tech Report**

# Accessing the SPDX License List

# Abstract

The Software Products Data Exchange (SPDX) maintains the SPDX License List: a list of commonly found open source software licenses for the purposes of being able to easily and efficiently identify such licenses in an SPDX document. The SPDX License List includes a standardized short identifier, full name for each license, vetted license text, other basic information, and a canonical permanent URL.  This document describes various methods of accessing the current and previous versions of the list.  Several methods of accessing the license list are provided ranging from simply reading the license list on the website to programmatically accessing the license list information online.

This document is organized from the easiest method of access targeted at more casual users to the most sophisticated access targeted at software programmers.

This document does not go into any details on the criteria for what licenses are included on the SPDX License List, how to suggest new licenses, or how to determine if a license you find matches a license on the SPDX License List.  Information on the license list process and additional information on SPDX licenses can be found at http://spdx.org/licenses/ and links provided there.



Version2.1



Author: Gary O&#39;Neall

gary@sourceauditor.com

# Tech Report License

**Creative Commons Attribution 3.0 (SPDX License ID** [**CC-BY-3.0**](http://spdx.org/licenses/CC-BY-3.0)**)**

### License Summary

### You are free to:

- **Share**  — copy and redistribute the material in any medium or format
- **Adapt**  — remix, transform, and build upon the material
- for any purpose, even commercially

The licensor cannot revoke these freedoms as long as you follow the license terms.

### Under the following terms:

- **Attribution**  — You must give  [**appropriate credit**](http://creativecommons.org/licenses/by/3.0/), provide a link to the license, and [**indicate if changes were made**](http://creativecommons.org/licenses/by/3.0/). You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

- **No additional restrictions**  — You may not apply legal terms or  [**technological measures**](http://creativecommons.org/licenses/by/3.0/) that legally restrict others from doing anything the license permits.

### Notices:

- You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable  [**exception or limitation**](http://creativecommons.org/licenses/by/3.0/).
- No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as  [**publicity, privacy, or moral rights**](http://creativecommons.org/licenses/by/3.0/) may limit how you use the material.



See [http://creativecommons.org/licenses/by/3.0/legalcode](http://creativecommons.org/licenses/by/3.0/legalcode) for complete text of the license.

# Reading Licenses on the SPDX License List Web Pages

If you would like to quickly view the SPDX License List, simply going to the SPDX License List page is the fastest approach.  The SPDX License List page always contains the most recent published version of the license list.

## URL

The web page is located at http://www.spdx.org/licenses

## Table of Contents page

The main index page contains a description of the SPDX License List, pointers to other relevant information, the license list version, and a list of licenses.

### License List Version

The version of the license list can be found immediately prior to the list of licenses.

### List of Licenses

The license table contains information on the licenses.  The definition of the table columns can be found in the Explanation of SPDX License List Fields section on the [License List Overview webpage](http://spdx.org/spdx-license-list/license-list-overview).  Not all the fields are listed in this table.  Clicking on the full name of each license (or the License Text link) takes you to an individual web page for each license on the SPDX License List which contains the information for all the fields.

### Deprecated Licenses

Licenses in this table are no longer in used.  They are included on this page as a historical reference and should not be used going forward. That said, as the list is immutable, you may still see some of them in use in older SPDX documents as they may not have been updated.

### License Exception

A list of license exceptions can be found at [https://spdx.org/licenses/exceptions-index.html](https://spdx.org/licenses/exceptions-index.html)  The table columns follow the same definitions as the listed license.  Clicking on the full name of each license exception (or the License Exception Text link) takes you to an individual web page for each license on the SPDX License List which contains the information for all the fields.

# Accessing the Listed Licenses on github

In addition to updating the text on the website, license information is also maintained in github.  There are several formats supported.  The licenses are updated in github on every release of the license list.

The repository can be found at [https://github.com/spdx/license-list-data](https://github.com/spdx/license-list-data)

See the [README](https://github.com/spdx/license-list-data/blob/master/README.md) file for information on the format and conventions.

## Tags for Versions

A tag is created for each SPDX License List once it has been released and published at http://spdx.org/licenses.  The tag consists of &quot;v&quot; followed by the version number.  For example to access 2.4 of the license list use [https://github.com/spdx/license-list-data/tree/v2.4](https://github.com/spdx/license-list-data/tree/v2.4)

# Programmatically Accessing the Online License List using JSON

A table of contents for all SPDX listed licenses as well as license details is available on the spdx.org/licenses website.

## License List Table of Contents

The JSON file [https://spdx.org/licenses/licenses.json](https://spdx.org/licenses/licenses.json) lists summary information for all listed licenses and exceptions.

The JSON file contains 2 fields:

- licenseListVersion – The version for the licenselist
- licenses – An array of license summary information

The license summary information contains the following fields:

- reference – Reference to the HTML format for the license file
- isDeprecatedLicenseId – True if the entire license is deprecated (note – this isn&#39;t actually the best name for this particular field)
- detailsUrl – URL to a JSON file containing the license detailed information
- referenceNumber – Deprecated - this field is generated and is no longer in use
- name – License name
- licenseId – License identifier
- seeAlso – Cross reference URL pointing to additional copies of the license
- isOsiApproved – Indicates if the  [OSI](http://opensource.org/) has approved the license

## License List Details

A separate JSON file is present for each listed license and license exception.

### Forming the URL

To retrieve details for a license on the SPDX License List, access the JSON file at http://spdx.org/licenses/[licenseID].json where [licenseID] is the SPDX license identifier.

### License Detail JSON File Format

The JSON format for the licenses and exceptions follow the same term names and schema as the RDFa elements.

Below are the JSON field names:

- isDeprecatedLicenseId – True if the entire license is deprecated (note – this isn&#39;t actually the best name for this particular field)

- name - License name
- licenseId - License identifier
- licenseText - The full text of the license
- standardLicenseHeader - Text for a license notice as specifically delineated by the license or license appendix
- licenseTemplate - License template (if applicable) which describes sections of the license which can be varied. See [License Matching Guidelines](http://spdx.org/spdx-license-list/matching-guidelines) and Appendix II: License Matching Guidelines and Templates section of the specification for format information.
- isOsiApproved - Indicates if the  [OSI](http://opensource.org/) has approved the license
- seeAlso - Cross reference URL pointing to additional copies of the license



# Programmatically Accessing the Online License List using RDFa

To allow easy, well-defined programmatic access to the current SPDX Licenses List, the web pages are encoded using a [W3C](http://www.w3.org/) standard RDFa.  Using RDFa parsers, a program can access SPDX License List information in a more reliable fashion than manually parsing the HTML pages themselves.  The RDF terms used on the pages are also well-defined and documented in the [SPDX RDF terms page](http://spdx.org/rdf/terms).

## What is RDFa?

RDFa (Resource Descriptor Framework in Attributes) extends HTML (and XHTML) with attributes allowing RDF data to be easily extracted from the same web pages which can also be rendered using web browsers.

The following resources can provide you further information on RDFa:

- [Wikipedia article](http://en.wikipedia.org/wiki/RDFa)
- [W3C RDFa primer](http://www.w3.org/TR/rdfa-primer/)
- [Community website for RDFa](http://rdfa.info/) contains a number of resources for developers and users

### RDFa Available Parsers

There are a number of RDFa parsers available for various languages.   [The RDFa community page for developers](http://rdfa.info/dev/) contains a list of libraries for JavaScript, PHP, Python, Ruby, C, and Java.

In addition to the libraries mentioned above, [Java-RDFa](../../C:%5CUsers%5CGary%5CDocuments%5CSPDX%5CJava-RDFa) used in conjunction with [Apache Jena](http://jena.apache.org/) provides rich RDF functionality for Java applications.  These are the libraries used by the [SPDX Workgroup Tools](http://spdx.org/spdx-tools/tools-from-the-spdx-workgroup).

## Forming the URLs

To retrieve details for a license on the SPDX License List, access the HTML file at http://spdx.org/licenses/[licenseID] where [licenseID] is the SPDX license identifier.  Note that there is no file type appended.

## Listing the License ID&#39;s Available

A list of license ID&#39;s can be accessed by querying the RDFa located at http://spdx.org/licenses/index.html for resource license ID (http://spdx.org/rdf/terms#licenseId).

## RDFa Terms Used

The following RDF terms are used in both the index.html and individual license pages:

- http://spdx.org/rdf/terms#licenseId - A human readable short form license. The license Id must be of the form &quot;LicenseRef-&quot;[idString] where [idString] is a unique string containing letters, numbers, &quot;.&quot;, &quot;-&quot; or &quot;+&quot;.

The following RDF terms are used on the individual license pages:

- http://spdx.org/rdf/terms#name - License name
- http://spdx.org/rdf/terms#licenseText - The full text of the license
- http://spdx.org/rdf/terms#standardLicenseHeader - Text for a license notice as specifically delineated by the license or license appendix
- http://spdx.org/rdf/terms#licenseTemplate - License template (if applicable) which describes sections of the license which can be varied. See [License Matching Guidelines](http://spdx.org/spdx-license-list/matching-guidelines) and Appendix II: License Matching Guidelines and Templates section of the specification for format information.
- http://spdx.org/rdf/terms#isOsiApproved - Indicates if the  [OSI](http://opensource.org/) has approved the license
- http://www.w3.org/2000/01/rdf-schema#seeAlso - Cross reference URL pointing to additional copies of the license
- http://spdx.org/rdf/terms#isDeprecatedLicenseId – True if the entire license is deprecated (note – this isn&#39;t actually the best name for this particular field)

# Programmatically Accessing the Current SPDX License List using the SPDX Tools Library

The SPDX Tools are Java utilities and libraries made available by the SPDX workgroup under the Apache 2.0 license.  The SPDX Tools library contains a class SPDXLicenseInfoFactory which will parse SPDX license names, access the online SPDX License List using RDFa, and provide detailed information on the licenses.  If the web pages are not accessible (or if a Java property is set to use only offline licenses), a local cache of license information will be used.

## Downloading the Library

Source code for the SPDX libraries can be accessed in the Linux Git repository (git.spdx.org) in the spdx-tools.git project.  Implementation versions and a changelog is maintained in the root project directory.

The binary libraries are also included in each of the [SPDX workgroup tools](http://spdx.org/spdx-tools/tools-from-the-spdx-workgroup).

The binary jar files can also be downloaded from the [Maven Central Repository](http://search.maven.org/) using the group ID org.spdx and the artifact ID spdx-tools.

## Library APIs

The primary interfaces to the SPDX License List are the following methods in the org.spdx.rdfparser.SPDXLicenseInfoFactory class:

- String getLicenseListVersion() - Return the license list version used by the SPDX tools library
- SPDXStandardLicense getStandardLicenseById(String licenseId) - Return a SPDX license associated with the license ID parameter
- String[] getStandardLicenseIds() - Return an array of all SPDX standard license ID&#39;s
- isStandardLicenseId(String licenseId) - Returns true if the license ID is associated with an SPDX standard license ID
- SPDXLicenseInfo parseSPDXLicenseString(String licenseString) - Parses a license string compliant with the specification and returns an object representing the licenses.  The parser will handle standard license ID&#39;s, conjunctive license sets, disjunctive license sets, and non-standard license IDs.

The class SPDXStandardLicense contains fields for all the properties of a license on the SPDX License List (e.g. text, id, name, sourceUrls, template, standardLicenseHeader, comments).

The package org.spdx.licenseTemplate contains classes to manage the license templates used in SPDX licenses.  See the JavaDocs for this package (located in the doc directory of the source code or in the javadoc jar file in Maven) for a description of the interface to this package.  The primary interfaces are in the org.spdx.licenseTemplate.SpdxLicenseTemplateHelper class.

The class org.spdx.compare.LicenseCompareHelper contains methods to compare license text to determine if they are equivalent according to the license matching [guidelines](https://spdx.org/spdx-license-list/matching-guidelines) maintained by the SPDX workgroup.  The method boolean LicenseCompareHelper.isTextStandardLicense(SPDXStandardLicense license, String licenseText) will return true if the licenseText is equivalent to a license on the SPDX License List considering both the license template replaceable/optional text as well as the license matching guidelines.

## Updating the SPDX License List in the Offline Cache

By default, the SPDX Tools Library will access the current SPDX License List web pages using RDFa to acquire the license information.  If there is no Internet access to http://spdx.org/licenses or if the configuration property OnlyUseLocalLicenses is set to true, a local offline cache of the licenses is used.

The license cache can be found in the resources/stdlicenses directory in the same directory where the library is installed.  The files in this directory is are exact copies of the HTML files found on the http://spdx.org/licenses web pages.  If you wish to update the licenses, theses files can be replaced.

Also within the resources/stdlicenses directory is a file licenses.properties.  This file contains the configuration property OnlyUseLocalLicenses.  Editing this text file and setting OnlyUseLocalLicenses=true will always use the offline cache.

## Examples

### Accessing the Text for a Standard SPDX License

To print out the text for Apache 1.1 to the console:
```Java

        public static void main(String[] args) {

                try {

                        SPDXStandardLicense apache11 = SPDXLicenseInfoFactory

                                ._getStandardLicenseById_("Apache-1.1");

                        System._out_.println(apache11.getText());

                } catch (InvalidSPDXAnalysisException e) {

                        System._out_.println("Error getting Standard License: " +

                                                        e.getMessage());

                }

        }
```
### Determining if License Text is Equivalent to an SPDX Standard License Text

To determine if the license text in the string licenseTxt is equivalent to the license text for the BSD 3 clause license:
```Java
        public static void main(String[] args) {

                String licenseText = "...";

                try {

                        SPDXStandardLicense bsd3clause = SPDXLicenseInfoFactory

                                        ._getStandardLicenseById_("BSD-3-Clause");

                        boolean matches = LicenseCompareHelper

                                ._isTextStandardLicense_(bsd3clause, licenseText);

                        if (matches) {

                                System._out_.println(&quot;Matches&quot;);

                        } else {

                                System._out_.println("Does not match");

                        }

                } catch (InvalidSPDXAnalysisException e) {

                        System._out_.println("Error getting lic: ";+e.getMessage());

                } catch (SpdxCompareException e) {

                        System._out_.println("Error comparing: "+e.getMessage());

                }

        }
```
# Accessing Older Versions of the License List

An archive of the older versions of the HTML pages for the SPDX License List, starting with version 1.17, can be found at http://spdx.org/licenses/archive/archived\_ll\_vX.XX where vX.XX is the version of the license list.
