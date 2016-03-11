# -*- coding: utf-8 -*-
import webapp2
import json
from google.appengine.ext import ndb
import ndbRequests
import checker
import enteries_sets
import urllib, cStringIO


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello")


class ParseJson(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = json.loads(self.request.body)
        region_name = data['region_name']
        towns_and_univers = data['towns']
        self.insert_regions(region_name)

        self.insert_towns(towns_and_univers, region_name)




    def insert_regions(self, region_name):
        region = enteries_sets.Region(name=region_name)
        region.key = ndb.Key(enteries_sets.Region, region_name)
        region.put()

    def insert_towns(self, data, region_name):
        for entry in data:
            town = enteries_sets.Town(name=entry['town_name'], region=region_name)
            town.key = ndb.Key(enteries_sets.Town, town.name)
            town.put()
            self.insert_universities(entry['universities'])


    def insert_universities(self, data):
        for university in data:
            university_to_add = enteries_sets.University(name=university['university_name'])
            university_to_add.address = university['address']
            university_to_add.desctiption = university['description']
            university_to_add.region = university['region']
            university_to_add.telephone = university['phone']
            university_to_add.town = university['town_name']
            university_to_add.logo_url = university['logo_url']
            university_to_add.image_url = university['image_url']
            university_to_add.site_url = university['site_url']
            university_to_add.key = ndb.Key(enteries_sets.University, university_to_add.name +university_to_add.town)
            university_to_add.mean_point, university_to_add.mean_price = self.get_mean_price_and_points(university)
            self.insert_specialities_universities(university_to_add, university['specialities'])
            university_to_add.put()

    def insert_specialities_universities(self, university, data):
        for entery in data:
            speciality = enteries_sets.UniversitySpeciality()
            speciality.name = entery['speciality_name']
            speciality.university = university.name
            speciality.description = entery['description']
            speciality.duration = entery['duration']
            speciality.form = entery['form']
            speciality.places = entery['places']
            speciality.scores = entery['points']
            speciality.prise = entery['price']
            speciality.subjects = entery['subjects']
            enteries_sets.SpecialityTypeUniversity.get_or_insert(speciality.name, name= speciality.name)
            speciality.put()

    def get_mean_price_and_points(self, university):
        try:
            total_price = 0
            total_points = 0
            size = 0
            for speciality in university['specialities']:
                total_points += speciality['points']
                total_price += speciality['price']/1000
                if speciality['points'] > 0:
                    size += 1
            total_points = total_points/size
            total_price = int(round(total_price/size))*1000
            return  total_points, total_price
        except ZeroDivisionError:
            return None, None


class Update(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = json.loads(self.request.body)
        university_key = ndb.Key(data['name'])
        university = enteries_sets.University.get_or_insert(university_key)

        university.logo =   file = cStringIO.StringIO(urllib.urlopen(data['logoUrl']).read())






app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/parse', ParseJson),
    ('/getRegions', ndbRequests.GetRegions),
    ('/getTowns', ndbRequests.GetTowns),
    ('/getUniversities', ndbRequests.GetUniversities),
    ('/getUniversitySpecialities', ndbRequests.GetUniversitySpecialities),
    ('/getSpecialities', ndbRequests.GetSpecialities ),
    ('/drop', ndbRequests.DropDataBase),
    ('/check', checker.Check )
], debug=True)


