from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify
import uuid
# Create your models here.
 
class signup(models.Model):
    email=models.EmailField(null=False,blank=False)
    password=models.CharField(max_length=15)

    

    class Meta:
        verbose_name = _("signup")
        verbose_name_plural = _("signups")

    def __str__(self):
        return self.email


class List(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title=models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=False,default=uuid.uuid1)
    bg_image=models.ImageField(upload_to="media/")
    short_description=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    trailer_url=models.URLField()
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(List, self).save(*args, **kwargs)
    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def __str__(self):
        return self.title

    