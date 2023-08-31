<!-- get into django shell -->

python manage.py shell

<!-- import model  -->

from flights.models import Flight

<!-- Insert new flight  -->

f = Flight(origin='New York', destination='London', duration=415)
f.save()

<!-- View flights  -->

from flights.models import \*
flights = Flight.objects.all()
fligts

nrt = Airport(code='NRT', city='Tokyo')

> > > nrt.save()
> > > f = Flight(origin=jfk, destination=lhr, duration=415)
> > > f.save()

python manage.py createsuperuser
