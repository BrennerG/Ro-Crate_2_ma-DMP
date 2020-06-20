import json
import sys

class DMP_Constructor:

    def __init__(self, rocrate_PATH):
        self.RO_Crate = self.read(rocrate_PATH)
        self.dmp = None

    def read(self, path:str):
        with open(path) as json_file:
            data = json.load(json_file)
            return data['@graph']

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
    
    def construct(self):
        self.dmp = self.dmp_skeleton()
        self.set_base_attributes()
        person_list = self.extract_people()
        self.dmp['contact']  = person_list[0]
        self.dmp['contributors'] = person_list[1:]
        self.dmp['dataset'] = self.extract_dataset()
    
    def dmp_skeleton(self):
        return {
            'dmp': {
                # base fields
                'title' : None,
                'dmp_id' : None,
                'created' : None,
                'description' : None,
                'language' : None,
                'modified' : None,
                'ethical_issues_description' : None,
                'ethical_issues_exist' : None,

                # Big ones
                'contact' : {},
                'contributor' : [],
                # 'cost' : [], TODO is this really lost?
                'project' : [],
                'dataset' : []
            }
        }

    def set_base_attributes(self):
        # find root entity
        for entity in self.RO_Crate:
            if '@type' in entity and entity['@type'] == "CreativeWork":
                pass

        # 'title' : None,
        # 'dmp_id' : None,
        # 'created' : None,
        # 'description' : None,
        # 'language' : None,
        # 'modified' : None,
        # 'ethical_issues_description' : None,
        # 'ethical_issues_exist' : None,
        pass


    def extract_people(self):
        contributors = []
        for entity in self.RO_Crate:
            if '@type' in entity and entity['@type'] == 'Person':
                contributors.append({
                    'contact_id' : {
                        'type' : "orcid", # TODO check wether this really is orcid
                        'identifier' : self.check('@id', entity)
                    },
                    'mbox' : self.check('email', entity),
                    'name' : self.check('name', entity)
                })

        return contributors

    def extract_project(self):
        pass

    def extract_dataset(self):
        data = []
        for entity in self.RO_Crate:
            if '@type' in entity and entity['@type'] == "Dataset":
                data.append({
                    'title' : self.check("name", entity),
                    'type' : self.check("encodingFormat", entity),
                    'dataset_id' : {
                        'identifier' : self.check("@id", entity),
                        'type' : 'doi' # TODO check this properly
                    },
                    'description' : self.check("description", entity),
                    'issued' : self.check('datePublished', entity),
                    'keyword' : self.check("keywords", entity), # TODO unsure if "keywords" is name
                    'language' : self.check("Language", entity),
                    #  # TODO can the following even be retrieved ?
                    # 'personal_data' : None,
                    # 'preservation_statement' : None,
                    # 'sensitive_data' : None
                })

        return data


if __name__ == "__main__":
    ro1 = 'samples/ro-crate-metadata1.jsonld' 
    ro2 = 'samples/ro-crate-metadata2.jsonld' 
    ro3 = 'samples/ro-crate-metadata3.jsonld' 
    out = 'transformation1.jsonld'

    DC = DMP_Constructor(ro1)
    DC.construct()

    print("DONE")