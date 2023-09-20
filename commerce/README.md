## Common Commands

Start server
`python manage.py runserver`

Get into django shell
`python manage.py shell`

Create admin user
`python manage.py createsuperuser`


## Making a database
update models.py with classes want in database
Make Migrations
`python manage.py makemigrations`
Deploy Migrations
`python manage.py migrate`

Open django shell
`python manage.py shell`

Import class
`from auctions.models import Comment`
Make Comment
`c = Comment(user="bforr", comment="This is a test comment")`

`l = Listing(category="Auto", description="Some description", imgUrl="https://images.freeimages.com/images/large-previews/21f/vector-2-1147339.jpg", owner="bforr", startingBid=".05", title="Audi 500")`


Save Comment
`c.save()`

View all 
`Comment.objects.all()`


## Add models to admin for use in admin
from .models import Listing

# Register your models here.
admin.site.register(Listing)