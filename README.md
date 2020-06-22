# RO-Crate & maDMP Parser

## Usage
TODO shellscript

## Mapping
### Base Attributes
maDMP         | RO-Crate      
------------- | -------------
title | [name](http://schema.org/name)
Content Cell | Content Cell 

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