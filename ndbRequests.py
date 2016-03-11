__author__ = 'yudzh_000'
# -*- coding: utf-8 -*-
import webapp2
import enteries_sets
import json

class GetRegions(webapp2.RequestHandler):
    def get(self):
        count = int(self.request.get('count', 9999))
        offset = self.request.get('offset', 0)
        json_string = json.dumps([p.to_dict() for p in enteries_sets.Region.query().fetch(limit=count, offset=offset)])
        self.response.write(json_string)

class GetTowns(webapp2.RequestHandler):
    def get(self):
        count = int(self.request.get('count', 9999))
        offset = self.request.get('offset', 0)
        region = self.request.get('region', '')
        if region == '':
            towns = [p.to_dict() for p in enteries_sets.Town.query().fetch(count)]
        else:
            towns = [p.to_dict() for p in enteries_sets.Town.query(enteries_sets.Town.region == region).fetch(limit=count, offset=offset)]
        map(lambda d: d.pop('region'), towns)
        self.response.write(json.dumps(towns))

class GetUniversities(webapp2.RequestHandler):
    def get(self):
        count = int(self.request.get('count', 9999))
        offset = self.request.get('offset', 0)
        town = self.request.get('town', '')
        min_price = self.request.get('min_price', 0)
        max_price = self.request.get('max_price', 1000000000)
        min_points = self.request.get('min_points', 0)
        max_points = self.request.get('max_points', 1000)
        flag = self.request.get('flag', True)
        print(flag)
        if town == '':
            universities = [p.to_dict() for p in enteries_sets.University.query().fetch(count)]
        else:
            if flag:
                universities = [p.to_dict() for p in enteries_sets.University.query(enteries_sets.University.town == town).fetch(limit=count, offset=offset)]
            else:
                universities = [p.to_dict() for p in enteries_sets.University.query(enteries_sets.University.town == town and
                                                                                    enteries_sets.University.mean_point is not None and
                                                                                   min_points <= enteries_sets.University.mean_point <= max_points
                                                                                    and min_price <= enteries_sets.University.mean_price <= max_price).fetch(limit=count, offset=offset)]
        map(lambda d: d.pop('town'), universities)
        self.response.write(json.dumps(universities))

def isBeetween(numb, min, max):
    return min <= numb <= max


class DropDataBase(webapp2.RequestHandler):
    def get(self):
        universities = enteries_sets.University.query().fetch()
        towns = enteries_sets.Town.query().fetch()
        speciality_types = enteries_sets.SpecialityTypeUniversity.query().fetch()
        regions = enteries_sets.Region.query().fetch()
        universiti_speciality = enteries_sets.UniversitySpeciality.query().fetch()


        for region in regions:
            region.key.delete()

        for town in towns:
            town.key.delete()

        for universiti in universities:
            universiti.key.delete()

        for speciality_type in speciality_types:
            speciality_type.key.delete()

        for speciality in universiti_speciality:
            speciality.key.delete()


class GetUniversitySpecialities(webapp2.RequestHandler):
    def get(self):
        count = int(self.request.get('count', 9999))
        offset = self.request.get('offset', 0)
        university = self.request.get('university', '')
        university = university.strip()
        if university == '':
            self.response.write("Пошел нахуй говнокодер, напииши university")
            return
        else:
            specialities = [p.to_dict() for p in enteries_sets.UniversitySpeciality.query(
                enteries_sets.UniversitySpeciality.university == university).fetch(limit=count, offset=offset)]
        map(lambda d: d.pop('university'), specialities)
        self.response.write(json.dumps(specialities))

class GetSpecialities(webapp2.RequestHandler):
    def get(self):
        count = int(self.request.get('count', 9999))
        offset = self.request.get('offset', 0)
        specialities = [p.to_dict() for p in enteries_sets.SpecialityTypeUniversity.query().fetch(limit=count, offset=offset)]
        self.response.write(json.dumps(specialities))
