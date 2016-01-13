# -*- coding: utf-8 -*-
import webapp2
import urllib

import json

import codecs
from google.appengine.ext import ndb

class Region(ndb.Model):
    name = ndb.StringProperty()

class Town(ndb.Model):
    name = ndb.StringProperty()
    region_key = ndb.KeyProperty()

class University(ndb.Model):
    name = ndb.StringProperty()
    telephone = ndb.StringProperty()
    site_url = ndb.StringProperty()
    address = ndb.StringProperty()
    town_key = ndb.KeyProperty()

class College(ndb.Model):
    name = ndb.StringProperty()
    telephone = ndb.StringProperty()
    site_url = ndb.StringProperty()
    address = ndb.StringProperty()
    town_key = ndb.KeyProperty()

class UniversitySpeciality(ndb.Model):
    university_key = ndb.KeyProperty()
    prise = ndb.IntegerProperty()
    scores = ndb.IntegerProperty()
    speciality_type_key = ndb.KeyProperty()
    form = ndb.StringProperty()
    cualification = ndb.StringProperty()

class SpecialityTypeUniversity(ndb.Model):
    name = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):

        i = 5

class ParseJson(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = json.loads(self.request.body)
        region_name = self.insert_regions(data)
        self.insert_towns(data, region_name)
        self.insert_universities(data)
        self.insert_specialities_universities(data)
        self.insert_colleges(data)

    def insert_regions(self, data):
        region = Region(name=data['name'])
        region.key = ndb.Key(Region, data['name'])
        region.put()
        return region.name

    def insert_towns(self, data, region_name):
        unique_town_names = set()

        for university in data['universities']:
            unique_town_names.add(university['town'])

        for college in data['colleges']:
            unique_town_names.add(college['town'])

        for name in unique_town_names:
            town = Town(name=name)
            town.region_key = Region.get_or_insert(region_name).key
            town.key = ndb.Key(Town, name)
            town.put()

    def insert_universities(self, data):
        universities = data['universities']
        university_enteries = []
        for university in universities:
            university_entery = University()
            university_entery.name = university['name']
            university_entery.address = university['fullAddress'][1:]
            university_entery.telephone = university['phone']
            university_entery.site_url = university['site']
            university_entery.town_key = Town.get_or_insert(university['town']).key
            university_entery.key = ndb.Key(University, university_entery.name)
            university_enteries.append(university_entery)
            university_entery.put()
        return university_enteries

    def insert_specialities_universities(self, data):
        universities = data['universities']
        for university in universities:
            for speciality in university['special']:
                speciality_type_entery = SpecialityTypeUniversity.get_or_insert(speciality['specialty'],
                                                                      name=speciality['specialty'])
                speciality_entery = UniversitySpeciality()
                speciality_entery.prise = 0
                speciality_entery.scores = 0
                speciality_entery.cualification = speciality['cualification']
                speciality_entery.form = speciality['form']
                speciality_entery.speciality_type_key = speciality_type_entery.key
                speciality_entery.university_key = University.get_or_insert(university['name']).key
                speciality_entery.put()

    def insert_colleges(self, data):
        colleges = data['colleges']
        college_enteries = []
        for college in colleges:
            college_entery = College()
            college_entery.name = college['name']
            college_entery.address = college['fullAddress']
            college_entery.telephone = college['phone']
            college_entery.site_url = college['site']
            college_entery.town_key = Town.get_or_insert(college['town']).key
            college_entery.key = ndb.Key(College, college_entery.name)
            college_enteries.append(college_entery)
            college_entery.put()
        return college_enteries



class DropDataBase(webapp2.RequestHandler):
    def get(self):
        universities = University.query().fetch()
        towns = Town.query().fetch()
        speciality_types = SpecialityTypeUniversity.query().fetch()
        regions = Region.query().fetch()
        universiti_speciality = UniversitySpeciality.query().fetch()

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


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/parse', ParseJson),
    ('/drop', DropDataBase)
], debug=True)


