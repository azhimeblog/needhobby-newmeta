from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize

STATUS = ((0,"Draft"),(1,"Publish"))

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="ชื่อหมวดหมู่")
    content = models.TextField(default='ใส่เนื้อหาหมวดหมู่')
    slug = models.SlugField(max_length=200, default='ใส่ลิงค์บทความ ตัวอย่าง /your-post-content')
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"  

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class Websitedetail(models.Model):
    websitename = models.CharField(max_length=200,unique=True,default='ชื่อเว็บไซต์')
    websitedetail = models.CharField(max_length=400,unique=True,default='รายละเอียดเว็บไซต์')

    def __str__(self):
        return self.websitename

class Post(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200,unique=True,default='ใส่ชื่อบทความ')
    content = models.TextField(default='ใส่เนื้อหาบทความ')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    post_viewcount = models.PositiveIntegerField(default=0,)
    slug = models.SlugField(max_length=200, default='ลิงค์หลังบทความ')
    status = models.IntegerField(choices=STATUS , default=1)
    likes = models.ManyToManyField(User, related_name="likes")
    

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category # for now ignore this instance method
        
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]
