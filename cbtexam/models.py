from email.policy import default
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from matplotlib import widgets
from tinymce import models as tinymce_models
def validate_pass(value):
    if len(str((value) ))< 6:
        raise ValidationError(
            _('%(value)s is not up to 7 digits'),
                              params={'value': value},
        )
        
        
class Student_field(models.Model):
    field_title = models.CharField(max_length=200,  null=True,  blank=True)
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['field_title']
        verbose_name = 'Student Field'
        verbose_name_plural = 'Student Fields'

    def __str__(self):
        return self.field_title

    def save(self,  *args,  **kwargs):
        self.slug = slugify(self.field_title)
        super(Student_field,  self).save(*args,  **kwargs)

       
class Level(models.Model):
    class_name = models.CharField(max_length=200,  null=True)
    slug = models.SlugField(null=True,  blank=True)

    class Meta:
        ordering = ['class_name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.class_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.class_name)
        super(Level, self).save(*args, **kwargs)


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to ='media/', null = True, blank =True)
    phone = models.IntegerField( unique=True, null= True, blank = True, validators=[validate_pass])
    country = models.CharField(max_length=200,  null = True, blank=True)
    state = models.CharField(max_length=200,  null = True, blank=True)
    is_student = models.BooleanField(default=0)
    is_teacher = models.BooleanField(default=0)
    mailing_address = models.CharField(max_length=200, null = True,   blank=True)
    study_field = models.ForeignKey(Student_field, on_delete=models.CASCADE, blank=True, null=True)
    class_enrolled = models.ForeignKey(Level, on_delete=models.CASCADE,  blank=True, null=True, related_name='studentlevel')
 
 
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)



class Subject(models.Model):
    name = models.CharField(max_length=200,  null=True)
    subject_class = models.ForeignKey(Level, on_delete=models.CASCADE, null =True, related_name ='subject_class')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name ='subject_teacher')
    tag = models.CharField(max_length=200,  null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tag = slugify(self.subject_class)
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)


class GCE(models.Model):
    question = models.CharField(max_length=1000, null = True)
    year = models.CharField(max_length=1000, null = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cbt_subject_teacher')
    author_class = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='cbt_subject_class')
    author_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='cbt_subject')
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    class Meta:
        verbose_name = 'GCSSE'
        verbose_name_plural = 'GCSSE'
    
    def __str__(self):
        return self.question
    
    def save(self,  *args,  **kwargs):
        self.author_class = self.author_subject.subject_class
        super(GCE,  self).save(*args,  **kwargs)
    
class Logo(models.Model):
    title = models.CharField(max_length=1000, null = True)
    pic = models.ImageField(upload_to ='media/', null = True, blank =True)
    
    
class Posts(models.Model):
    title = models.CharField(max_length=100, null=True)
    slug =models.SlugField(max_length=100)
    author =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/')
    
    class Meta:
        ordering = ['post_date']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Posts, self).save(*args, **kwargs)
        

class PostComments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments', null=True)
    name =models.CharField(max_length=200, null=True, blank=True)
    email =models.EmailField(max_length=100)
    heading =models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(null =True, auto_now_add=True)
    body =models.TextField()
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.heading
    
    
class Scholarships(models.Model):
    title = models.CharField(max_length=100, null=True)
    slug =models.SlugField(max_length=100)
    author =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/')
    link = models.URLField(max_length=200)
    country = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['post_date']
        verbose_name = 'scholarship'
        verbose_name_plural = 'scholarships'
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Scholarships, self).save(*args, **kwargs)
        
        
class ScholarshipComments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Scholarships, on_delete=models.CASCADE, related_name='scholarshipcomments', null=True)
    name =models.CharField(max_length=200, null=True, blank=True)
    email =models.EmailField(max_length=100)
    heading =models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(null =True, auto_now_add=True)
    body =models.TextField()
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.heading
    
    
class JAMB(models.Model):
    question = models.CharField(max_length=1000, null = True)
    year = models.CharField(max_length=1000, null = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jamb_subject_teacher')
    author_class = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='jamb_subject_class')
    author_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='jamb_subject')
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question
    
    def save(self,  *args,  **kwargs):
        self.author_class = self.author_subject.subject_class
        super(JAMB,  self).save(*args,  **kwargs)
    
    
class SSCE(models.Model):
    question = models.CharField(max_length=1000, null = True)
    year = models.CharField(max_length=1000, null = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ssce_subject_teacher')
    author_class = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='ssce_subject_class')
    author_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='ssce_subject')
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question
    
    def save(self,  *args,  **kwargs):
        self.author_class = self.author_subject.subject_class
        super(SSCE,  self).save(*args,  **kwargs)
    
    
class NECO(models.Model):
    question = models.CharField(max_length=1000, null = True)
    year = models.CharField(max_length=1000, null = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='neco_subject_teacher')
    author_class = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='neco_subject_class')
    author_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='neco_subject')
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question
    
    def save(self,  *args,  **kwargs):
        self.author_class = self.author_subject.subject_class
        super(NECO,  self).save(*args,  **kwargs)
        
    
class SCORES(models.Model):
    student_name = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='studentusername')
    exam = models.CharField(max_length=1000, null = True)
    correct = models.CharField(max_length=200,null=True)
    incorrect = models.CharField(max_length=200,null=True)
    total_score = models.CharField(max_length=200,null=True)
    date_taken = models.DateTimeField(null =True, auto_now_add=True)
    author_class = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, related_name='subjectclass')
    author_subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE, related_name='subject')
    
    def __str__(self):
        return self.exam
    
    '''def save(self,  *args,  **kwargs):
        self.author_class = self.author_subject.subject_class
        super(SCORES,  self).save(*args,  **kwargs)'''

        
class Poll(models.Model):
    question = models.CharField(max_length=1000, null = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='poll_author')
    pub_date = models.DateTimeField(auto_now_add=True)
    op1 = models.CharField(max_length=200,null=True)
    op1score = models.IntegerField(default=0)
    op2 = models.CharField(max_length=200,null=True)
    op2score = models.IntegerField(default=0)
    op3 = models.CharField(max_length=200,null=True)
    op3score = models.IntegerField(default=0)
    op4 = models.CharField(max_length=200,null=True)
    op4score = models.IntegerField(default=0)
    

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'
    
    def __str__(self):
        return self.question
    
    def save(self,  *args,  **kwargs):
        super(Poll,  self).save(*args,  **kwargs)