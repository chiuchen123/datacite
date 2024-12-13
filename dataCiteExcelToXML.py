
from lxml import etree as ET
import csv
import argparse
import pandas as pd
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--excel', help='Enter Excel filename to convert to CSV, including extension. Optional - if not provided, the script will ask for input. Example: sheets.xlsx')
parser.add_argument('-c', '--CSV', help="Enter filename for CSV to be created. Optional - if not provided, the script will ask for input. Example: C:\\Users\\User1\\Desktop\\export_dataframe.csv")
args = parser.parse_args()

if args.excel:
    excelfile = args.excel
else:
    excelfile = input('Enter Excel filename: ')
if args.CSV:
    filename = args.CSV
else:
    filename = input('Enter CSV filename: ')

# Create the pd.ExcelFile() object
xls = pd.ExcelFile(excelfile)

# Extract the sheet names from xls
sheetNamesList = xls.sheet_names
sheetNamesList.pop()

# Create an empty list: listings
listings = []

# Import the data
for sheetName in sheetNamesList:
    df = pd.read_excel(xls, sheet_name=sheetName, na_values='n/a')
    df = df.iloc[1:, :]
    df.dropna(axis=0, how='all', subset=None, inplace=True)
    df.dropna(axis=1, how='all', subset=None, inplace=True)
    listings.append(df)

excelfile_edited = excelfile[:-5]  # createlog
f = (open('log_'+excelfile_edited+'_'+datetime.now().strftime('%Y-%m-%d %H.%M.%S')+'.txt', 'a'))

# Concatenate the listings: listing_data
listing_data = pd.concat(listings, join='outer', ignore_index=True, sort=False)
listing_data.to_csv(filename, index=False, header=True, encoding='utf-8')
print('CSV of data created, saved as {}!'.format(filename), file=f)
print()


# Find all unique requests
request_list = []
with open(filename, encoding='utf-8') as nameFile:
    datacite_elements = csv.DictReader(nameFile)
    for element in datacite_elements:
        request = element['JHED - Request#'].strip()
        if request:
            if request not in request_list:
                request_list.append(request)
        elif not request:
            print('ERROR! Your workbook has a row with a blank identifier.', file=f)


