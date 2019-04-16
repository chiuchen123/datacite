
from lxml import etree as ET
import lxml.builder
import csv
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--excel', help='Enter Excel filename to convert to CSV, including extension. Optional - if not provided, the script will ask for input. Example: sheets.xlsx')
parser.add_argument('-c', '--CSV', help="Enter file path with filename where you'd like CSV saved. Optional - if not provided, the script will ask for input. Example: C:\\Users\\User1\\Desktop\\export_dataframe.csv")
args = parser.parse_args()

if args.excel:
    excelfile = args.excel
else:
    excelfile  = input('Enter Excel filename: ')
if args.CSV:
    filename = args.CSV
else:
    filename = input('Enter file path: ')

# Create the pd.ExcelFile() object
xls = pd.ExcelFile(excelfile)

# Extract the sheet names from xls
sheetNamesList = xls.sheet_names
sheetNamesList.pop()

# Create an empty list: listings
listings = []

# Import the data
for sheetName in sheetNamesList :
    df = pd.read_excel(xls, sheet_name=sheetName, na_values='n/a')
    df = df.iloc[1:,:]
    df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
    df.dropna(axis=1, how='all', thresh=None, subset=None, inplace=True)
    #print df
    listings.append(df)

# Concatenate the listings: listing_data
listing_data = pd.concat(listings, join ='outer', ignore_index=True, sort=False)
listing_data.to_csv(filename, index = False, header = True, encoding = 'utf-8')
print('CSV of data created, saved as {}!'.format(filename))
print()



request_list = []
with open(filename) as nameFile:
    datacite_elements = csv.DictReader(nameFile)
    for element in datacite_elements:
        request = element['JHED - Request#'].strip()
        if request not in request_list:
            request_list.append(request)


