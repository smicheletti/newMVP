from django.shortcuts import render, render_to_response
from bands.models import *
from django.http import HttpResponse, HttpResponseRedirect
from forms import *
from django.core.context_processors import csrf
from bands.models import *
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from bands.models import Adjective
from django.template.context import RequestContext
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from datetime import date
from tagstar.models import *
from forms import *
from sets import Set
from users.forms import messageForm
import json
# Create your views here.

#copy this to create bands by region, or bands by attribute

def allBands(request):
        return render_to_response('bands.html',
                              {'bands' : Band.objects.all()}, context_instance = RequestContext(request),)
@login_required
def addFavoriteBand(request, userID, bandID):
    myPerson = User.objects.get(id = userID)
    myPerson.userAcc.favorite_bands.add(Band.objects.get(id = bandID))
    myBand = Band.objects.get(id = bandID)
    myBand.users_who_like.add(myPerson.userAcc)
    return render_to_response('band.html',
                              {'band': myBand, 'adjectives': myBand.adjectives.all(), 'user': request.user})
@login_required
def unlikeBand(request, userID, bandID):
    myPerson = User.objects.get(id = userID)
    myPerson.userAcc.favorite_bands.remove(Band.objects.get(id = bandID))
    myBand = Band.objects.get(id = bandID)
    myBand.users_who_like.remove(myPerson.userAcc)
    return render_to_response('band.html',
                              {'band': myBand, 'adjectives': myBand.adjectives.all(), 'user': request.user})
    
def attribute(request, adjective):
    adjID = Adjective.objects.get(name = adjective)
    mathBands = Band.objects.all()
    newset = []
    for band in mathBands:
        for x in band.adjectives.all():
            if x.name == adjective:
                newset.append(band)
    if (newset):
        return render_to_response('bands.html',
                              {'bands' :newset}, context_instance = RequestContext(request),)
    else:
        return HttpResponseRedirect('/bands/notFound')
    
    
def notFound(request):
    return render_to_response('notFound.html', context_instance = RequestContext(request),)
    
def oneBand(request, bandID):
    myBand = Band.objects.get(id = bandID)
    songs = Song.objects.all().filter(songOwner = myBand).filter(include_on=True)
    messageform = messageForm()
    
    context_instance = RequestContext(request)
    today = set()
    tomorrow = set()
    next_week = set()
    this_month = set()
    for event in myBand.events.all():
        if event.date == datetime.date(datetime.now()):
            today.add(event)
        elif ((event.date > datetime.date(datetime.now())) and (event.date < datetime.date(datetime.now())+timedelta(2))):
            tomorrow.add(event)
        elif ((event.date >= datetime.date(datetime.now())+timedelta(2)) and (event.date <= datetime.date(datetime.now())+timedelta(7))):
            next_week.add(event)
        else:
            this_month.add(event)
    return render_to_response('band.html',
                              {'band': myBand, 'adjectives': myBand.adjectives.all(), 'user': request.user, 'songs' : songs, 'today': today, 'tomorrow': tomorrow,
                               'next_week': next_week, 'this_month': this_month, 'message_form': messageform}, context_instance = RequestContext(request))

def handle_uploaded_file(file_path):
    dest = open(file_path.name, 'wb')
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()
    
    
@login_required
def create(request):
    myUser = request.user
    if  myUser.userAcc.first_name =='':  
        return HttpResponseRedirect('/edit/')
    try:
        c = band_member.objects.get(name = str(myUser.userAcc.first_name + ' ' + myUser.userAcc.last_name))
    except:
        c = None
    if c:
        c = band_member.objects.filter(name = str(myUser.userAcc.first_name + ' ' + myUser.userAcc.last_name))
    else:
        c = band_member(name = str(myUser.userAcc.first_name + ' ' + myUser.userAcc.last_name))
        c.save()
        c = band_member.objects.filter(name = str(myUser.userAcc.first_name + ' ' + myUser.userAcc.last_name))
    if request.POST:
        form = BandForm(request.POST)
        formset = band_member_form_set(request.POST, queryset = c)
        picform = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid() and picform.is_valid():
                this = form.save(commit = False)
                this.manager = myUser.userAcc
                tag_identifier = '#' + this.name
                tag_identifier.replace(' ', '_')
                a = Tag(name = tag_identifier, count = 1)
                a.save()
                this.tag_identifier = a 
                this.album_status = AlbumStatus.objects.get(id = 1)
                that = picform.save(commit = False)
                that.uploader = myUser.userAcc
                that.save()
                handle_uploaded_file(request.FILES['picture_file'])
                this.main_image = that
                this.save()
                for form in formset.forms:
                    thing = form.save(commit = False)
                    thing.save()
                    this.band_members.add(thing)
                    form.save_m2m()
                
                myUser.userAcc.bandsIn.add(this)
                
                myID = str(this.id)
                myURL = '/bands/form_2/' + myID + '/'
                return HttpResponseRedirect(myURL)  
    else:
        
        form = BandForm()
        formset = band_member_form_set(queryset = c)
        picform = ProfilePicForm()    
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['formset'] = formset
    args['picform'] = picform
    return render_to_response('create_band.html', args, context_instance = RequestContext(request))


