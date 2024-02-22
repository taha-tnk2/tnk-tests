import sys
sys.path.append('/Users/tahaakbarally/Documents/TNK/tnkai/')

import math
import json
from lookup import Lookup
from embeddable import Embeddable, Similarity
from clientWrapper import ClientWrapper

"""
A bunch of nonsense
"""
class DigitalPersonality(Embeddable):

    # Initializes the class.
    def __init__(self, name : str, description : str, client : ClientWrapper):
        self.description = description
        super().__init__(name, client)

    # The string that will be called to be embedded.
    @property
    def embed_text(self):
        return self.description

"""
A bunch of nonsense
"""
class Application(Embeddable):

    # Initializes the class.
    def __init__(self, app_code : Lookup, client : ClientWrapper):
        self.app_code = app_code
        super().__init__(self.app_code.name, client)

    # The string that will be called to be embedded.
    @property
    def embed_text(self):
        if ("ideal_user" not in self.__dict__):
            self.get_ideal_user()
        return self.ideal_user

    # Prompts for the ideal user of this application.
    def get_ideal_user(self):
        self.prompt = "Can you please describe the kind of job that would need to use applications such as {0} in their work".format(self.name)
        self.response = self.client.get_response(self.prompt)
        self.ideal_user = self.response.choices[0].message.content

"""
A bunch of nonsense
"""
class Job(Embeddable):

    # Initializes the class.
    def __init__(self, industry_code : Lookup, role_code : Lookup, client : ClientWrapper, digital_personalities : list = None, applications : list = None):
        self.industry_code = industry_code
        self.role_code = role_code
        super().__init__("(" + self.industry_code.name + ":" + self.role_code.name + ")", client)
        
        if (digital_personalities != None):
            self.dtypes = Similarity(self, digital_personalities, truncate=math.inf)
        if (applications != None):
            self.apps = Similarity(self, applications, truncate=3)

    # The string that will be called to be embedded.
    @property
    def embed_text(self):
        if ("description" not in self.__dict__):
            self.get_description()
        return self.description

    # Prompts for a description of this job.
    def get_description(self):
        self.prompt = "Can you please describe the kind of work done by someone in the field of {0} does, where there role is primarily {1}".format(self.industry_code.name, self.role_code.name)
        self.response = self.client.get_response(self.prompt)
        self.description = self.response.choices[0].message.content


def embed_digital_personalities(client : ClientWrapper, max_iter = math.inf):
    digital_personalities = []
    dtypes = [
        { "name" : "Orchestrator", "desc" : "Uses technology to plan, manage and organise activities and tasks and monitor progress." },
        { "name" : "Explorer", "desc"  : "Uses technology to aggregate and interpret data from multiple sources to gain insights."},
        { "name" : "Communicator", "desc"  : "Uses technology to communicate with others and seek for opportunity to build relationships in various channels."},
        { "name" : "Supporter", "desc"  : "Uses technology to complete daily administration tasks, track, share information from multiple sources and collaborate with others."}
    ]
    for i in range(min(max_iter, len(dtypes))):
        digital_personalities.append(DigitalPersonality(dtypes[i]["name"], dtypes[i]["desc"], client))
        print(digital_personalities[i])
    return digital_personalities

def embed_applications(client : ClientWrapper, max_iter = math.inf):
    applications = []
    app_codes = Lookup.get_application_codes()
    for i in range(min(max_iter, len(app_codes))):
        applications.append(Application(app_codes[i], client))
        print(applications[i])
    return applications

def embed_jobs(client : ClientWrapper, digital_personalities : list = None, applications : list = None, max_iter = math.inf):
    jobs = []
    job_codes = Lookup.get_all_job_codes()
    for i in range(min(max_iter, len(job_codes))):
        jobs.append(Job(job_codes[i][0], job_codes[i][1], client, digital_personalities, applications))
        print(jobs[i])
    return jobs


def main():
    client = ClientWrapper(limit=False)
    digital_personalities = embed_digital_personalities(client, math.inf)
    applications = embed_applications(client, math.inf)
    jobs = embed_jobs(client, digital_personalities, applications, 100)
    
    data = {}
    for job in jobs:
        print(job.name, job.dtypes.rounded, job.apps.ordered)
        dtypes = [[val[0].name, val[1]] for val in job.dtypes.rounded]
        ordered_apps = [val[0].name for val in job.apps.ordered]
        data[job.role_code.id] = {
            "name" : job.name,
            "industry_code" : job.industry_code.id,
            "role_code" : job.role_code.id,
            "digital_personalities" : dtypes,
            "predicted_applications" : ordered_apps,
            }
    
    # apps_dict = {}
    # for app in applications:
    #     apps_dict[app.app_code.id] = app.__dict__
    # with open('embedded_apps.json', 'w', encoding='utf-8') as f:
    #     json.dump(apps_dict, f, ensure_ascii=False, indent=4)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    main()
