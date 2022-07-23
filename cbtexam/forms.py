from django.forms import  ModelForm
from .models import CustomUser, PostComments, GCE, Level, Subject


class RegisterForm(ModelForm):
    class Meta:
        model =CustomUser
        fields = ['username', 'email', 'password', 'is_student', 'phone', 'state', 'country']
        
        
class ForgotPwdForm(ModelForm):
    class Meta:
        model =CustomUser
        fields = [ 'email', ]
        
        
class LoginForm(ModelForm):
    class Meta:
        model =CustomUser
        fields = ['username', 'password']
        
        
class GCEform(ModelForm):
    class Meta:
        model = GCE
        fields ='__all__'
        
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields ='__all__'
        
    

class CommentForm(ModelForm):
    class Meta:
        model = PostComments
        fields = ('heading', 'email', 'body')
       
        

