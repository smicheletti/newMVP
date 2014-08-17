from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^all/$', 'bands.views.allBands'),
    url(r'^get/(?P<bandID>\w{0,70})/$', 'bands.views.oneBand'),
    url(r'^create/$', 'bands.views.create'),
    #display bands of a single attribute
    url(r'^get/attribute/(?P<adjective>\w{0,30})/$', 'bands.views.attribute'),# need to rework this, may not be only bands here
    url(r'^notFound/$', 'bands.views.notFound'),
    url(r'^(?P<bandID>\w{0,70})/createSong/$', 'bands.views.createSong'),
    url(r'^like/(?P<userID>\w{0,30})/(?P<bandID>\w{0,30})/$', 'bands.views.addFavoriteBand'),
    url(r'^unlike/(?P<userID>\w{0,30})/(?P<bandID>\w{0,30})/$', 'bands.views.unlikeBand'),
    #url(r'^search/$', 'bands.views.search_text'),
    url(r'^edit/(?P<bandID>\w{0,30})/$', 'bands.views.editBand'),
    url(r'^edit/$', 'bands.views.editBand'),
    url(r'^remove/(?P<bandID>\w{0,30})/(?P<songID>\w{0,30})/$', 'bands.views.removeSong'),
    url(r'^addPicture/(?P<bandID>\w{0,30})/$', 'bands.views.addPicture'),
    url(r'^addProfilePicture/(?P<bandID>\w{0,30})/$', 'bands.views.ProfilePicture'),
    url(r'^removePic/(?P<bandID>\w{0,30})/(?P<pictureID>\w{0,30})/$', 'bands.views.removePicture'),
    url(r'^addThumbnailPic/(?P<bandID>\w{0,30})/$', 'bands.views.ThumbnailPicture'),
    url(r'^edit_album/(?P<albumID>\w{0,30})/(?P<bandID>\w{0,30})/$', 'bands.views.editAlbums'),
    url(r'^addAlbum/(?P<bandID>\w{0,30})/', 'bands.views.addAlbums'),
    url(r'^editAlbum/(?P<albumID>\w{0,30})/(?P<songID>\w{0,30})/', 'bands.views.areYouSure'),
    url(r'^doIt/(?P<albumID>\w{0,30})/(?P<songID>\w{0,30})/', 'bands.views.removeAlbumSong'),
    url(r'^removeBand/(?P<bandID>\w{0,30})/$', 'bands.views.removeBand'),
    url(r'^remove/(?P<bandID>\w{0,30})/$', 'bands.views.remove'),
    url(r'^choose_songs/(?P<bandID>\w{0,30})/$', 'bands.views.choose_songs'),
    url(r'^album/get/(?P<bandID>\w{0,30})/(?P<albumID>\w{0,30})/$', 'bands.views.viewAlbum'),
    url(r'^send_message/(?P<bandID>\w{0,30})/(?P<userID>\w{0,30})/$', 'bands.views.send_message'),
    url(r'^message/(?P<messageID>\w{0,30})/$', 'users.views.oneMessage'),
    url(r'^messages/(?P<bandID>\w{0,30})/$', 'bands.views.messages'),
    url(r'^reply/(?P<messageID>\w{0,30})/$', 'bands.views.reply_message'),
    url(r'^form_2/(?P<bandID>\w{0,30})/$', 'bands.views.form_2'),
    url(r'^form_3/(?P<bandID>\w{0,30})/(?P<albumID>\w{0,30})/$', 'bands.views.form_3'),
    url(r'^remove_album/(?P<albumID>\w{0,30})/(?P<bandID>\w{0,30})/$', 'bands.views.remove_album'), 
    
    
)

        