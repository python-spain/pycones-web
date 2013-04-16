# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404


#def get_or_create_active_newsletter():
#    current_active_nl = getattr(settings, 'ACTIVE_NEWSLETTER', '2013')
#    try:
#        newsletter = Newsletter.objects.get(name=current_active_nl)
#    except Newsletter.DoesNotExist:
#        newsletter = Newsletter.objects.create(name=current_active_nl)
#
#    return newsletter


class ArticleManager(models.Manager):
    def get_article_by_path(self, article_path):
        """
        Method to get an article or entry by path field.
        If path is not exist 404Exception will be raised
        """
        queryset = super(ArticleManager,self).get_query_set()

        article = queryset.get_object_or_404(
                    path__iexact=article_path, visible=True)

        return article

    def get_last_articles(self):
        """
        Method to get last 5 articles added to active newsletter
        """
        article_queryset = super(ArticleManager,self).get_query_set()
        articles = article_queryset\
            .filter(visible=True)\
            .order_by('-create_date')[:5]

        return articles

    def get_articles_per_page(self, page_number):
        """
        Method to get 5 articles per page number( 5 articles per page )
        For example:
            if page=1 articles 6-10
            if page=2 articles 11-15
        To calculate first article we use: 5 * page_number + 1
        To calculate last article we use: first_article + 4
        """

        # FIXME: use django pagination instead of manual pagination
        first_article = (page_number * 5 + 1)
        last_article = (first_article + 4)

        queryset = super(ArticleManager,self).get_query_set()

        articles = queryset\
            .filter(visible=True)\
            .order_by('-create_date')[first_article:last_article]

        return articles

    def get_articles_per_year(self,year):
        """
        Method to get articles per year
        """
        queryset = super(ArticleManager,self).get_query_set()

        articles = queryset.filter(
                    visible=True,
                    create_date__year=year)\
                    .order_by('-create_date')

        return articles

    def get_articles_per_month(self):
        """
        Method to get articles per year and month
        """
        queryset = super(ArticleManager,self).get_query_set()
        articles = queryset.filter(
                        visible=True,
                        create_date__year=year, create_date__month=month)\
                    .order_by('-create_date')

        return articles

class NewsletterManager(models.Manager):

    def get_latest_newsletter(self):
        """
        Method to get latest newsletter
        """
        queryset = super(NewsletterManager,self).get_query_set()
        try:
            newsletter = queryset.all().order_by('-create_date').get()
        except Newsletter.DoesNotExist:
            newsletter = None

        return newsletter

    def get_newsletter(self,year,month):
        """
        Method to get a single newsletter with year and month
        """
        queryset = super(NewsletterManager,self).get_query_set()
        try:
            newsletter = queryset.filter(create_date__year=year,create_date__month=month).get()
        except Newsletter.DoesNotExist:
            newsletter = None

        return newsletter

class Article(models.Model):
    path = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(editable=False, auto_now_add=True)
    update_date = models.DateTimeField(editable=False, auto_now=True)
    visible = models.BooleanField(default=False)

    objects = ArticleManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["create_date"]


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    head = models.TextField()
    create_date = models.DateTimeField(editable=False, auto_now_add=True)
    send_date = models.DateTimeField()
    articles = models.ManyToManyField("Article")

    objects = NewsletterManager()

    def __unicode__(self):
        return "{0} ({1})".format(self.title,str(self.create_date)[:7])

    class Meta:
        ordering = ["send_date"]


class Subscription(models.Model):
    user_email = models.EmailField()
    val_token = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user_email


