# RO-Crate & maDMP Parser
TODO general
TODO missing fields -> maDMP is still in there
TODO identifiers -> provide link

## Usage
TODO shellscript

## Mapping maDMP to RO-Crate
TODO mapping of super entities

### dmp attributes
maDMP           | RO-Crate      
-------------   | -------------
title   | [schema.org/name](http://schema.org/name)
dmp_id  | @id (type omitted) 
created | [schema.org/dateCreated](http://schema.org/dateCreated)
description | [schema.org/description](http://schema.org/description)
language    | [schema.org/Language](http://schema.org/Language)
modified    | [schema.org/dateModified](http://schema.org/dateModified)
ethical_issues_description  | -
ethial_issues_exist | -

### project
maDMP           | RO-Crate      
-------------   | -------------
title   | [schema.org/name](http://schema.org/name)
description     | [schema.org/description](http://schema.org/description)
start   | [schema.org/startDate](http://schema.org/startDate)
end     | [schema.org/endDate](http://schema.org/endDate)
funding | distinct entity ([documentation](https://researchobject.github.io/ro-crate/1.0/#funding-and-grants))

### project.funding
maDMP           | RO-Crate      
-------------   | -------------
funder_id   | @id (type omitted)
funding_status  | - 
grant_id    | @id (type omitted)

### contact
maDMP           | RO-Crate      
-------------   | -------------
contact_id  | @id (type omitted)
mbox    | [schema.org/email](http://schema.org/email)
name    | [schema.org/name](http://schema.org/name)

### contributor
maDMP           | RO-Crate      
-------------   | -------------
contact_id  | @id (type omitted)
mbox    | [schema.org/email](http://schema.org/email)
name    | [schema.org/name](http://schema.org/name)
role | [schema.org/Role](http://schema.org/Role)

### cost
omitted

### dataset
maDMP           | RO-Crate      
-------------   | -------------
title   | [schema.org/name](http://schema.org/name)
description     | [schema.org/description](http://schema.org/description)
type | [schema.org/encodingFormat](http://schema.org/encodingFormat)
data_quality_assurance  | -
dataset_id  | @id (omit type)
description | [schema.org/description](http://schema.org/description)
issued  | [schema.org/dateCreated](http://schema.org/dateCreated)
keyword | distinct entity [documentation](https://researchobject.github.io/ro-crate/1.0/#subjects--keywords)
language    | [schema.org/Language](http://schema.org/Language)
personal_data   | - 
preservation_statement  | -
sensitive_data  | -

### dataset.distribution
maDMP           | RO-Crate      
-------------   | -------------
title   | [schema.org/name](http://schema.org/name)
description     | [schema.org/description](http://schema.org/description)
access_url  | [schema.org/URL](http://schema.org/URL)
available_until | [schema.org/endDate](http://schema.org/endDate)
byte_size   | [schema.org/contentSize](http://schema.org/contentSize)
data_access | [schema.org/URL](http://schema.org/URL)
download_url    | [schema.org/downloadUrl](http://schema.org/downloadUrl)
format  | [schema.org/encodingFormat](http://schema.org/encodingFormat)
license | distinct entity [documentation](https://researchobject.github.io/ro-crate/1.0/#licensing-access-control-and-copyright)
metadata | distinct entity [documentation](https://researchobject.github.io/ro-crate/1.0/#metadata-license)
host    | distinct entity [documentation](https://researchobject.github.io/ro-crate/1.0/#digital-library-and-repository-content)
security and privacy    | omitted
technical resource  | distinct entity [for equipment](https://researchobject.github.io/ro-crate/1.0/#provenance-equipment-used-to-create-files), [for software](https://researchobject.github.io/ro-crate/1.0/#provenance-software-used-to-create-files)

### dataset.distribution.license
maDMP           | RO-Crate      
-------------   | -------------
license_ref | @id
start_date  | [schema.org/startDate](http://schema.org/startDate)
start_date -> schema:startDate

### dataset.distribution.host
maDMP           | RO-Crate      
-------------   | -------------
availability    | -
backup__frequency   | -
backup_type | -
certified_with | -
description | [schema.org/description](http://schema.org/description)
host_geo_location   | [schema.org/location](http://schema.org/location)
pid_system  | -
storage_type    | -
support_versioning  | -
url | [schema.org/URL](http://schema.org/URL)
title   | [schema.org/name](http://schema.org/name)

### dataset.metadata
maDMP           | RO-Crate      
-------------   | -------------
description | [schema.org/description](http://schema.org/description)
language    | [schema.org/Language](http://schema.org/Language)
metadata_standard_id    | [schema.org/encodingFormat](http://schema.org/encodingFormat)

## DMP Reference
    dmp
        contact
            contact_id
                identifier
                type
            mbox
            name
        contributor
            contributor_id
                identifier
                type
            mbox
            name
            role
        cost
            currency_code
            description
            title
            value
        created
        dataset
            data_quality_assurance
            dataset_id
                identifier
                type
            description
            distribution
                access_url
                available_until
                byte_size
                data_access
                description
                download_url
                format
                host
                    availability
                    backup__frequency
                    backup_type
                    certified_with
                    description
                    geo_location
                    pid_system
                    storage_type
                    support_versioning
                    title
                    url
                license
                    license_ref
                    start_date
                title
            issued
            keyword
            language
            metadata
                description
                language
                metadata_standard_id
                    identifier
                    type
            personal_data
            preservation_statement
            security_and_privacy
                description
                title
            sensitive_data
            technical_resource
                description
                name
            title
            type
        description
        dmp_id
            identifier
            type
        ethical_issues_description
        ethical_issues_exist
        ethical_issues_report
        language
        modified
        project
            description
            end
            funding
                funder_id
                    identifier
                    type
                funding_status
                grant_id
                    identifier
                    type
            start
            title
        title

## Related Links
[Ro-Crate](https://researchobject.github.io/ro-crate/1.0/)  
[RDA ma-DMPs](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)  
[Ro-Crate JSON-LD context](https://researchobject.github.io/ro-crate/1.0/context.jsonld)  