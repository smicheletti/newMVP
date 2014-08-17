from django.db import models
from django.contrib.auth.models import User
from venues.models import *
from users.models import *
from events.models import *
from time import time
from tagstar.db.fields import TagsField
from tagstar.models import Tag
from datetime import *


def get_upload_video_name(instance, filename):
    myString = 'videos/%s/%s/%s' % (str(instance.user.id), str(instance.id), filename)
    myString.replace(' ', '_')
    return myString

def get_upload_file_name(instance, filename):
    myString =  'songs/%s/%s/%s' % (str(instance.songOwner.id), str(instance.songName), filename)
    myString.replace(' ', '_')
    return myString

def get_upload_picture_name(instance, filename):
    myString = 'pictures/%s/%s/%s' % (str(instance.uploader.id), str(instance.id), filename)
    myString.replace(' ', '_')
    return myString

def get_upload_cover_name(instance, filename):
    myString =  'pictures/%s/%s' %(str(instance.id), str(instance.name))
    myString.replace(' ', '_')
    return myString

class Adjective(models.Model):
    name = models.CharField(max_length = 25)
    used = models.IntegerField()
    def __unicode__(self):
        return self.name
    

class Region(models.Model):
    name = models.CharField(max_length = 40)
    bandCount = models.IntegerField()
    bands = models.ManyToManyField('Band')
    

class Instrument(models.Model):
    name = models.CharField(max_length = 25)  
    def __unicode__(self):
        return self.name

class Picture(models.Model):
    date = models.DateTimeField(default=datetime.now())
    caption = models.CharField(max_length = 100)
    tags = models.ManyToManyField('tagstar.Tag')
    picture_file = models.FileField(upload_to = get_upload_picture_name )
    uploader = models.ForeignKey('users.userAcc')
    
    def __unicode__(self):
        return self.caption
    
    

    


class Region(models.Model):
    name = models.CharField(max_length = 40)
    tag = models.ForeignKey('tagstar.Tag', related_name = 'identity_tag', null = True)
    def __unicode__(self):
        return self.name
    
    
    
    

class Instrument(models.Model):
    name = models.CharField(max_length = 25)
    tag = models.ForeignKey('tagstar.Tag', related_name = 'identity_tag', null = True)
    def __unicode__(self):
        return self.name
    
class band_member(models.Model):
    name = models.CharField(max_length = 20)
    instruments = models.ManyToManyField('Instrument', related_name = 'Instruments_played', null = True)
    user_related = models.ForeignKey('users.userAcc', null = True)
    
    def __unicode__(self):
        return self.name
        
class Adjective(models.Model):
    name = models.CharField(max_length = 25)
    used = models.IntegerField()
    tag = models.ForeignKey('tagstar.Tag', related_name = 'identity_tag', null = True)
    def __unicode__(self):
        return self.name

    

class Album(models.Model):
    name = models.CharField(max_length = 50)
    collaborators = models.ManyToManyField('Band', related_name = 'featuring')
    songs = models.ManyToManyField('Song', related_name = 'tracks')
    about = models.TextField(null = True)
    cover = models.FileField(upload_to = get_upload_cover_name )
    release_yr = models.ForeignKey('events.Year')
    release_month = models.ForeignKey('events.Month')
    copyright_info = models.TextField(null = True)
    tag_identifiers = models.ManyToManyField('tagstar.Tag', null = True)
    purchase_link = models.URLField(null = True)
    
    def __unicode__(self):
        return self.name


class Video(models.Model):
    date = models.DateTimeField()
    caption = models.CharField(max_length = 100)
    tags = models.ManyToManyField('tagstar.Tag')
    user = models.ForeignKey('users.userAcc')
    video_file = models.FileField(upload_to =get_upload_video_name)
    def __unocode__(self):
        return self.video_file
                                  
class Song(models.Model):
    songName = models.CharField(max_length = 40)
    songOwner = models.ForeignKey('Band')
    audio_track = models.FileField(upload_to = get_upload_file_name)
    written_by = models.ForeignKey('users.userAcc' ,related_name = 'writer')
    tags = models.ManyToManyField('tagstar.Tag')
    produced_by = models.ManyToManyField('users.userAcc')
    part_of_album = models.ForeignKey('Album', related_name = 'track_on', null = True)
    include_on = models.BooleanField(default = False)
    order = models.CharField(max_length = 5)
    def __unicode__(self):
        return self.songName
class YouTube(models.Model):
    url = models.CharField(max_length = 90)
    parsed_code = models.CharField(max_length = 20)
    description = models.TextField(null = True)
    def __unicode(self):
        return self.parsed_code
    
class Status(models.Model):
    text = models.CharField(max_length = 70)
    used = models.IntegerField()
    tag = models.ForeignKey('tagstar.Tag', related_name = 'status_identity_tag', null = True)
    def __unicode__(self):
        return self.text
    
class AlbumStatus(models.Model):
    text = models.CharField(max_length = 70)
    used = models.IntegerField()
    tag = models.ForeignKey('tagstar.Tag', related_name = 'album_status_identity_tag', null = True)
    def __unicode__(self):
        return self.text

class Post(models.Model):
    date = models.DateTimeField()
    text = models.TextField()
    user = models.ForeignKey('users.userAcc')
    tags = models.ManyToManyField('tagstar.Tag')
    pictures = models.ManyToManyField('Picture')
    video = models.ManyToManyField('Video')
    def __unicode__(self):
        return self
    


class Base(models.Model):
    name = models.CharField(max_length = 40)
    description = models.TextField()
    adjectives = models.ManyToManyField('Adjective', null = True)
    pictures = models.ManyToManyField('Picture', null = True)
    tag_identifier = models.ForeignKey('tagstar.Tag', related_name = 'identity_tag')
    email = models.EmailField()
    events = models.ManyToManyField('events.Event', null = True)
    twitter_handle = models.CharField(max_length = 60, null = True)
    manager = models.ForeignKey('users.userAcc', related_name = 'my_manager')
    posts = models.ManyToManyField('Post')
    users_who_like = models.ManyToManyField('users.userAcc', related_name = 'likers')
    region = models.ManyToManyField('bands.Region', null = True)
    def __unicode__(self):
        return self.name
    
class Band(Base):
    instruments = models.ManyToManyField('Instrument', null = True)
    band_members = models.ManyToManyField('band_member', related_name = 'band_mates')
    status = models.ForeignKey('Status', null = True)
    album_status = models.ForeignKey('AlbumStatus', null = True)
    similar_bands = models.ManyToManyField('Band')
    albums = models.ManyToManyField('Album')
    year_formed = models.ForeignKey('events.Year')
    

class Venue(Base):
    location = models.TextField()
    phone_number = models.CharField(max_length = 12)
    site_link = models.URLField(null = True)
    attire = models.TextField(null = True)
    menu_link = models.URLField(null = True)
    similar_venues = models.ManyToManyField('Venue', null = True)
    
   


    
    


