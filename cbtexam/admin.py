from django.contrib import admin
from .models import JAMB, NECO, SCORES, SSCE, CustomUser, Level, Logo, Poll, PostComments, Posts, GCE, ScholarshipComments, Scholarships, Student_field, Subject
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username',  'email', 'first_name', 'last_name', 'is_staff', 'is_student', 'is_teacher', 'mailing_address', 'phone', 'state', 'country')
    search_fields =['username', 'status']

    
    fieldsets = ( 
                 ( None, { 'fields': ('username', 'password') }),
                 
                 ('Personal info', { 'fields' : ('first_name', 'last_name', 'email') }),
                 
                ('Permissions', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),

                 ('Important dates', {'fields': ('last_login', 'date_joined') }),
                 
                 ('Additional info:', {'fields': ( 'is_student', 'is_teacher', 'mailing_address',  'phone', 'state', 'country', 'profile_pic', 'study_field', 'class_enrolled')}),
                 
                 )
    
    add_fieldsets = ( 
                     
                 ( None, { 'fields': ('username', 'password1', 'password2') }),
                 
                 ('Personal info', { 'fields' : ('first_name', 'last_name', 'email') }),
                 
                ('Permissions', { 'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),
                 
                 ('Important dates', {'fields': ('last_login', 'date_joined') }),
                 
                 ('Additional info:', {'fields': ( 'is_student', 'is_teacher', 'mailing_address', 'phone', 'state', 'country', 'profile_pic', 'study_field', 'class_enrolled')}),
                 
                 )
    
    
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'author']


class GCEAdmin(admin.ModelAdmin):
    list_display = ['question', 'ans']
    
    
class Student_fieldAdmin(admin.ModelAdmin):
    list_display = ['field_title', 'slug']
    prepopulated_fields = {'slug': ('field_title',)}
    
    
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 
    
    
class LevelAdmin(admin.ModelAdmin):
    list_display = ['class_name',  'slug']
    prepopulated_fields = {'slug': ('class_name',)}
    
    
class ScholarshipCommentsInline(admin.StackedInline):
    model = ScholarshipComments
    extra = 3
    

class ScholarshipsAdmin(admin.ModelAdmin):
    fieldsets = [
           ( 'Scholarship Information', {'fields': ['title', 'slug', 'author', 'description', 'image', 'link', 'country']}),
]
    inlines = [ScholarshipCommentsInline]
    
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student_field, Student_fieldAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Scholarships, ScholarshipsAdmin)
admin.site.register(ScholarshipComments)
admin.site.register(JAMB)
admin.site.register(SSCE)
admin.site.register(NECO)
admin.site.register(Posts)
admin.site.register(PostComments)
admin.site.register(GCE, GCEAdmin)
admin.site.register(Logo)
admin.site.register(SCORES)
admin.site.register(Poll, PollAdmin)
