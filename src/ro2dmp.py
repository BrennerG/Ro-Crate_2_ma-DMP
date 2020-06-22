import json
import sys
from datetime import date

class DMP_Constructor:

    def __init__(self, rocrate_PATH):
        self.RO_Crate = self.read(rocrate_PATH)
        self.dmp = None

    def read(self, path:str):
        with open(path) as json_file:
            data = json.load(json_file)
            return data['@graph']

    def write(self, output_PATH:str="ma_DMP.json"):
        with open(output_PATH, 'w') as file:
            json.dump(self.dmp, file, indent=4)

    def check(self, key:str, pos:dict, l2_pos:str=None):
        if l2_pos:
            if l2_pos in pos and key in pos[l2_pos]:
                return pos[l2_pos][key]
        else:
            if key in pos:
                return pos[key]
            else:
                print("WARNING: could not find", key)
    
    def clean(self, dictionary:dict):
        cleaned = {}

        if type(dictionary) == dict:
            for k in dictionary:
                if dictionary[k] != None:
                    cleaned[k] = dictionary[k]

        elif type(dictionary) == list:
            for dic in dictionary:
                self.clean(dic)

        return cleaned

    def identify(self, identifier:str):
        identifiers = ['doi', 'orcid', 'handle', 'ark', 'isni', 'openid']

        if identifier == None:
            return None

        for ident in identifiers:
            if ident in identifier:
                return ident
            elif identifier.startswith('http') or identifier.startswith('www'):
                return 'url'
                
        return 'other'

    def construct(self, clean:bool=False):
        self.dmp = self.dmp_skeleton()
        self.set_base_attributes()
        person_list = self.extract_people()
        self.dmp['dmp']['contact']  = person_list[0]
        self.dmp['dmp']['contributor'] = person_list[1:]
        self.dmp['dmp']['dataset'] = self.extract_dataset()
        self.dmp['dmp']['project'] = self.extract_project()

        if clean:
            self.dmp['dmp'] = self.clean(self.dmp['dmp'])
    
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
                'cost' : [],
                'project' : [],
                'dataset' : []
            }
        }

    def set_base_attributes(self):
        created = date.today().strftime("%Y/%m/%d")
        self.dmp['dmp']['dmp_id'] = "PLEASE REGISTER A DOI"
        self.dmp['dmp']['title'] = "Machine-Actionable Data Management Plan"
        self.dmp['dmp']['description'] = "This is a machine-generated maDMP. Please fill out missing fields according to RDA maDMP standards."
        self.dmp['dmp']['created'] = created
        self.dmp['dmp']['modified'] = created
        self.dmp['dmp']['language'] = None
        self.dmp['dmp']['ethical_issues_exist'] = None
        self.dmp['dmp']['ethical_issues_description'] = None

    def extract_people(self):
        contributors = []
        for entity in self.RO_Crate:
            if '@type' in entity and entity['@type'] == 'Person':
                contributors.append({
                    'contact_id' : {
                        'identifier' : self.check('@id', entity),
                        'type' : self.identify(self.check('@id', entity))
                    },
                    'mbox' : self.check('email', entity),
                    'name' : self.check('name', entity)
                })

        return contributors

    def extract_project(self):
        projects = []
        for entity in self.RO_Crate:
            if '@type' in entity and (entity['@type'] == 'Project' or (entity['@type'] == 'Organization' and 'funder' in entity)):
                projects.append({
                    'title' : self.check('title', entity),
                    'description' : self.check('description', entity),
                    'start' : None,
                    'funding' : {
                        'funder_id' : {
                            'identifier' : self.check('@id', entity, 'funder'),
                            'type' : self.identify(self.check('@id', entity, 'funder'))
                        }
                    },
                    'funding_status' : None,
                    'grant_id' : {
                        'identifier' : None,
                        'type' : None
                    }
                })

        return projects

    def extract_dataset(self):
        data = []
        for entity in self.RO_Crate:
            if '@type' in entity and entity['@type'] == "Dataset":
                data.append({
                    'title' : self.check("name", entity),
                    'type' : self.check("encodingFormat", entity),
                    'dataset_id' : {
                        'identifier' : self.check("@id", entity),
                        'type' : self.identify(self.check('@id', entity))
                    },
                    'description' : self.check("description", entity),
                    'issued' : self.check('datePublished', entity),
                    'keyword' : self.check("keywords", entity),
                    'language' : self.check("Language", entity),
                    'personal_data' : None,
                    'preservation_statement' : None,
                    'sensitive_data' : None
                })

        return data


if __name__ == "__main__":
    ro1 = 'samples/ro-crate-metadata1.jsonld' 
    ro2 = 'samples/ro-crate-metadata2.jsonld' 
    ro3 = 'samples/ro-crate-metadata3.jsonld' 

    ros = [ro1, ro2, ro3]
    filenames = ['transformation1.jsonld', 'transformation2.jsonld', 'transformation3.jsonld']

    for i in range(0,len(ros)):
        DC = DMP_Constructor(ros[i])
        DC.construct()
        DC.write(filenames[i])

    print("DONE")