total_requests = len(request_list)
print('{} DOI requests found: {}; generating {} XML documents.'.format(total_requests, request_list, total_requests), file=f)
print('', file=f)
for x in request_list:   # for each request identifier in CSV
    with open(filename, encoding='utf-8') as nameFile:  # open CSV
        datacite_elements = csv.DictReader(nameFile)  # read each row as a dictonary
        attr_qname = ET.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        datacite = 'http://datacite.org/schema/kernel-4'
        xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        nsmap = {None: datacite, 'xsi': xsi}
        resource = ET.Element('resource', {attr_qname: "http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.2/metadata.xsd"}, nsmap=nsmap)
        identifier = ET.SubElement(resource, 'identifier')
        identifier.text = ''
        identifier.set('identifierType', 'DOI')
        name_loop = 0
        subject_loop = 0
        contributor_name_loop = 0
        date_loop = 0
        alternative_loop = 0
        related_loop = 0
        geo_locations_loop = 0
        funding_loop = 0
        geo_polygon = []
        print('Creating XML document for request with identifier "{}".'.format(x), file=f)
        for element in datacite_elements:
            if x in element['JHED - Request#'].strip():  # for each row in CSV where request number is found, map associated element into XML
                try:
                    creator_name = element['creatorName'].strip()
                    name_type = element['nameType'].strip()
                    if creator_name and name_type:
                        name_loop = name_loop + 1
                        if name_loop == 1:
                            creators = ET.SubElement(resource, 'creators')
                            creator = ET.SubElement(creators, 'creator')
                            creatorName = ET.SubElement(creator, 'creatorName')
                            creatorName.text = creator_name
                            creatorName.set('nameType', name_type)
                        else:
                            creator = ET.SubElement(creators, 'creator')
                            creatorName = ET.SubElement(creator, 'creatorName')
                            creatorName.text = creator_name
                            creatorName.set('nameType', name_type)
                    elif creator_name:
                        print('ERROR! name "{}" requires a nameType.'.format(creator_name), file=f)
                    elif name_type:
                        print('ERROR! nameType "{}" requires a name.'.format(name_type), file=f)
                except:
                    pass
                try:
                    name_identifier = element['nameIdentifier'].strip()
                    name_scheme_URI = element['nameIdentifierScheme'].strip()
                    if name_identifier and name_scheme_URI:
                        nameIdentifier = ET.SubElement(creator, 'nameIdentifier')
                        nameIdentifier.text = name_identifier
                        nameIdentifier.set('nameIdentifierScheme', name_scheme_URI)
                    elif name_identifier:
                        print('ERROR! nameIdentifier "{}" requires a nameIdentifierScheme.'.format(name_identifier), file=f)
                    elif name_scheme_URI:
                        print('ERROR! nameIdentifierScheme "{}" requires a nameIdentifier.'.format(name_scheme_URI), file=f)
                except:
                    pass
                try:
                    organization = element['Affiliation'].strip()
                    if organization:
                        affiliation = ET.SubElement(creator, 'affiliation')
                        affiliation.text = organization
                except:
                    pass
                try:
                    title_csv = element['title'].strip()
                    if title_csv:
                        titles = ET.SubElement(resource, 'titles')
                        title = ET.SubElement(titles, 'title')
                        title.text = title_csv
                except:
                    pass
                try:
                    publisher_csv = element['publisher'].strip()
                    if publisher_csv:
                        publisher = ET.SubElement(resource, 'publisher')
                        publisher.text = publisher_csv
                except:
                    pass
                try:
                    publication_year = element['publicationYear'].strip()
                    if publication_year:
                        publicationYear = ET.SubElement(resource, 'publicationYear')
                        publicationYear.text = publication_year
                except:
                    pass
                try:
                    subject_csv = element['subject'].strip()
                    if subject_csv:
                        subject_loop = subject_loop + 1
                        if subject_loop == 1:
                            subjects = ET.SubElement(resource, 'subjects')
                            subject = ET.SubElement(subjects, 'subject')
                            subject.text = subject_csv
                        else:
                            subject = ET.SubElement(subjects, 'subject')
                            subject.text = subject_csv
                except:
                    pass
                try:
                    subject_scheme_URI = element['subjectSchemeURI'].strip()
                    if subject_scheme_URI:
                        subject.set('schemeURI', subject_scheme_URI)
                except:
                    pass
                try:
                    subject_scheme = element['subjectScheme'].strip()
                    if subject_scheme:
                        subject.set('subjectScheme', subject_scheme)
                except:
                    pass
                try:
                    subject_value_URI = element['valueURI'].strip()
                    if subject_value_URI:
                        subject.set('valueURI', subject_value_URI)
                except:
                    pass
                try:
                    contributor_name = element['contributorName'].strip()
                    contributor_type = element['contributorType'].strip()
                    if contributor_name and contributor_type:
                        contributor_name_loop = contributor_name_loop + 1
                        if contributor_name_loop == 1:
                            contributors = ET.SubElement(resource, 'contributors')
                            contributor = ET.SubElement(contributors, 'contributor')
                            contributorName = ET.SubElement(contributor, 'contributorName')
                            contributorName.text = contributor_name
                            contributor.set('contributorType', contributor_type)
                        else:
                            contributor = ET.SubElement(contributors, 'contributor')
                            contributorName = ET.SubElement(contributor, 'contributorName')
                            contributorName.text = contributor_name
                            contributor.set('contributorType', contributor_type)
                    elif contributor_name:
                        print('ERROR! contributorName "{}" requires a contributorType.'.format(contributor_name), file=f)
                    elif contributor_type:
                        print('ERROR! contributorType "{}" requires a contributorName.'.format(contributor_type), file=f)
                except:
                    pass
                try:
                    contributor_name_type = element['contributorNameType'].strip()
                    if contributor_name_type:
                        contributorName.set('nameType', contributor_name_type)
                except:
                    pass
                try:
                    contributor_name_identifier = element['contributorNameIdentifier'].strip()
                    contributor_identifier_scheme = element['contributorIdentifierScheme'].strip()
                    if contributor_name_identifier and contributor_identifier_scheme:
                        contributorNameIdentifier = ET.SubElement(contributor, 'nameIdentifier')
                        contributorNameIdentifier.text = contributor_name_identifier
                        contributorNameIdentifier.set('nameIdentifierScheme', contributor_identifier_scheme)
                    elif contributor_name_identifier:
                        print('ERROR! contributorNameIdentifier "{}" requires a contributorIdentifierScheme.'.format(contributor_name_identifier), file=f)
                    elif contributor_identifier_scheme:
                        print('ERROR! contributorIdentifierScheme "{}" requires a contributorNameIdentifier.'.format(contributor_identifier_scheme), file=f)
                except:
                    pass
                try:
                    contributor_name_scheme_URI = element['contributorSchemeURI'].strip()
                    if contributor_name_scheme_URI:
                        contributorNameIdentifier.set('schemeURI', contributor_name_scheme_URI)
                except:
                    pass
                try:
                    contributor_affiliation = element['contributorAffiliation']
                    if contributor_affiliation:
                        affiliation = ET.SubElement(contributor, 'affiliation')
                except:
                    pass
                try:
                    date_csv = element['date'].strip()
                    date_type = element['dateType'].strip()
                    if date_csv and date_type:
                        date_loop = date_loop + 1
                        if date_loop == 1:
                            dates = ET.SubElement(resource, 'dates')
                            date = ET.SubElement(dates, 'date')
                            date.text = date_csv
                            date.set('dateType', date_type)
                        else:
                            date = ET.SubElement(dates, 'date')
                            date.text = date_csv
                            date.set('dateType', date_type)
                    elif date_csv:
                        print('ERROR! Date "{}" requires a dateType'.format(date_csv), file=f)
                    elif date_type:
                        print('ERROR! DateType "{}" requires a date'.format(date_type), file=f)
                except:
                    pass
                try:
                    language_csv = element['language'].strip()
                    if language_csv:
                        language = ET.SubElement(resource, 'language')
                        language.text = language_csv
                except:
                    pass
                try:
                    resource_type = element['resourceType'].strip()
                    resource_type_general = element['generalResourceType'].strip()
                    if resource_type and resource_type_general:
                        resourceType = ET.SubElement(resource, 'resourceType')
                        resourceType.text = resource_type
                        resourceType.set('resourceTypeGeneral', resource_type_general)
                    elif resource_type:
                        print('ERROR! resourceType "{}" requires a generalResourceType'.format(resource_type), file=f)
                    elif resource_type_general:
                        print('ERROR! resourceTypeGeneral "{}" requires a resouceType'.format(resource_type_general), file=f)

                except:
                    pass
                try:
                    alternative_identifier = element['alternativeIdentifier'].strip()
                    alternative_identifier_type = element['alternativeIdentifierType'].strip()
                    if alternative_identifier and alternative_identifier_type:
                        alternative_loop = alternative_loop + 1
                        if alternative_loop == 1:
                            alternativeIdentifiers = ET.SubElement(resource, 'alternativeIdentifiers')
                            alternativeIdentifier = ET.SubElement(alternativeIdentifiers, 'alternativeIdentifier')
                            alternativeIdentifier.text = alternative_identifier
                            alternativeIdentifier.set('alternativeIdentifierType', alternative_identifier_type)
                        else:
                            alternativeIdentifier = ET.SubElement(alternativeIdentifiers, 'alternativeIdentifier')
                            alternativeIdentifier.text = alternative_identifier
                            alternativeIdentifier.set('alternativeIdentifierType', alternative_identifier_type)
                    elif alternative_identifier:
                        print('ERROR! alternativeIdentifier "{}" requires an alternativeIdentifierType'.format(alternative_identifier), file=f)
                    elif alternative_identifier_type:
                        print('ERROR! alternativeIdentifierType "{}" requires an alternativeIdentifier'.format(alternative_identifier_type), file=f)
                    else:
                        pass
                except:
                    pass
                try:
                    related_identifier = element['relatedIdentifier'].strip()
                    related_identifier_type = element['relatedIdentifierType'].strip()
                    relation_type = element['relationType'].strip()
                    if related_identifier and related_identifier_type and relation_type:
                        related_loop = related_loop + 1
                        if related_loop == 1:
                            relatedIdentifiers = ET.SubElement(resource, 'relatedIdentifiers')
                            relatedIdentifier = ET.SubElement(relatedIdentifiers, 'relatedIdentifier')
                            relatedIdentifier.text = related_identifier
                            relatedIdentifier.set('relatedIdentifierType', related_identifier_type)
                            relatedIdentifier.set('relationType', relation_type)
                        else:
                            relatedIdentifier = ET.SubElement(relatedIdentifiers, 'relatedIdentifier')
                            relatedIdentifier.text = related_identifier
                            relatedIdentifier.set('relatedIdentifierType', related_identifier_type)
                            relatedIdentifier.set('relationType', relation_type)
                    elif related_identifier or (related_identifier and related_identifier_type) or (related_identifier and relation_type):
                        print('ERROR! relatedIdentifier "{}" requires a relatedIdentifierType and a relationType'.format(related_identifier), file=f)
                    elif related_identifier_type or (related_identifier_type and relation_type):
                        print('ERROR! relatedIdentifierType "{}" requires an relatedIdentifier and a relationType'.format(related_identifier_type), file=f)
                    elif relation_type:
                        print('ERROR! relationType "{}" requires an relatedIdentifier and a relatedIdentifierType'.format(relation_type), file=f)
                    else:
                        pass
                except:
                    pass
                try:
                    related_metadata_scheme = element['relatedMetadataScheme'].strip()
                    if related_metadata_scheme:
                        relatedIdentifier.set('relatedMetadataScheme', related_metadata_scheme)
                except:
                    pass
                try:
                    related_scheme_uri = element['relatedSchemeURI'].strip()
                    if related_scheme_uri:
                        relatedIdentifier.set('schemeURI', related_scheme_uri)
                except:
                    pass
                try:
                    related_scheme_type = element['relatedSchemeType'].strip()
                    if related_scheme_type:
                        relatedIdentifier.set('schemeType', related_scheme_type)
                except:
                    pass
                try:
                    size_csv = element['size'].strip()
                    if size_csv:
                        sizes = ET.SubElement(resource, 'sizes')
                        size = ET.SubElement(sizes, 'size')
                        size.text = size_csv
                except:
                    pass
                try:
                    format_csv = element['format'].strip()
                    if format_csv:
                        formats = ET.SubElement(resource, 'formats')
                        format = ET.SubElement(formats, 'format')
                        format.text = format_csv
                except:
                    pass
                try:
                    version_csv = element['version'].strip()
                    if version_csv:
                        version = ET.SubElement(resource, 'version')
                        version.text = version_csv
                except:
                    pass
                try:
                    rights_csv = element['rights'].strip()
                    if rights_csv:
                        rightsList = ET.SubElement(resource, 'rightsList')
                        rights = ET.SubElement(rightsList, 'rights')
                        rights.text = rights_csv
                except:
                    pass
                try:
                    rights_uri = element['rightsURI'].strip()
                    if rights_uri:
                        rights.set('rightsURI', rights_uri)
                except:
                    pass
                try:
                    description_csv = element['description'].strip()
                    description_type = element['descriptionType'].strip()
                    if description_csv and description_type:
                        descriptions = ET.SubElement(resource, 'descriptions')
                        description = ET.SubElement(descriptions, 'description')
                        description.set('descriptionType', description_type)
                        description.text = description_csv
                    elif description_csv:
                        print('ERROR! description "{}" requires a descriptionType.'.format(description_csv), file=f)
                    elif description_type:
                        print('ERROR! descriptionType "{}" requires a description.'.format(description_type), file=f)
                except:
                    pass
                geo_location_loop = 0
                try:
                    geo_location_place = element['geoLocationPlace'].strip()
                    if geo_location_place:
                        geo_locations_loop = geo_locations_loop + 1
                        geo_location_loop = geo_location_loop + 1
                        if geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPlace = ET.SubElement(geoLocation, 'geoLocationPlace')
                            geoLocationPlace.text = geo_location_place
                        elif geo_location_loop == 1:
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPlace = ET.SubElement(geoLocation, 'geoLocationPlace')
                            geoLocationPlace.text = geo_location_place
                        else:
                            geoLocationPlace = ET.SubElement(geoLocation, 'geoLocationPlace')
                            geoLocationPlace.text = geo_location_place
                except:
                    pass
                try:
                    point_longitude = element['pointLongitude'].strip()
                    point_latitude = element['pointLatitude'].strip()
                    if point_longitude and point_latitude:
                        geo_locations_loop = geo_locations_loop + 1
                        geo_location_loop = geo_location_loop + 1
                        if geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPoint = ET.SubElement(geoLocation, 'geoLocationPoint')
                            geoPointLongitude = ET.SubElement(geoLocationPoint, 'pointLongitude')
                            geoPointLatitude = ET.SubElement(geoLocationPoint, 'pointLatitude')
                            geoPointLongitude.text = point_longitude
                            geoPointLatitude.text = point_latitude
                        elif geo_location_loop == 1:
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPoint = ET.SubElement(geoLocation, 'geoLocationPoint')
                            geoPointLongitude = ET.SubElement(geoLocationPoint, 'pointLongitude')
                            geoPointLatitude = ET.SubElement(geoLocationPoint, 'pointLatitude')
                            geoPointLongitude.text = point_longitude
                            geoPointLatitude.text = point_latitude
                        else:
                            geoLocationPoint = ET.SubElement(geoLocation, 'geoLocationPoint')
                            geoPointLongitude = ET.SubElement(geoLocationPoint, 'pointLongitude')
                            geoPointLatitude = ET.SubElement(geoLocationPoint, 'pointLatitude')
                            geoPointLongitude.text = point_longitude
                            geoPointLatitude.text = point_latitude
                    elif point_latitude or point_longitude:
                        print('ERROR! geoLocationPoint requires both pointLongitude and pointLatitude.', file=f)
                except:
                    pass
                try:
                    westbound_longitude = element['westBoundLongitude'].strip()
                    eastbound_longitude = element['eastBoundLongitude'].strip()
                    southbound_latitude = element['southBoundLatitude'].strip()
                    northbound_latitude = element['northBoundLatitude'].strip()
                    if westbound_longitude and eastbound_longitude and southbound_latitude and northbound_latitude:
                        geo_locations_loop = geo_locations_loop + 1
                        geo_location_loop = geo_location_loop + 1
                        if geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationBox = ET.SubElement(geoLocation, 'geoLocationBox')
                            westBoundLongitude = ET.SubElement(geoLocationBox, 'westBoundLongitude')
                            eastBoundLongitude = ET.SubElement(geoLocationBox, 'eastBoundLongitude')
                            southBoundLatitude = ET.SubElement(geoLocationBox, 'southBoundLatitude')
                            northBoundLatitude = ET.SubElement(geoLocationBox, 'northBoundLatitude')
                            westBoundLongitude.text = westbound_longitude
                            eastBoundLongitude.text = eastbound_longitude
                            southBoundLatitude.text = southbound_latitude
                            northBoundLatitude.text = northbound_latitude
                        elif geo_location_loop == 1:
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationBox = ET.SubElement(geoLocation, 'geoLocationBox')
                            westBoundLongitude = ET.SubElement(geoLocationBox, 'westBoundLongitude')
                            eastBoundLongitude = ET.SubElement(geoLocationBox, 'eastBoundLongitude')
                            southBoundLatitude = ET.SubElement(geoLocationBox, 'southBoundLatitude')
                            northBoundLatitude = ET.SubElement(geoLocationBox, 'northBoundLatitude')
                            westBoundLongitude.text = westbound_longitude
                            eastBoundLongitude.text = eastbound_longitude
                            southBoundLatitude.text = southbound_latitude
                            northBoundLatitude.text = northbound_latitude
                        else:
                            geoLocationBox = ET.SubElement(geoLocation, 'geoLocationBox')
                            westBoundLongitude = ET.SubElement(geoLocationBox, 'westBoundLongitude')
                            eastBoundLongitude = ET.SubElement(geoLocationBox, 'eastBoundLongitude')
                            southBoundLatitude = ET.SubElement(geoLocationBox, 'southBoundLatitude')
                            northBoundLatitude = ET.SubElement(geoLocationBox, 'northBoundLatitude')
                            westBoundLongitude.text = westbound_longitude
                            eastBoundLongitude.text = eastbound_longitude
                            southBoundLatitude.text = southbound_latitude
                            northBoundLatitude.text = northbound_latitude
                    elif westbound_longitude or eastbound_longitude or southbound_latitude or northbound_latitude:
                        print('ERROR! One or more points from your geobox is missing.', file=f)
                except:
                    pass
                try:
                    polygon_long = element['polyPointLongitude']
                    polygon_lat = element['polyPointLatitude']
                    geo_location_polygon = element['geoLocationPolygon'].strip()
                    if geo_location_polygon:
                        geo_locations_loop = geo_locations_loop + 1
                        geo_location_loop = geo_location_loop + 1
                        if geo_location_polygon not in geo_polygon and geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPolygon = ET.SubElement(geoLocation, 'geoLocationPolygon')
                            polygonPoint = ET.SubElement(geoLocationPolygon, 'polygonPoint')
                            polyPointLongitude = ET.SubElement(polygonPoint, 'pointLongitude')
                            polyPointLatitude = ET.SubElement(polygonPoint, 'pointLatitude')
                            polyPointLongitude.text = polygon_long
                            polyPointLatitude.text = polygon_lat
                            geo_polygon.append(geo_location_polygon)
                        elif geo_location_polygon not in geo_polygon and geo_location_loop == 1:
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPolygon = ET.SubElement(geoLocation, 'geoLocationPolygon')
                            polygonPoint = ET.SubElement(geoLocationPolygon, 'polygonPoint')
                            polyPointLongitude = ET.SubElement(polygonPoint, 'pointLongitude')
                            polyPointLatitude = ET.SubElement(polygonPoint, 'pointLatitude')
                            polyPointLongitude.text = polygon_long
                            polyPointLatitude.text = polygon_lat
                            geo_polygon.append(geo_location_polygon)
                        elif geo_location_polygon not in geo_polygon and geo_locations_loop != 1:
                            geoLocationPolygon = ET.SubElement(geoLocation, 'geoLocationPolygon')
                            polygonPoint = ET.SubElement(geoLocationPolygon, 'polygonPoint')
                            polyPointLongitude = ET.SubElement(polygonPoint, 'pointLongitude')
                            polyPointLatitude = ET.SubElement(polygonPoint, 'pointLatitude')
                            polyPointLongitude.text = polygon_long
                            polyPointLatitude.text = polygon_lat
                            geo_polygon.append(geo_location_polygon)
                        elif geo_location_polygon in geo_polygon and geo_locations_loop != 1:
                            polygonPoint = ET.SubElement(geoLocationPolygon, 'polygonPoint')
                            polyPointLongitude = ET.SubElement(polygonPoint, 'pointLongitude')
                            polyPointLatitude = ET.SubElement(polygonPoint, 'pointLatitude')
                            polyPointLongitude.text = polygon_long
                            polyPointLatitude.text = polygon_lat
                        else:
                            print('error!')
                except:
                    pass
                try:
                    funder_name = element['funderName'].strip()
                    if funder_name:
                        funding_loop = funding_loop + 1
                        if funding_loop == 1:
                            fundingReferences = ET.SubElement(resource, 'fundingReferences')
                            fundingReference = ET.SubElement(fundingReferences, 'fundingReference')
                            funderName = ET.SubElement(fundingReference, 'funderName')
                            funderName.text = funder_name
                        else:
                            fundingReference = ET.SubElement(fundingReferences, 'fundingReference')
                            funderName = ET.SubElement(fundingReference, 'funderName')
                            funderName.text = funder_name
                except:
                    pass
                try:
                    funder_identifier = element['funderIdentifier'].strip()
                    funder_identifier_type = element['funderIdentifierType'].strip()
                    if funder_identifier and funder_identifier_type:
                        funderIdentifier = ET.SubElement(fundingReference, 'funderIdentifier')
                        funderIdentifier.text = funder_identifier
                        funderIdentifier.set('funderIdentifierType', funder_identifier_type)
                    elif funder_identifier:
                        print('ERROR! funderIdentifier "{}" requires a funderIdentifierType.'.format(funder_identifier), file=f)
                    elif funder_identifier_type:
                        print('ERROR! funderIdentifierType "{}" requires a funderIdentifier.'.format(funder_identifier_type), file=f)
                except:
                    pass
                try:
                    award_number = element['awardNumber'].strip()
                    if award_number:
                        awardNumber = ET.SubElement(fundingReference, 'awardNumber')
                        awardNumber.text = award_number
                except:
                    pass
                try:
                    award_title = element['awardTitle'].strip()
                    if award_title:
                        awardTitle = ET.SubElement(fundingReference, 'awardTitle')
                        awardTitle.text = award_title
                except:
                    pass
                try:
                    award_uri = element['awardURI'].strip()
                    if award_uri:
                        awardNumber.set('awardURI', award_uri)
                except:
                    pass
            else:
                pass

        required_list = set(['titles', 'creators', 'publisher', 'publicationYear', 'resourceType'])
        list_elements = set()
        for child in resource.iter():
            child = child.tag
            list_elements.add(child)
        missing_elements = required_list.difference(list_elements)
        if missing_elements is not None:
            for missing in missing_elements:
                print(('"{}" is missing required element "{}".'.format(x, missing)), file=f)

        tree = ET.ElementTree(resource)
        xmlfile = 'dataCite_'+x+'.xml'
        ET.tostring(tree, encoding='utf-8')  # encodes characters properly
        tree.write(open(xmlfile, 'wb'))  # Creates XML document
        print('XML document for ""{}" request created, saved as "{}".'.format(x, xmlfile), file=f)
        print('', file=f)


f.close()  # print log to terminal
name = f.name
log = open(name)
log = log.read()
print(log)
print('Script finished')
