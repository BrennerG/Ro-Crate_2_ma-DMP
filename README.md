# DS Exercise 2 Notes
[Ro-Crate](https://researchobject.github.io/ro-crate/1.0/)
[RDA ma-DMPs](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)

## TODO
* [x] Research schema.org (JSON-LD)
* [x] Research ro-Crates (1.0)
* [x] Create Github Repo
* [x] Get example 10 maDMPs (5/5)
* [ ] Get example 5 ro-crates
* [ ] Create Mappings (both directions necessary?)
* [ ] DMP to RO-Crate (10x)
* [ ] RO-Crate to DMP (5x)
* [ ] Validate generated maDMP against provided JSON schema
* [ ] Beautify Github
* [ ] License
* [ ] README (table mapping, any assumptions)
* [ ] Zenodo

## Thoughts
[use ro-crate-py ?](https://github.com/ResearchObject/ro-crate-py/tree/master/rocrate)

# RO-Crates
## General
uses [JSON-LD](https://schema.org/)  
core is a metadata file "ro-crate-metadata.jsonld"  
metadatafile should use [JSON-LD Context](https://researchobject.github.io/ro-crate/1.0/context.jsonld)  
A minimal RO-Crate is a directory containing a single RO-Crate Metadata File.  

## Contents of a RO-Crate
<RO-Crate root directory>/  
|   ro-crate-metadata.jsonld            # RO-Crate Metadata File MUST be present  
|   ro-crate-preview.html               # RO-Crate Website homepage MAY be present  
|   ro-crate-preview_files/             # MAY be present  
|    | [other RO-Crate Website files]  
|   [payload files and directories]     # 1 or more SHOULD be present  

## Metadata file
A valid RO-Crate JSON-LD graph MUST describe:  
* The RO-Crate Metadata File Descriptor
* The Root Data Entity (represents RO-Crate as a whole)
* Zero or more Data Entities (Data Set, Content, ...)
* Zero or more Contextual Entities (Entities related to Data Entities)

## Mappings
* [noticable](https://researchobject.github.io/ro-crate/1.0/#additional-metadata-standards)
* RO:File = JSON:MediaObject
* RO:Journal = JSON:Periodical
* RO:Metadata File Descriptor = CreativeWork

# MA-DMPs
## List of sample DMPs