def form_2(request, bandID):
    myBand = Band.objects.get(id = bandID)
    
    if request.method == 'POST':
        nameform = band_tag_form(request.POST, instance = myBand.tag_identifier)
        infoForm = BandForm2(request.POST, instance = myBand)
        if infoForm.is_valid() and nameform.is_valid():
            this = nameform.save(commit = False)
            this.save()
            that = infoForm.save(commit = False)
            that.save()
            infoForm.save_m2m()
            that.tag = this
            myURL = '/bands/form_3/'+ bandID+ '/999999/'
            return HttpResponseRedirect(myURL)
        else:
            return HttpResponseRedirect('/')
    else:
        args = {}
        args.update(csrf(request))
        args['nameform'] = band_tag_form(instance = myBand.tag_identifier)
        args['infoform'] = BandForm2(request.POST, instance = Band.objects.get(id = bandID))
        args['band'] = Band.objects.get(id = bandID)
        return render_to_response('band_form_2.html', args, context_instance = RequestContext(request))
    
def form_3(request, bandID, albumID):
    myBand = Band.objects.get(id = bandID)
    sing = None
    myBandOther = myBand.name + " 's other songs"
    try:
        Album.objects.get(name = myBandOther)
    except:
        a = Album(name = myBandOther, release_yr = Year.objects.get(year_no = 2014), release_month = Month.objects.get(id = 1))
        a.save()
        myBand.albums.add(a)
    if request.method == 'POST':
        try:
            myAlbum = Album.objects.get(id = albumID)
            albumform = AlbumForm(request.POST,  request.FILES, instance = myAlbum)
            songs = Song.objects.filter(part_of_album = myAlbum)
            songformset = SongFormSet(request.POST, request.FILES, songs)
        except:
             albumform = AlbumForm(request.POST,  request.FILES)
             songformset = SongFormSet(request.POST, request.FILES)
        if albumform.is_valid():
            this = albumform.save(commit = False)
            this.save()
            albumform.save_m2m()
            try:
                myBand.albums.get(name  = this.name)
            except:
                myBand.albums.add(this)
            for form in songformset.forms:
                if form.is_valid():
                    that = form.save(commit = False)
                    if that.songName == '':
                        break
                    that.songOwner = myBand
                    that.written_by = request.user.userAcc
                    that.part_of_album = this
                    that.save()
                    this.songs.add(that)    
                else:
                    pass
                
            myURL = '/bands/form_3/'+ bandID + '/999999/'
            return HttpResponseRedirect(myURL)
        else:
            return HttpResponseRedirect('/')
    else:
        args = {}
        try:
            myAlbum = Album.objects.get(id = albumID)
            albumform = AlbumForm(instance = myAlbum)
            args['albumform'] = albumform
            args['songformset'] = SongFormSet(queryset = myAlbum.songs.all())
        except:
             
            args['albumform'] = AlbumForm()
            args['songformset']= SongFormSet(queryset = Song.objects.none())
        
        args.update(csrf(request))
        args['band'] = myBand
        args['number'] = albumID
        return render_to_response('band_form_3.html', args)

