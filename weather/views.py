from django.shortcuts import render

from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .forms import PlaceForm

from .get_place import get_place
from .get_weather import get_weather
from .models import City

import logging
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import F


def work_City(name_city: str):
    try:
        city = City.objects.filter(name=name_city)
        logging.info("The city was found in the database")
    except ObjectDoesNotExist:
        city = None
        logging.error("The city was not found in the database.")

    if city:
        city.update(count_request=F("count_request")+1)
    else:
        City.objects.create(name=name_city, count_request=1)

    return None


class IndexView(SuccessMessageMixin, FormView):
    template_name = "index.html"
    form_class = PlaceForm
    success_url = "/"
    success_message = ('Город найден')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        last_cities = self.request.session.get('last_cities', None)

        if last_cities is None:
            return super().get_context_data(**kwargs)

        logging.info('Sessions are working')

        last_city = last_cities[-1]
        messages.info(self.request, f'Хотите узнать погоду {last_city}')
        messages_ = messages.get_messages(self.request)

        context = super(IndexView, self).get_context_data(**kwargs)
        context['messages'] = messages_
        context['history'] = last_cities
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            logging.info("Form valid")
            name_city = form.cleaned_data['place']

        try:
            place = get_place(name_city)
            weather_place = get_weather(place['latitude'], place['longitude'])
            weather_place['address'] = place['address']

            messages.success(request, 'Город найден')
            logging.info("City is found")
        except TypeError:
            weather_place = None

            logging.error("City not found")
            messages.error(request, 'Город не найден')
            return super().get(self, request, *args, **kwargs)

        work_City(name_city)

        last_cities = request.session.get('last_cities', None)
        if last_cities is None:
            last_cities = [name_city]
        elif len(last_cities) < 10:
            last_cities.append(name_city)
        else:
            last_cities.pop(0)
            last_cities.append(name_city)
        request.session['last_cities'] = last_cities

        messages_ = messages.get_messages(request)
        return render(
            request,
            'index.html',
            context={
                'form': self.get_form(),
                'messages': messages_,
                'weather_place': weather_place,
                'history': last_cities
            }
        )


class CountCities(ListView):
    model = City
    template_name = 'count_cities.html'
    context_object_name = 'cities'
