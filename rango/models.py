from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

""" Some Field Types:
• CharField, a field for storing character data (e.g. strings). Specify max_length to provide a
maximum number of characters the field can store.
• URLField, much like a CharField, but designed for storing resource URLs. You may also
specify a max_length parameter.
• IntegerField, which stores integers.
• DateField, which stores a Python datetime.date object.
"""

""" Django Keys:
• ForeignKey, a field type that allows us to create a one-to-many relationship;
• OneToOneField, a field type that allows us to define a strict one-to-one relationship; and
• ManyToManyField, a field type which allows us to define a many-to-many relationship.
"""

# Create your models here.

class Category(models.Model):
    name_max_length = 128
    name = models.CharField(max_length=name_max_length, unique=True) # Unique means name can be used as a primary key
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username

