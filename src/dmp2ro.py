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
        else:
            self.PROJECT = []

        if 'dataset' in self.maDMP:
            self.DATASET = self.maDMP['dataset']

        if 'contributor' in self.maDMP:
            self.CONTRIBUTOR = self.maDMP['contributor']


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
                    if type(k) != dict and entity[k] != None and len(entity) > 1:
                        clean[k] = entity[k]
                self.RO_Crate['@graph'].append(clean)
            else:
                self.RO_Crate['@graph'].append(entity)
        elif type(entity) == list:
            for ent in entity:
                self.add(ent)


    def check(self, key:str, pos:dict, l2_pos:str=None):
        if l2_pos and pos:
            if l2_pos in pos and key in pos[l2_pos]:
                return pos[l2_pos][key]
        else:
            if pos and key in pos:
                return pos[key]
            else:
                print("WARNING: could not find", key)
    

    def extract_contact(self):
        orcid = self.check('identifier', self.CONTACT['contact_id'])
        name = self.check('name', self.CONTACT)
        email = self.check('mbox', self.CONTACT)

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

        # TODO where to put:
        # ethical_issues_description = self.check('ethical_issues_description', self.BASE)
        # ethical_issues_exist = self.check('ethical_issues_exist', self.BASE)

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

    def extract_project_funding_R(self, project=None):
        if project == None:
            project = self.PROJECT

        entities = []

        if type(project) == list:
            for proj in project:
                for ent in self.extract_project_funding_R(proj):
                    entities.append(ent)

        elif type(project) == dict:
            # extract project information
            title = self.check('title', project)
            description = self.check('description', project)
            start = self.check('start', project)
            end = self.check('end', project)

            # extract funding information
            funder_id = self.check('funder_id', project, 'funding')

            # append project
            entities.append({
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
            })
        
        return entities

    def extract_contributors(self):
        contributors = []

        for con in self.CONTRIBUTOR:
            contributors.append({
                "@type": "Person",
                "@id": self.check('identifier', con, 'contributor_id'),
                "name": self.check('name', con),
                "email": self.check('email', con),
                "Role": self.check('role', con)
            })

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
            keywords = self.check('keywords', dset)
            # TODO where to put:
            # sensitive_data = self.check('sensitive_data', dset)
            # personal_data = self.check('personal_data', dset)
            # preservation_statement = self.check('preservation_statement', dset)
            # data_quality_assurance = self.check('data_quality_assurance ', dset)

            # distribution attributes (dropped: description, data_access, format, title)
            access_url = self.check('access_url', dset, 'distribution')
            download_url = self.check('download_url', dset, 'distribution')
            available_until = self.check('available_until', dset, 'distribution')
            byte_size = self.check('byte_size', dset, 'distribution')

            # license attributes
            licenses = []
            if self.check('distribution', dset) and type(dset['distribution']) == list and 'license' in dset['distribution'][0]:
                for lic in self.check('license', dset['distribution'][0]):
                    license_ref = self.check('license_ref', lic)
                    start_date = self.check('start_date', lic)

                    licenses.append({
                        "@id": license_ref,
                        "@type": "CreativeWork",
                        "startDate": start_date
                    })
            elif self.check('distribution', dset) and self.check('license', dset, 'distribution'):
                    license_ref = self.check('license_ref', dset['distribution']['license'])
                    start_date = self.check('start_date', dset['distribution']['license'])

                    licenses.append({
                        "@id": license_ref,
                        "@type": "CreativeWork",
                        "startDate": start_date
                    })

            # metadata attributes
            metadata = self.check('metadata', dset)
            metad_description = self.check('description', metadata)
            metad_language = self.check('language', metadata)
            metad_encodingFormat= self.check('identifier', metadata, 'metadata_standard_id')

            # host attributes
            host = self.check('host', dset)
            host_url = self.check('host_url', host)
            host_title = self.check('host_title', host)
            host_description = self.check('host_description', host)
            host_geo_location = self.check('host_geo_location', host)
            # TODO where to put:
            # host_availability = self.check('host_availability', host)
            # host_backup_frequency = self.check('host_backup_frequency', host) 
            # host_backup_type = self.check('host_backup_type', host)
            # host_certified_with = self.check('host_certified_with', host)
            # host_pid_system = self.check('host_pid_system', host)
            # host_storage_type = self.check('host_storage_type', host)
            # host_support_versioning = self.check('host_support_versioning', host)

            # append datasets
            entities.append({
                "@id": dataset_id,
                "@type": "Dataset",
                "encodingFormat": dtype,
                "name": title,
                "description": description,
                "contentSize": byte_size,
                "Language" : language,
                "dateCreated" : issued,
                "URL": access_url,
                "downloadUrl": download_url,
                "endDate": available_until,
                "license": licenses,
                "keywords": keywords,
                'metadata': {
                    "@type": "File",
                    "encodingFormat": metad_encodingFormat,
                    "Language": metad_language,
                    "description": metad_description
                },
            })

            # append repositories
            entities.append({
                "@id": host_url,
                "@type": "RepositoryCollection",
                "title":  host_title,   
                "description": host_description,
                "location" : host_geo_location,
            })

        return entities

    def construct(self):
        self.add(self.extract_dmp_base())
        self.add(self.extract_contact())
        self.add(self.extract_project_funding_R())
        self.add(self.extract_contributors())
        self.add(self.extract_dataset())
        return self.RO_Crate

    def write(self, output_PATH:str="ro-crate-metadata.jsonld"):
        with open(output_PATH, 'w') as file:
            json.dump(self.RO_Crate, file)

# MAIN
if __name__ == "__main__":
    ex1 = 'samples/ex1-header-fundedProject.json'
    ex2 = 'samples/ex2-dataset-planned.json'
    ex3 = 'samples/ex3-dataset-finished.json'
    ex4 = 'samples/ex4-dataset-embargo.json'
    ex9 = 'samples/ex9-dmp-long.json'
    in_PATH = ex9
    out_PATH = 'transformation_ex9.jsonld'

    RCC = RO_Crate_constructor(in_PATH)
    rocrate = RCC.construct()
    RCC.write(out_PATH)

    print("DONE")