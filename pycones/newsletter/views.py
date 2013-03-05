# -*- coding: utf-8 -*-

import uuid

from django.shortcuts import render_to_response,redirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django import http

from .models import Subscription, get_or_create_active_newsletter


def send_welcome_msg(email_user,token):
    subject = u'¡Bienvenido a PyConES!'
    from_email = u'newsletter@es.pycon.org'

    # FIXME: put this text into one template.
    text_content = u'''¡Bienvenido a la newsletter de PyConES!

Hola,

Muchas gracias por registrarte a la newsletter de la Python Conference de
A partir de ahora recibirás todas las noticias y actualizaciones sobre el
eventp directamente en tu email sin esfuerzo alguno. Serás el primero en
recibir información crítica del evento como, por ejemplo, noticias sobre
ponentes y patrocinadores, venta de entradas, planificación de charlas..

Recuerda que también estamos en twitter en @PyConES y #PyConES. Estamos
encantados de escucharte así que no dudes en mandarnos un tweet :)

Aún así no te obligamos a aguantarnos. Podrás darte de baja con el siguiente
enlace:

http://es.pycon.org/newsletter/unsuscribe/?email={0}&val_token={1}

Un saludo
Muchas gracias
Equipo Organizativo de PyConES
    '''.format(email_user,token)
    context_email = {'email_user' : email_user, 'token' : token}
    template_email = get_template('newsletter_welcome_mail.html')
    html_content = template_email.render(Context(context_email))

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_user])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def suscribe_newsletter(request):
    """
    View to suscribe new users to newsletter
    """

    if request.method != 'POST':
        return redirect('/')

    email = request.POST('email_user', None)
    newsletter = get_or_create_active_newsletter()

    if not email_user:
        context = {'message' : u"Error al recoger el email. Intentalo de nuevo mas tarde"}
        return render_to_response("newsletter/comingsoon_message.html", context,
                                  context_instance=RequestContext(request))

    if not User.objects.filter(username=email).exists():
        user = User(username=email, email=email)
        user.set_unusable_password()
        user.save()

        # Create a profile model for new user
        profile = Profile(user=user, newsletter_token=unicode(uuid.uuid4()))
        profile.save()

    if Subscriber.objects.filter(user=user, newsletter=newsletter).exists():
        context = {'message' : u"Se ha producido un error. Quizás ya estes dado de alta."}
        return render_to_response("newsletter/comingsoon_message.html", context,
                                  context_instance=RequestContext(request))

    subscriber = Subscriber(user=user, newsletter=newsletter)
    subscriber.save()

    context = {'message' : u"Registrado. Muchas gracias"}
    return render_to_response("newsletter/comingsoon_message.html", context,
                               context_instance=RequestContext(request))


def unsuscribe_newsletter(request):
    """
    View to unsuscribe newsletter
    """
    if request.method != 'GET':
        return redirect('/')

    email = request.GET.get('email', None)
    token = request.GET.get('val_token', None)

    newsletter = get_or_create_active_newsletter()

    if not email or not token:
        context = {"message": u"Parametros incorrectos"}
        return render_to_response("newsletter/comingsoon_message.html",
                        context, context_instance=RequestContext(request))

    queryset = User.objects.filter(username=email, profile__newsletter_token=token)
    try:
        user = queryset.get()
    except User.DoesNotExist:
        context = {"message": u"Usuario no encontrado."}
    else:
        subscription_queryset = Subscription.objects.filter(
                                    newsletter=newsletter, user=user)
        if subscription_queryset.exists():
            subscription_queryset.delete()
            context = {"message": u"Eliminado de la newsletter correctamente"}
        else:
            context = {"message": u"Usuario no encontrado."}

    return render_to_response("newsletter/comingsoon_message.html",
                        context, context_instance=RequestContext(request))
