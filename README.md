# DS Exercise 2 Notes
[Ro-Crate](https://researchobject.github.io/ro-crate/1.0/)  
[RDA ma-DMPs](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)  
[Ro-Crate JSON-LD context](https://researchobject.github.io/ro-crate/1.0/context.jsonld)  

## TODO
* [x] Research schema.org (JSON-LD)
* [x] Research ro-Crates (1.0)
* [x] Create Github Repo
* [x] Get example 10 maDMPs (5/5)
* [x] Get example 5 ro-crates
* [x] Create Mappings (both directions necessary?)
* [x] DMP to RO-Crate (10x)
* [x] RO-Crate to DMP (5x)
* [x] cleanup TODOs
* [x] create CLIent
* [ ] Validate generated maDMP against provided JSON schema
* [x] Make 'manual' comparisons of transformations
* [x] produce clean output
* [ ] Beautify Github
* [x] License
* [ ] README (table mapping, any assumptions)
* [ ] Zenodo

## Thoughts
[use ro-crate-py ?](https://github.com/ResearchObject/ro-crate-py/tree/master/rocrate)  
difference between schema:name & schema:title ?!  

# RO-Crates
## General
uses [JSON-LD](https://schema.org/)  
core is a metadata file "ro-crate-metadata.jsonld"  
metadatafile should use [JSON-LD Context](https://researchobject.github.io/ro-crate/1.0/context.jsonld)  
A minimal RO-Crate is a directory containing a single RO-Crate Metadata File.  

## Contents of a RO-Crate
* <RO-Crate root directory>/  
    - |   ro-crate-metadata.jsonld            # RO-Crate Metadata File MUST be present  
    - |   ro-crate-preview.html               # RO-Crate Website homepage MAY be present  
    - |   ro-crate-preview_files/             # MAY be present  
        - |    | [other RO-Crate Website files]  
    - |   [payload files and directories]     # 1 or more SHOULD be present  

## Metadata file
A valid RO-Crate JSON-LD graph MUST describe:  
* The RO-Crate Metadata File Descriptor (Parent. contains Root Data Entity, Data Entities, Contextual Entities)
* The Root Data Entity (represents RO-Crate as a whole)
    - @type
    - @id
    - name
    - description
    - datePublished
    - license
* Zero or more Data Entities (Data Set, Content, ...)
* Zero or more Contextual Entities (Entities related to Data Entities)

## Mappings
* [noticable](https://researchobject.github.io/ro-crate/1.0/#additional-metadata-standards)
* RO:File = JSON:MediaObject
* RO:Journal = JSON:Periodical
* RO:Metadata File Descriptor = CreativeWork


# Mapping
## DMP -> RO-Crate
* DMP (contains Project, Funding, Contact, ...)
    - title -> schema:name
    - dmp_id -> schema:identifier
    - created -> schema:dateCreated
    - description -> schema:description
    - language -> schema:Language ?
    - modified -> schema:dateModified
    - ethical_issues_description -> ??? put in own ethical entity?
    - ethical_issues_exist -> ??? put in own ethical entity?
 
* Project
    - title -> schema:name
    - description -> schema:description
    - start -> schema:startDate
    - end -> schema:endDate
    - funding [put this here](https://researchobject.github.io/ro-crate/1.0/#funding-and-grants)
        - funder_id
            - identifier -> ORCID / ROR
            - type -> @type:Organization / @type:Person
        - funding_status -> schema:status (is of enumerate type Evenstatus)
        - grant_id [schema/Grant](https://schema.org/Grant)
            - identifier -> Grant/identifier
            - type -> ??? schema:identifier mb even for parent

* Funding [Ro-Crate example](https://researchobject.github.io/ro-crate/1.0/#funding-and-grants)
    same as Project/funding.  
    if those 2 funders are different, create 2 different funder contextual-entities!  

* Contact [Ro-Crate:Person example](https://researchobject.github.io/ro-crate/1.0/#people)
    - contact_id -> schema:identifier
    - mbox -> schema:email
    - name -> schema:name

* Contributor
    same as Contact above, but possibly with multiple entities  

* Cost [schema/MonetaryAmount](https://schema.org/MonetaryAmount)
    - title -> schema:name
    - description -> schema:description
    - currency_code -> schema:currency
    - value -> schema:value

* Dataset (contains Distribution, License, Host, Security, Techical, Metadata)  
    [Referencing Data Entities](https://researchobject.github.io/ro-crate/1.0/#examples-of-referencing-data-entities-files-and-folders-from-the-root-data-entity)   
    - title -> schema:name
    - type  -> ??? String
    - data_quality_assurance -> ??? String
    - dataset_id -> schema:identifier
        - identifier -> above
        - type -> above
    - description -> schema:description
    - issued -> schema:dateCreated
    - keyword -> schema:keywords [more](https://researchobject.github.io/ro-crate/1.0/#subjects--keywords)  
    - language -> schema:Language
    - personal_data -> yes/no/unknown
    - preservation_statement -> ??? String
    - sensitive_data -> yes/no/unknown

* Distribution
    - title -> schema:name
    - description -> schema:description
    - access_url -> ??? URI
    - available_until -> schema:endDate
    - byte_size -> schema:fileSize
    - data_access -> open/shared/closed
    - download_url -> ??? URI ?difference to access_url
    - format -> Pronom_id / schema:encodingFormat

* License [Ro-Crate example](https://researchobject.github.io/ro-crate/1.0/#licensing-access-control-and-copyright)  
    - license_ref -> @id
    - start_date -> schema:startDate

* Host
    - availability -> ??? String
    - backup__frequency -> ??? String
    - backup_type -> ??? String
    - certified_with -> din31644/dini-zertifikat/dsa/iso16363/iso16919/trac/wds/coretrustseal
    - description -> schema:description
    - geo_location -> schema:Country
    - pid_system -> ??? Controlled Vocabulary
    - storage_type -> ??? String
    - support_versioning -> yes/no/unknown
    - title -> schema:name
    - url -> ??? URL

* Security and Privacy
    - description -> schema:description
    - title -> schema:name

* Technical Resource 
    [Equipment](https://researchobject.github.io/ro-crate/1.0/#provenance-equipment-used-to-create-files)  
    [Software](https://researchobject.github.io/ro-crate/1.0/#provenance-software-used-to-create-files)   
    - description -> schema:description
    - name -> schema:name

* Metadata
    [metadata license](https://researchobject.github.io/ro-crate/1.0/#metadata-license)   
    - description -> schema:description
    - language -> schema:Language
    - metadata_standard_id -> schema:identifier (?)
        - identifier -> above
        - type -> above
