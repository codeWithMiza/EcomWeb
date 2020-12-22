from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    heading_one = models.CharField(max_length=500, default="")
    content_one = models.CharField(max_length=5000, default="")
    heading_two = models.CharField(max_length=500, default="")
    content_two = models.CharField(max_length=5000, default="")
    heading_three = models.CharField(max_length=500, default="")
    content_three = models.CharField(max_length=5000, default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to='store/images', default="")

    def __str__(self):
        return self.title