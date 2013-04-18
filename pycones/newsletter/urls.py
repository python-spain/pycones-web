from django.conf.urls.defaults import url,patterns

urlpatterns = patterns("pycones.newsletter.views",
    #url(r"^$","get_last_entries",name="get_last_entries"),
    url(r"^suscribe/$", "suscribe_newsletter",name="suscribe_newletter"),
    url(r"^unsuscribe/$", "unsuscribe_newsletter",name="unsuscribe_newsletter"),
    url(r"^latest/$", "get_last_newsletter",name="get_last_newsletter"),
    url(r"^(?P<year_month>\d{6})/$","get_newsletter",name="get_newsletter"),
    url(r"^(?P<year_month>\d{6})/send/$","send_newsletter",name="send_newsletter"),
    #url(r"^(?P<page>\d(1-3))/$","get_entries_per_page",name="get_entries_per_page"),
    #url(r"^(?P<year>\d(4))/$","get_entries_per_year",name="get_entries_per_year"),
    #rl(r"^(?P<year>\d(4))/(?P<month>\d(2))/$",
    #    "get_entries_per_month",
    #    name="get_entries_per_month"),
    url(r"^article/(?P<article_path>[\w\-]+)/$","get_article",name="get_article"),

)
