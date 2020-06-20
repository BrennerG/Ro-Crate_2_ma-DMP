import json
import sys

class RO_Crate_constructor:

    def __init__(self, madmp_PATH):
        self.PATH = madmp_PATH
        self.maDMP = self.read(madmp_PATH)
        self.RO_Crate = self.rocrate_base()

        # LOCATIONS
        self.BASE = self.maDMP
        self.CONTACT = self.maDMP['contact']

        if 'project' in self.maDMP:
            self.PROJECT = self.maDMP['project']

        if 'dataset' in self.maDMP:
            self.DATASET = self.maDMP['dataset']


    def read(self, path:str):
        with open(path) as json_file:
            data = json.load(json_file)
            return data['dmp']

    def rocrate_base(self):
        return {
            "@context": "https://w3id.org/ro/crate/1.0/context", 
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.jsonld",
                    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.0"},
                    "about": {"@id": "./"}
                }
            ]
        }

    def add(self, entity, clean=True):
        if type(entity) == dict:
            if clean:
                clean = {}
                for k in entity:
                    if type(k) != dict and entity[k] != None:
                        clean[k] = entity[k]
                self.RO_Crate['@graph'].append(clean)
            else:
                self.RO_Crate['@graph'].append(entity)
        elif type(entity) == list:
            for ent in entity:
                self.add(ent)


    def check(self, key:str, pos:dict, l2_pos:str=None):
        if l2_pos:
            if l2_pos in pos and key in pos[l2_pos]:
                return pos[l2_pos][key]
        else:
            if key in pos:
                return pos[key]
            else:
                # TODO more precise location output
                print("WARNING: could not find", key)
    

    def extract_contact(self):
        orcid = self.check('identifier', self.CONTACT['contact_id'])
        name = self.check('name', self.CONTACT)
        email = self.check('mbox', self.CONTACT)

        # TODO additional attributes?

        return {
            "@type": "Person",
            "@id": orcid,
            "name": name,
            "email": email
        }

    def extract_dmp_base(self):
        title = self.check('title', self.BASE)
        dmp_id = self.check('identifier', self.BASE['dmp_id'])
        description = self.check('description', self.BASE)
        created = self.check('created', self.BASE)
        language = self.check('language', self.BASE)
        modified = self.check('modified', self.BASE)

        # TODO where to put these 2?
        ethical_issues_description = self.check('ethical_issues_description', self.BASE)
        ethical_issues_exist = self.check('ethical_issues_exist', self.BASE)

        return {
            "@id": dmp_id,
            "@type": "File",
            "encodingFormat": "RDA ma-DMP",
            "fileFormat": "http://www.nationalarchives.gov.uk/PRONOM/Format/proFormatSearch.aspx?status=detailReport&id=1617",
            "path": self.PATH,
            "name": title,
            "description": description,
            "dateCreated": created,
            "Language": language,
            "dateModified": modified,
        }

    def extract_project_funding(self):
        entities = []

        for proj in self.PROJECT:

            # extract project information
            title = self.check('title', proj)
            description = self.check('description', proj)
            start = self.check('start', proj)
            end = self.check('end', proj)

            # extract funding information
            funder_id = self.check('funder_id', proj, 'funding')

            # append project
            entities.append({
                # TODO what about the project id -> dmp_id???
                # "@id": "https://eresearch.uts.edu.au/projects/provisioner",
                "@type": "Organization",
                "name": title,
                "description": description,
                "startDate": start,
                "endDate": end,
                "funder": [
                    {
                    "@id": funder_id
                    }
                ]
            })

            # append funder
            entities.append({
                "@id": funder_id,
                "@type": "Organisation",
                # TODO is there really no funders name in madmp ?!
                # "name": "University of Technology Sydney"
            })

        return entities

    def extract_contributors(self):
        pass

    def extract_cost(self):
        pass

    def extract_dataset(self):
        entities = []

        for dset in self.DATASET:

            # dataset base attributes
            dataset_id = self.check('identifier', dset, 'dataset_id')
            dtype = self.check('type', dset)
            title = self.check('title', dset)
            description = self.check('description', dset)
            issued = self.check('issued', dset)
            language = self.check('language', dset)

            # TODO what to do with these entries?
            sensitive_data = self.check('sensitive_data', dset)
            personal_data = self.check('personal_data', dset)
            preservation_statement = self.check('preservation_statement', dset)
            data_quality_assurance = self.check('data_quality_assurance ', dset)
            # TODO https://researchobject.github.io/ro-crate/1.0/#subjects--keywords
            keyword = self.check('keyword', dset)

            # distribution attributes (dropped: title, description, data_access, format)
            access_url = self.check('access_url', dset, 'distribution')
            download_url = self.check('download_url', dset, 'distribution')
            available_until = self.check('available_until', dset, 'distribution')
            byte_size = self.check('byte_size', dset, 'distribution')

            # license attributes
            licenses = []

            if self.check('distribution', dset) and 'license' in dset['distribution'][0]:
                for lic in self.check('license', dset['distribution'][0]):
                    license_ref = self.check('license_ref', lic)
                    start_date = self.check('start_date', lic)

                    licenses.append({
                        "@id": license_ref,
                        "@type": "CreativeWork",
                        "startDate": start_date
                    })
 
            # TODO metadata
            # TODO host
            # TODO security and privacy
            # TODO technical resource

            # append datasets
            entities.append({
                "@id": dataset_id,
                # TODO distinguish Files from Folders
                "@type": "File",
                # TODO more like this: "encodingFormat": ["text/plain", {"@id": "https://www.commonwl.org/v1.0/Workflow.html"}]
                "encodingFormat": dtype,
                "description": description,
                "contentSize": byte_size,
                "Language" : language,
                "dateCreated" : issued,
                "URL": access_url,
                "downloadUrl": download_url,
                "endDate": available_until,
                "license": licenses,
                # 'metadata': {
                    #"@id": "pics/2017-06-11%2012.56.14.jpg",
                    #"@type": "File",
                    #"encodingFormat": "image/jpeg",
                    #"Language": metadata_language,
                    #"description": "Depicts a fence at a disused motor racing venue with the front part of a slightly out of focus black dog in the foreground.",
                #},
            })

        return entities

    def construct(self):
        self.add(self.extract_dmp_base())
        self.add(self.extract_contact())
        self.add(self.extract_project_funding())
        # TODO contributors
        # TODO cost -> no equivalence in RO-Crate
        self.add(self.extract_dataset())
        return self.RO_Crate

    def write(self, output_PATH:str="ro-crate-metadata.jsonld"):
        with open(output_PATH, 'w') as file:
            json.dump(self.RO_Crate, file)

# MAIN
if __name__ == "__main__":
    in_PATH = 'samples/maDMP3.json'
    out_PATH = 'transformation3.jsonld'

    RCC = RO_Crate_constructor(in_PATH)
    rocrate = RCC.construct()
    RCC.write(out_PATH)

    print("DONE")