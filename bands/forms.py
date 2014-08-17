from django import forms
from bands.models import  *
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import Widget
from users.models import userAcc
from venues.models import *
from tagstar.models import *
from datetime import *
from haystack.forms import ModelSearchForm
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from events.models import *



class PictureForm(forms.ModelForm):
    picture_file = forms.FileField()
    class Meta:
        model = Picture
        fields = ('caption', 'picture_file', 'date')
        
class ProfilePicForm(forms.ModelForm):
    picture_file = forms.FileField()
    class Meta:
        model = Picture
        fields = ('picture_file',)
        
        
class ThumbnailPicForm(forms.ModelForm):
    picture_file = forms.FileField()
    class Meta:
        model = Picture
        fields = ('picture_file',)
        
        
        
class AlbumForm(forms.ModelForm):
   
    class Meta:
        model = Album
        fields = ('name', 'about',  'release_yr', 'release_month','cover' )
        
class AlbumEditForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ( 'copyright_info', 'cover', 'purchase_link')

class SongForm(forms.ModelForm):
    audio_track = forms.FileField()
    class Meta:
        model = Song
        fields = ('songName',  'audio_track', 'include_on')
        exclude = ['include_on']
        
        
SongFormSet = modelformset_factory(Song,  extra = 1, exclude = ['songOwner', 'written_by', 'tags', 'produced_by', 'part_of_album', 'order'])

class SongChooseForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('songName', 'include_on')
        
ChooseFormSet = modelformset_factory(Song, extra = 0,   exclude = ['songOwner', 'audio_track','written_by', 'tags', 'produced_by', 'part_of_album', 'order'])


class band_tag_form(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
        
class band_member_form(forms.ModelForm):
    class Meta:
        model = band_member
        fields = ('name', 'instruments')
        

band_member_form_set = modelformset_factory(band_member, extra = 0,   exclude= ['user_related', 'instruments'])

        
class BandForm(forms.ModelForm): # first form stage
    #adjectives = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Adjective.objects.all())
    class Meta:
        model = Band
        fields = ('name', 'year_formed','description')
        
class BandForm2(forms.ModelForm):
    adjectives = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Adjective.objects.all())
    class Meta:
        model = Band
        fields = ('adjectives', 'status', 'album_status', )
        
class bandEditForm(forms.ModelForm):
    adjectives = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Adjective.objects.all())
    
    class Meta:
        model = Band
        fields = ('name',  'description', 'adjectives','status')
        
class AutocompleteModelSearchForm(ModelSearchForm):
    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        if not self.cleaned_data.get('q'):
            return self.no_query_found()
        sqs = self.searchqueryset.filter(name_auto = self.cleaned_data['q'])
        
        if self.load_all:
            sqs = sqs.load_all()
        
        return sqs
    