def remove_album(request, bandID, albumID):
    myBand = Band.objects.get(id = bandID)
    myAlbum = Album.objects.get(id = albumID)
    myBand.albums.remove(myAlbum)
    myAlbum.delete()
    myURL = '/bands/form_3/'+ bandID+ '/10000000/'
    return HttpResponseRedirect(myURL)


            
@login_required
def editBand(request, bandID):

    bandName = "#" + Band.objects.get(id= bandID).name
    
    if request.method == 'POST':
        form = bandEditForm(request.POST, instance = Band.objects.get(id = bandID))
       
        if form.is_valid():
            
            this = form.save(commit = False)
            this.save()
            form.save_m2m()
            myURL = '/bands/get/'+ bandID+ '/'
            return HttpResponseRedirect(myURL)
    else:
        band = Band.objects.get(id = bandID)
        form = bandEditForm(instance = band)
        
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['band'] = Band.objects.get(id = bandID)
    return render_to_response('bandprofile.html', args)

def userAdd(user, band):
    user.userAcc.liked_bands.add(band)
    return
@login_required
def editAlbums(request, albumID, bandID):#this edits one album, should include ability to add songs, and to also add a cover photo, and the about section
    myBand = Band.objects.get(id = bandID)
    myAlbum = Album.objects.get(id = albumID)
    
    if request.method == 'POST':
        form = AlbumEditForm(request.POST, request.FILES, instance = myAlbum)
        formset = SongFormSet(request.POST, request.FILES)
        albumform = AlbumForm(request.POST, request.FILES, instance= myAlbum)
        #need to erase the tag thing
        if form.is_valid() and formset.is_valid() and albumform.is_valid():
            this = form.save(commit = False)
            this.save()
            form.save_m2m
            that = albumform.save(commit = False)
            that.save()
            albumform.save_m2m()
            for form in formset.forms:
                this = form.save(commit = False)
                this.songOwner = myBand
                if this.songName == '':
                    break
                    
                this.written_by = request.user.userAcc
                this.part_of_album = myAlbum
                this.save()
                myAlbum.songs.add(this)
        myURL =    '/bands/edit/'+str(myBand.id)+'/'     
        return HttpResponseRedirect(myURL)
                
            
    else:
        form = AlbumEditForm(instance = myAlbum)
        formset = SongFormSet()
        albumform = AlbumForm(instance = myAlbum)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['formset'] = formset
    args['albumform'] = albumform
    args['album'] = myAlbum
    args['band'] = myBand
    return render_to_response('album_edit.html',
                              args,  context_instance = RequestContext(request))
@login_required
def choose_songs(request, bandID):
    myBand = Band.objects.get(id = bandID)
    albums = myBand.albums.all()
    mySongs = Song.objects.filter(songOwner = myBand)
    if request.method == 'POST':
        songform = ChooseFormSet(request.POST, queryset = mySongs)
        if songform.is_valid():
            for form in songform.forms:
                this = form.save(commit = False)
                this.save()
                
        myURL = '/bands/choose_songs/'+str(myBand.id)+'/'          
        return HttpResponseRedirect(myURL)
    else:
        songform = ChooseFormSet(queryset = mySongs)
    args = {}
    args.update(csrf(request))
    args['songform'] = songform
    args['band'] = myBand
    return render_to_response('choose_songs.html', args, context_instance = RequestContext(request))


@login_required       
def addAlbums(request, bandID):
    myBand = Band.objects.get(id = bandID)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            this = form.save(commit = False)
            this.release_month = Month.objects.get(id = 1)
            this.save()
            form.save_m2m()
            myBand.albums.add(this)
            myURL = '/bands/edit_album/'+ str(this.id)+'/'+ bandID+'/'
            return HttpResponseRedirect(myURL)
    else:
        form = AlbumForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['band'] = myBand
        
    return render_to_response('new_album.html', args, context_instance = RequestContext(request))

