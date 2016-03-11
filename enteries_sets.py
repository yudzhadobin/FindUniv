__author__ = 'yudzh_000'


from google.appengine.ext import ndb

class Region(ndb.Model):
    name = ndb.StringProperty()

class Town(ndb.Model):
    name = ndb.StringProperty()
    region = ndb.StringProperty(indexed=True)

class UniversitySpeciality(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    form = ndb.StringProperty()
    description = ndb.TextProperty()
    prise = ndb.IntegerProperty()
    scores = ndb.IntegerProperty()
    places = ndb.IntegerProperty()
    subjects = ndb.StringProperty()
    duration = ndb.StringProperty()
    qualification = ndb.StringProperty()
    university = ndb.StringProperty(indexed=True)

class SpecialityTypeUniversity(ndb.Model):
    name = ndb.StringProperty()


class University(ndb.Model):
    name = ndb.StringProperty()
    telephone = ndb.StringProperty()
    site_url = ndb.StringProperty()
    address = ndb.StringProperty()
    town = ndb.StringProperty()
    region = ndb.StringProperty()
    logo_url = ndb.StringProperty()
    image_url = ndb.StringProperty()
    desctiption = ndb.TextProperty()
    mean_price = ndb.IntegerProperty()
    mean_point = ndb.IntegerProperty()