total_requests = len(request_list)
print('{} DOI requests found; generating {} XML documents.'.format(total_requests, total_requests))
print()
for x in request_list:
    with open(filename) as nameFile:
        datacite_elements = csv.DictReader(nameFile)
        attr_qname = ET.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        datacite = 'http://datacite.org/schema/kernel-4'
        xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        nsmap = {None: datacite, 'xsi': xsi}
        resource = ET.Element('resource', {attr_qname:"http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.1/metadata.xsd"}, nsmap = nsmap)
        identifier = ET.SubElement(resource, 'identifier')
        identifier.text = '10.5072'
        identifier.set('identifierType','DOI')
        name_loop = 0
        subject_loop = 0
        contributor_name_loop = 0
        date_loop = 0
        alternative_loop = 0
        related_loop = 0
        geo_locations_loop = 0
        funding_loop = 0
        geo_polygon = []
        print('Creating XML document for request with identifier {}.'.format(x))
        print()
        for element in datacite_elements:
            if x in element['JHED - Request#'].strip():
                try:
                    creator_name = element['creatorName'].strip()
                    if creator_name:
                        name_loop = name_loop + 1
                        if name_loop == 1:
                            creators = ET.SubElement(resource, 'creators')
                            creator = ET.SubElement(creators, 'creator')
                            creatorName = ET.SubElement(creator, 'creatorName')
                            creatorName.text = creator_name
                        else:
                            creator = ET.SubElement(creators, 'creator')
                            creatorName = ET.SubElement(creator, 'creatorName')
                            creatorName.text = creator_name
                except:
                    pass
                try:
                    name_type = element['nameType'].strip()
                    if name_type == 'organization':
                        creatorName.set('nameType', name_type)
                    elif name_type == "personal":
                        personal_name = creator_name.split(',')
                        given_name = personal_name[1].strip()
                        family_name = personal_name[0].strip()
                        creatorName.set('nameType', name_type)
                        givenName = ET.SubElement(creator, 'givenName')
                        familyName = ET.SubElement(creator, 'familyName')
                        givenName.text = given_name
                        familyName.text = family_name
                    else:
                        pass
                except:
                    pass
                try:
                    name_identifier = element['Orchid ID'].strip()
                    if name_identifier:
                        nameIdentifier = ET.SubElement(creator, 'nameIdentifer')
                        nameIdentifier.text = name_identifier
                except:
                    pass
                try:
                    name_scheme_URI = element['Scheme ID'].strip()
                    if name_scheme_URI:
                        nameIdentifier.set('schemeURI', name_scheme_URI)
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
                        publicationYear = ET.SubElement(resource,'publicationYear')
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
                    if contributor_name:
                        contributor_name_loop = contributor_name_loop + 1
                        if contributor_name_loop == 1:
                            contributors = ET.SubElement(resource, 'contributors')
                            contributor = ET.SubElement(contributors, 'contributor')
                            contributorName = ET.SubElement(contributor, 'contributorName')
                            contributorName.text = contributor_name
                        else:
                            contributor = ET.SubElement(contributors, 'contributor')
                            contributorName = ET.SubElement(contributor, 'contributorName')
                            contributorName.text = contributor_name
                except:
                    pass
                try:
                    contributor_name_type = element['contributorNameType'].strip()
                    if contributor_name_type:
                        if contributor_name_type == 'organization':
                            contributorName.set('nameType', contributor_name_type)
                        elif contributor_name_type== "personal":
                            contributor_personal_name = contributor_name.split(',')
                            contributor_given_name = contributor_personal_name[1].strip()
                            contributor_family_name = contributor_personal_name[0].strip()
                            contributorName.set('nameType', contributor_name_type)
                            contributorGivenName  = ET.SubElement(contributor, 'givenName' )
                            contributorFamilyName = ET.SubElement(contributor, 'familyName')
                            contributorGivenName.text = contributor_given_name
                            contributorFamilyName.text = contributor_family_name
                except:
                    pass
                try:
                    contributor_name_identifier = element['contributorNameIdentifier'].strip()
                    if contributor_name_identifier:
                        contributorNameIdentifier = ET.SubElement(contributor, 'nameIdentifer')
                        contributorNameIdentifier.text = contributor_name_identifier
                        contributorNameIdentifier.set('nameIdentifierScheme', 'ORCID')
                except:
                    pass
                try:
                    contributor_name_scheme_URI = element['contributorSchemeURI'].strip()
                    contributor_identifier_scheme = element['contributorIdentifierScheme'].strip()
                    if contributor_name_scheme_URI:
                        contributorNameIdentifier.set('schemeURI', contributor_name_scheme_URI)
                        contributorNameIdentifier.set('nameIdentifierScheme', contributor_identifier_scheme)
                except:
                    pass
                try:
                    conbtributor_organization = element['contributorAffiliation'].strip()
                    if conbtributor_organization:
                        contributorAffiliation = ET.SubElement(contributor, 'affiliation')
                        contributorAffiliation.text = conbtributor_organization
                except:
                    pass
                try:
                    date_csv = element['date'].strip()
                    if date_csv:
                        date_loop = date_loop + 1
                        if date_loop == 1:
                            dates = ET.SubElement(resource, 'dates')
                            date = ET.SubElement(dates, 'date')
                            date.text = date_csv
                        else:
                            date = ET.SubElement(dates, 'date')
                            date.text = date_csv
                except:
                    pass
                try:
                    date_type = element['dateType'].strip()
                    if date_type:
                        date.set('dateType', date_type)
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
                    if resource_type:
                        resourceType = ET.SubElement(resource, 'resourceType')
                        resourceType.text = resource_type
                except:
                    pass
                try:
                    resource_type_general = element['generalResourceType'].strip()
                    if resource_type_general:
                        resourceType.set('resourceTypeGeneral', resource_type_general)
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
                    else:
                        pass
                except:
                    pass
                try:
                    related_identifier = element['relatedIdentifier'].strip()
                    if related_identifier:
                        related_loop = related_loop + 1
                        if related_loop == 1:
                            relatedIdentifiers = ET.SubElement(resource, 'relatedIdentifiers')
                            relatedIdentifier = ET.SubElement(relatedIdentifiers, 'relatedIdentifier')
                            relatedIdentifier.text = related_identifier
                        else:
                            relatedIdentifier = ET.SubElement(relatedIdentifiers, 'relatedIdentifier')
                            relatedIdentifier.text = related_identifier
                    else:
                        pass
                except:
                    pass
                try:
                    related_identifier_type = element['relatedIdentifierType'].strip()
                    if related_identifier_type:
                        relatedIdentifier.set('relatedIdentifierType', alternative_identifier_type)
                except:
                    pass
                try:
                    relation_type = element['relationType'].strip()
                    if relation_type:
                        relatedIdentifier.set('relationType', relation_type)
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
                    if description_csv:
                        descriptions = ET.SubElement(resource, 'descriptions')
                        description = ET.SubElement(descriptions, 'description')
                        description.set('descriptionType', description_type)
                        description.text = description_csv
                except:
                    pass
                try:
                    geo_location_place = element['geoLocationPlace'].strip()
                    if geo_location_place:
                        geo_locations_loop = geo_locations_loop + 1
                        if geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
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
                        if geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationPoint = ET.SubElement(geoLocation, 'geoLocationPoint')
                            geoPointLongitude = ET.SubElement(geoLocationPoint , 'pointLongitude')
                            geoPointLatitude = ET.SubElement(geoLocationPoint , 'pointLatitude')
                            geoPointLongitude.text =  point_longitude
                            geoPointLatitude.text = point_latitude
                        else:
                            geoLocationPoint = ET.SubElement(geoLocation, 'geoLocationPoint')
                            geoPointLongitude = ET.SubElement(geoLocationPoint , 'pointLongitude')
                            geoPointLatitude = ET.SubElement(geoLocationPoint , 'pointLatitude')
                            geoPointLongitude.text =  point_longitude
                            geoPointLatitude.text = point_latitude
                except:
                    pass
                try:
                    westbound_longitude = element['westBoundLongitude'].strip()
                    eastbound_longitude = element['eastBoundLongitude'].strip()
                    southbound_latitude = element['southBoundLatitude'].strip()
                    northbound_latitude = element['northBoundLatitude'].strip()
                    if westbound_longitude and eastbound_longitude and southbound_latitude and northbound_latitude:
                        geo_locations_loop = geo_locations_loop + 1
                        if geo_locations_loop == 1:
                            geoLocations = ET.SubElement(resource, 'geoLocations')
                            geoLocation = ET.SubElement(geoLocations, 'geoLocation')
                            geoLocationBox = ET.SubElement(geoLocation, 'geoLocationBox')
                            westBoundLongitude = ET.SubElement(geoLocationBox,'westBoundLongitude')
                            eastBoundLongitude = ET.SubElement(geoLocationBox, 'eastBoundLongitude')
                            southBoundLatitude = ET.SubElement(geoLocationBox, 'southBoundLatitude')
                            northBoundLatitude = ET.SubElement(geoLocationBox, 'northBoundLatitude')
                            westBoundLongitude.text = westbound_longitude
                            eastBoundLongitude.text = eastbound_longitude
                            southBoundLatitude.text = southbound_latitude
                            northBoundLatitude.text = northbound_latitude
                        else:
                            geoLocationBox = ET.SubElement(geoLocation, 'geoLocationBox')
                            westBoundLongitude = ET.SubElement(geoLocationBox,'westBoundLongitude')
                            eastBoundLongitude = ET.SubElement(geoLocationBox, 'eastBoundLongitude')
                            southBoundLatitude = ET.SubElement(geoLocationBox, 'southBoundLatitude')
                            northBoundLatitude = ET.SubElement(geoLocationBox, 'northBoundLatitude')
                            westBoundLongitude.text = westbound_longitude
                            eastBoundLongitude.text = eastbound_longitude
                            southBoundLatitude.text = southbound_latitude
                            northBoundLatitude.text = northbound_latitude
                except:
                    pass
                try:
                    polygon_long = element['polyPointLongitude']
                    polygon_lat = element ['polyPointLatitude']
                    geo_location_polygon = element['geoLocationPolygon'].strip()
                    if geo_location_polygon:
                        geo_locations_loop = geo_locations_loop + 1
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
                            print(no)
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
                    if funder_identifier:
                        funderIdentifier = ET.SubElement(fundingReference, 'funderIdentifier')
                        funderIdentifier.text = funder_identifier
                        funderIdentifier.set('funderIdentifierType', funder_identifier_type)
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
                        awardTitle.set('awardURI', award_uri)
                except:
                    pass
            else:
                pass


        tree = ET.ElementTree(resource)
        xmlfile = 'dataCite_'+x+'.xml'
        tree.write(open(xmlfile, 'wb'))
        print('XML document for {} request created, saved as {}.'.format(x, xmlfile))
        print()
print('Script finished')