@login_required
def createSong(request, bandID):
    this_band = Band.objects.get(id = bandID)
    if request.POST:
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            this = form.save(commit = False)
            this.songOwner = this_band
            this.written_by = request.user.userAcc
            this.save()
            form.save_m2m()
            handle_uploaded_file(request.FILES['audio_track'])
            this_band.songs.add(this)
            myURL = '/bands/get/'+ bandID + '/'
            return HttpResponseRedirect(myURL)    
    else:
        form = SongForm()
           
    args = {}                      
    args.update(csrf(request))
    args['form'] = form
    args['band'] = this_band
        
    return render_to_response('new_song.html', args, context_instance = RequestContext(request))
    
def search_bands(request):
    myBands = SearchQuerySet().autocomplete(content_auto = request.POST.get('searchk_text', ''))
    return render_to_response('search.html', {'bands': myBands})
@login_required
def removeSong(request, songID, bandID):
    song = Song.objects.get(id = songID)
    myAlbum = song.part_of_album
    myAlbum.songs.remove(song)
    myBand = Band.objects.filter(albums = myAlbum)
    song.delete()
    myURL = '/bands/form_3/'+bandID+'/1000000/'
    return HttpResponseRedirect(myURL)
@login_required
def removePicture(request, bandID, pictureID):
    myBand = Band.objects.get(id = bandID)
    picture = Picture.objects.get(id = pictureID)
    myBand.pictures.remove(picture)
    myURL = '/bands/form_3/'+ bandID + '/'
    return HttpResponseRedirect(myURL)

@login_required
def addPicture(request, bandID):
    myBand = Band.objects.get(id = bandID)
    if request.POST:
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            this = form.save(commit = False)
            this.uploader = request.user.userAcc
            this.save()
            form.save_m2m()
            handle_uploaded_file(request.FILES['picture_file'])
            myBand.pictures.add(this)
            myURL = '/bands/get/'+ bandID+'/'
            return HttpResponseRedirect(myURL)
    else:
        form = PictureForm()
        
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['band'] = myBand
    
    return render_to_response('new_picture.html', args, context_instance = RequestContext(request))
@login_required
def ProfilePicture(request, bandID):
    myBand = Band.objects.get(id = bandID)
    if request.POST:
        form = ProfilePicForm(request.POST, request.FILES)
        this = form.save(commit = False)
        this.uploader = request.user.userAcc
        this.caption = 'Profile pic for' + Band.objects.get(id = bandID).name
        
        this.save()
        form.save_m2m()
        handle_uploaded_file(request.FILES['picture_file'])
        myBand.main_image = this
        myBand.save()
        myURL = '/bands/edit/' + bandID + '/'
        return HttpResponseRedirect(myURL)
    else:
        form = ProfilePicForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['band'] = myBand
    return render_to_response('new_profile_picture.html', args, context_instance = RequestContext(request))
@login_required
def ThumbnailPicture(request, bandID):
    myBand = Band.objects.get(id = bandID)
    if request.POST:
        form = ThumbnailPicForm(request.POST, request.FILES)
        this = form.save(commit = False)
        this.uploader = request.user.userAcc
        this.caption = 'Thumbnail pic for' + Band.objects.get(id = bandID).name
        
        this.save()
        form.save_m2m()
        handle_uploaded_file(request.FILES['picture_file'])
        myBand.thumbnailPic = this
        myBand.save()
        myURL = '/bands/get/' + bandID + '/'
        return HttpResponseRedirect(myURL)
    else:
        form = ThumbnailPicForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['band'] = myBand
    return render_to_response('new_thumbnail_pic_bands.html', args, context_instance = RequestContext(request))

def search_bands(request):
    bands = SearchQuerySet().models(Band).autocomplete(content_auto=request.POST.get('search_text',''))
    return render_to_response('ajax_search.html', {'bands': bands})


from ajaxuploader.views import AjaxFileUploader

def start(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('import.html', args, context_instance = RequestContext(request))

import_uploader = AjaxFileUploader()
@login_required
def areYouSure(request, albumID, songID):
    band = Song.objects.get(id = songID).songOwner
    return render_to_response('are_you_sure.html',
                              {'album' : Album.objects.get(id = albumID), 'song': Song.objects.get(id = songID), 'band': band}, context_instance = RequestContext(request))
    
@login_required
def removeAlbumSong(request, albumID, songID):
    myAlbum = Album.objects.get(id = albumID)
    mySong = Song.objects.get(id = songID)
    myAlbum.songs.remove(mySong)
    form = AlbumEditForm(instance = myAlbum)
    formset = SongFormSet()
    albumform = AlbumForm(instance = myAlbum)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['formset'] = formset
    args['albumform'] = albumform
    args['album'] = myAlbum
    args['band'] = Song.objects.get(id = songID).songOwner
    
    return render_to_response('album_edit.html',
                              args,  context_instance = RequestContext(request))
def removeBand(request, bandID):
    return render_to_response('band_areYouSure.html',
                              {'band':Band.objects.get(id = bandID)}, context_instance = RequestContext(request))

def remove(request, bandID):
    myBand = Band.objects.get(id = bandID)
    myBand.delete()
    return HttpResponseRedirect('/bands/all/')


def viewAlbum(request, bandID, albumID):
    myBand = Band.objects.get(id = bandID)
    myAlbum = Album.objects.get(id = albumID)
    songs = Song.objects.filter(part_of_album = myAlbum)
    return render_to_response('album.html',
                              {'band': myBand, 'songs':songs, 'album':myAlbum})

def send_message(request, bandID, userID):
    myBand = Band.objects.get(id = bandID)
    myUser = request.user.userAcc
    try:
        myThread = Thread.objects.get(user = myUser, band = myBand)
    except:
        myThread = Thread(user = myUser, band = myBand)
        myThread.save()
    
    if request.user.userAcc != userAcc.objects.get(id = userID):
        return HttpResponseRedirect('/')
    if not request.user.userAcc.first_name:
        return HttpResponseRedirect('/edit/')
    if request.method == 'POST':
        form = messageForm(request.POST)
        
        if form.is_valid():
            this = form.save(commit = False)
            this.sender = request.user.userAcc
            this.save()
            this.subject_band = myBand
            for tag in myBand.tag_identifiers.all():
                this.subject_tags.add(tag)
            myBand.messages.add(this)
            myThread.messages.add(this)
            songs = Song.objects.all().filter(songOwner = myBand).filter(include_on=True)
            
            messageform = messageForm()
            
            message = 'Your message was sent successfully!'
            context_instance = RequestContext(request)
            today = set()
            tomorrow = set()
            next_week = set()
            this_month = set()
            for event in myBand.events.all():
                if event.date == datetime.date(datetime.now()):
                    today.add(event)
                elif ((event.date > datetime.date(datetime.now())) and (event.date < datetime.date(datetime.now())+timedelta(2))):
                    tomorrow.add(event)
                elif ((event.date >= datetime.date(datetime.now())+timedelta(2)) and (event.date <= datetime.date(datetime.now())+timedelta(7))):
                    next_week.add(event)
                else:
                    this_month.add(event)
            return render_to_response('band.html',
                                      {'band': myBand, 'adjectives': myBand.adjectives.all(), 'user': request.user, 'songs' : songs, 'today': today, 'tomorrow': tomorrow,
                                       'next_week': next_week, 'this_month': this_month, 'message_form': messageform, 'message':message}, context_instance = RequestContext(request))
        
    
  

def messages(request, bandID):
    messages = Band.objects.get(id = bandID).messages.all()
    form = messageForm(request.POST)
    threads = Thread.objects.filter(band = Band.objects.get(id = 1))
    return render_to_response('messages.html',
                              {'messages':messages, 'band':Band.objects.get(id = bandID), 'form': form}, context_instance = RequestContext(request))

def reply_message(request, messageID):
    recipient = Message.objects.get(id = messageID).sender
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = messageForm(request.POST)
        message = ' ' 
        if form.is_valid():
            this = form.save(commit = False)
            this.sender = request.user.userAcc
            this.save()
            recipient.messages.add(this)
            message = '<p>From'+ '    ' + Message.objects.get(id = messageID).message + '</p>'
        return render_to_response('messagereply.html',
                              {'message': message, 'myMessage': Message.objects.get(id = messageID), 'form': form, 'data':message}, context_instance = RequestContext(request))
    else:
        message = '<p>Something went wrong</p>'
    return render_to_response('messagereply.html',
                              {'message': message, 'myMessage': Message.objects.get(id = messageID), 'form': form, 'data': message}, context_instance = RequestContext(request))