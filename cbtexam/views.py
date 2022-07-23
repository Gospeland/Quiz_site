from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse_lazy
from .forms import *
from .models import JAMB, NECO, SCORES, SSCE, CustomUser, Logo, Poll, Posts, Scholarships, Student_field
from django.http import HttpRequest, HttpResponse
from .forms import GCEform, RegisterForm, SubjectForm 
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, FormView, PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,  force_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from cbtexam.token import account_activation_token
from django.core.paginator import Paginator
from django.core.mail import send_mail



class PasswordReset(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name ='password_reset_email.html'
    subject_template_name ='password_reset_subject.txt'
    extra_email_context = None

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    
    
class PasswordResetComplete(PasswordResetDoneView):
    template_name = 'password_reset_complete.html'
    
class Index(ListView):
    model = Student_field
    template_name ='index.html'
    context_object_name = 'studentfields'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        context['gce'] = GCE.objects.all()
        context['neco'] = NECO.objects.all()
        context['waec'] = SSCE.objects.all()
        context['jamb'] = JAMB.objects.all()


        return context
    
class Choose(LoginRequiredMixin, ListView):
    model = Subject
    template_name ='choose.html'
    context_object_name = 'choose'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        
        return context
    
    
class AddQuestion(ListView):
    model = Subject
    template_name ='choose_exam.html'
    context_object_name = 'choose'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        
        return context
       
class SubjectJAMB(ListView):
    model = Subject
    template_name ='subjects.html'
    context_object_name = 'subjects'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        context['jamb'] = Subject.objects.filter(tag='jamb')


        return context

class SubjectJAMB(ListView):
    model = Subject
    template_name ='jambsubjects.html'
    context_object_name = 'subjects'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        context['jamb'] = Subject.objects.filter(tag='jamb')


        return context
    
    
class SubjectGCE(ListView):
    model = Subject
    template_name ='gcesubjects.html'
    context_object_name = 'subjects'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        context['gce'] = Subject.objects.filter(tag='gsce')

        return context
    
    
class SubjectNECO(ListView):
    model = Subject
    template_name ='necosubjects.html'
    context_object_name = 'subjects'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        context['neco'] = Subject.objects.filter(tag='neco')


        return context
    
    
class SubjectSSCE(ListView):
    model = Subject
    template_name ='sscesubjects.html'
    context_object_name = 'subjects'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        context['ssce'] = Subject.objects.filter(tag='ssce')


        return context


class QuestionGCE(LoginRequiredMixin,  CreateView):
    model = GCE
    template_name ='addquestiongce.html'
    fields = ['question', 'year', 'author_subject',  'op1', 'op2', 'op3', 'op4', 'ans']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionGCE, self).form_valid(form)
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications']= Scholarships.objects.all()
        return context
    
    
class QuestionNECO(LoginRequiredMixin,  CreateView):
    model = NECO
    template_name ='addquestionneco.html'
    fields = ['question', 'year', 'author_subject',  'op1', 'op2', 'op3', 'op4', 'ans']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionNECO, self).form_valid(form)
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications']= Scholarships.objects.all()
        return context
    
    
class QuestionSSCE(LoginRequiredMixin,  CreateView):
    model = SSCE
    template_name ='addquestionssce.html'
    fields = ['question', 'year', 'author_subject',  'op1', 'op2', 'op3', 'op4', 'ans']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionSSCE, self).form_valid(form)
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications']= Scholarships.objects.all()
        return context
    
    
class QuestionJAMB(LoginRequiredMixin,  CreateView):
    model = JAMB
    template_name ='addquestionjamb.html'
    fields = ['question', 'year', 'author_subject',  'op1', 'op2', 'op3', 'op4', 'ans']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionJAMB, self).form_valid(form)
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications']= Scholarships.objects.all()
        return context
    
 
'''def addQuestion(request):    
    if request.user.is_teacher or request.user.is_superuser:
        form=QuesModelForm()
        if(request.method=='POST'):
            form=QuesModelForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'addQuestion.html',context)
    else: 
        return redirect('home') 
 
 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form = RegisterForm()
        if request.method=='POST':
            form = RegisterForm(request.POST)
            if form.is_valid() :
                request.user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'register.html',context)
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'login.html',context)
 
def logoutPage(request):
    logout(request)
    return redirect('/')'''


class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    redirect_authenticated_user = True
    
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            user =form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active =False
            user.save()
            
            current_site = get_current_site(request)
            subject ='Activate Your Account'
            message =render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please ' + user.username + ' Confirm your email to complete registration'))
            return redirect('register')
        return render(request, self.template_name, {'form':form})


    '''def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(
            form.cleaned_data["password"]
        )
        user=form.save(commit=True)
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)'''
    
    
class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user =CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user =None
            
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active =True
            user.save()
            messages.success(request, ('Your account has been confirmed. Please Login Now'))
            return redirect('login')
        else:
            messages.warning(request, ('Validation of account fatally failed'))
            return redirect('login')
            


class LoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True


class CustomLogout(LogoutView):
    pass


class Postlist(ListView):
    model = Posts
    template_name ='pubs.html'
    context_object_name = 'posts'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications']= Posts.objects.all()
        return context


def post_detail(request, slug):
    #similar posts starts here
    pub = Posts.objects.get(slug=slug)
    #comment starts here
    post = get_object_or_404(Posts, slug=slug)
    comments = pub.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.author =request.user
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'pub': pub,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'details.html', context)
    
    
class PubCreate(LoginRequiredMixin,  CreateView):
    model = Posts
    template_name ='createpub.html'
    fields = ['title', 'description', 'image']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('publications')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PubCreate, self).form_valid(form)
 
 
class UpdatePub(LoginRequiredMixin,  UpdateView):
    model = Posts
    fields = ['title', 'description', 'image']
    template_name ='createpub.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('details', kwargs={'slug':self.object.slug})
       
    
class DeletePub(LoginRequiredMixin,  DeleteView):
    model = Posts
    template_name ='deletepub.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('publications')
   
    
class Scholarshiplist(ListView):
    model = Scholarships
    template_name ='scholarships.html'
    context_object_name = 'scholarships'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications']= Scholarships.objects.all()
        return context


def scholarshipdetail(request, slug):
    #similar posts starts here
    pub = Scholarships.objects.get(slug=slug)
    #comment starts here
    post = get_object_or_404(Scholarships, slug=slug)
    comments = pub.scholarshipcomments.filter(active=True).order_by('-created_on')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.author =request.user
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'pub': pub,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'scholarshipdetails.html', context)
    

class ScholarshipCreate(LoginRequiredMixin,  CreateView):
    model = Scholarships
    template_name ='createscholarship.html'
    fields = ['title', 'description', 'image']
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('portal')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PubCreate, self).form_valid(form)
 
 
class UpdateScholarship(LoginRequiredMixin,  UpdateView):
    model = Scholarships
    fields = ['title', 'description', 'image']
    template_name ='createscholarship.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('scholarshipdetails', kwargs={'slug':self.object.slug})
    
    
class UpdateScholarshipNewsletter(LoginRequiredMixin,  UpdateView):
    model = Scholarships
    fields = ['title', 'description', 'image']
    template_name ='createscholarship.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('scholarshipdetails', kwargs={'slug':self.object.slug})
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        don = form.instance.title
        author = form.instance.author
        post = form.instance.description[:200]
        current_site = get_current_site(self.request)
        from_email = 'admin@gmail.com'
        receivers = []
        for userman in CustomUser.objects.all():
            receivers.append(userman.email)
        subject ='Our Latest Post: ' + don + '.'
        message =render_to_string( 'newsletter_email.html', {
                     'post': post,
                    'domain': current_site.domain,
                    'don': don,
                    'author': author

                })
        send_mail(subject, message, from_email, receivers)
        messages.success(self.request, ('Please ' + self.request.user.username + 'Verify your newsletter is sent by checking your inbox'))
        return super(UpdateScholarshipNewsletter, self).form_valid(form)

       
    
class DeleteScholarship(LoginRequiredMixin,  DeleteView):
    model = Scholarships
    template_name ='deletepub.html'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('scholarshiplist')
    
    
class AboutUs(LoginRequiredMixin,  ListView):
    model = CustomUser
    template_name = 'aboutus.html' 
    
    def get_context_data(self, **kwargs):   
            context = super().get_context_data(**kwargs)
            context['logos'] = Logo.objects.all()

            return context     
        

class Studentprofile(LoginRequiredMixin,  ListView):
    model =  CustomUser  
    template_name = 'studentdata.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users1'] = self.request.user
        context['logos'] = Logo.objects.all()
        context['results'] = SCORES.objects.filter(student_name=self.request.user).order_by('date_taken')

        return context
    
@csrf_exempt
def ssceexams(request, pk):
    title ='SSCE'
    logos = Logo.objects.all()
    questions=SSCE.objects.order_by('?').filter(author_subject__pk = pk)
    if request.method == 'POST':
        thelist =request.POST.items()
        score=0
        wrong=0
        correct=0
        total=0
        answ = []

        for q in questions:
            total+=1
            if q.ans == request.POST.get(q.question):
                score+=10
                correct+=1
                answ.append(q.ans)
            else:
                wrong+=1
        percent = score/(total*10) *100
         
        exam =title
        correctt =correct
        incorrect = wrong
        total_score = percent
        student =request.user
        subject = q.author_subject
        subject_class =q.author_class
        person = SCORES(author_subject=subject, author_class=subject_class, exam=exam, incorrect=incorrect, total_score=total_score, correct =correctt, student_name =student,   )
        person.save()
        
        context = {
            'exam':exam,
            'correctt':correctt,
            'incorrect':incorrect,
            'total_score':total_score,
            'student':student,
            'subject_class':subject_class,
            'subject':subject,

            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'questions': questions,
            'answ': answ,
            'thelist': thelist,
            'logos': logos,
            'title': title

        }
        return render(request,'result.html', context)
    else:
        questions=SSCE.objects.order_by('?').filter(author_subject = pk)
        exam_list = questions
        
        paginator = Paginator(exam_list, 1)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'questions':questions,
            'logos': logos,
            'title': title

        }
        return render(request,'home.html',context)
    


@csrf_exempt
def gceexams(request, pk):
    title ='GCE'
    logos = Logo.objects.all()
    questions=GCE.objects.order_by('?').filter(author_subject__pk = pk)
    if request.method == 'POST':
        thelist =request.POST.items()
        score=0
        wrong=0
        correct=0
        total=0
        answ = []

        for q in questions:
            total+=1
            if q.ans == request.POST.get(q.question):
                score+=10
                correct+=1
                answ.append(q.ans)
            else:
                wrong+=1
        percent = score/(total*10) *100
         
        exam =title
        correctt =correct
        incorrect = wrong
        total_score = percent
        student =request.user
        subject = q.author_subject
        subject_class =q.author_class
        person = SCORES(author_subject=subject, author_class=subject_class, exam=exam, incorrect=incorrect, total_score=total_score, correct =correctt, student_name =student,   )
        person.save()
        
        context = {
            'exam':exam,
            'correctt':correctt,
            'incorrect':incorrect,
            'total_score':total_score,
            'student':student,
            'subject_class':subject_class,
            'subject':subject,

            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'questions': questions,
            'answ': answ,
            'thelist': thelist,
            'logos': logos,
            'title': title

        }
        return render(request,'result.html', context)
    else:
        questions=GCE.objects.order_by('?').filter(author_subject = pk)
        context = {
            'questions':questions,
            'logos': logos,
            'title': title, 
        }
        return render(request,'home.html',context)
    
@csrf_exempt
def jambexams(request, pk):
    title ='JAMB'
    logos = Logo.objects.all()
    questions=JAMB.objects.order_by('?').filter(author_subject__pk = pk)
    '''for qua in questions:
        quest = qua.question
        ans =qua.ans'''
    if request.method == 'POST':
        thelist =request.POST.items()
        score=0
        wrong=0
        correct=0
        total=0
        answ = []

        for q in questions:
            total+=1
            if q.ans == request.POST.get(q.question):
                score+=10
                correct+=1
                answ.append(q.ans)
            else:
                wrong+=1
        percent = score/(total*10) *100
         
        exam =title
        correctt =correct
        incorrect = wrong
        total_score = percent
        student =request.user
        subject = q.author_subject
        subject_class =q.author_class
        person = SCORES(author_subject=subject, author_class=subject_class, exam=exam, incorrect=incorrect, total_score=total_score, correct =correctt, student_name =student,   )
        person.save()
        
        context = {
            'exam':exam,
            'correctt':correctt,
            'incorrect':incorrect,
            'total_score':total_score,
            'student':student,
            'subject_class':subject_class,
            'subject':subject,

            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'questions': questions,
            'answ': answ,
            '''ans': ans,
            'quest': quest,'''
            'thelist': thelist,
            'logos': logos,
            'title': title
        }
        return render(request,'result.html', context)
    else:
        questions=JAMB.objects.order_by('?').filter(author_subject = pk)
        context = {
            'questions':questions,
            'logos': logos,
            'title': title
        }
        return render(request,'home.html',context)
    
@csrf_exempt
def necoexams(request, pk):
    title ='NECO'
    logos = Logo.objects.all()
    questions=NECO.objects.order_by('?').filter(author_subject__pk = pk)
    if request.method == 'POST':
        thelist =request.POST.items()
        score=0
        wrong=0
        correct=0
        total=0
        answ = []

        for q in questions:
            total+=1
            if q.ans == request.POST.get(q.question):
                score+=10
                correct+=1
                answ.append(q.ans)
            else:
                wrong+=1
        percent = score/(t
                         otal*10) *100
        
        exam =title
        correctt =correct
        incorrect = wrong
        total_score = percent
        student =request.user
        subject = q.author_subject
        subject_class =q.author_class
        person = SCORES(author_subject=subject, author_class=subject_class, exam=exam, incorrect=incorrect, total_score=total_score, correct =correctt, student_name =student,   )
        person.save()
        
        context = {
            'exam':exam,
            'correctt':correctt,
            'incorrect':incorrect,
            'total_score':total_score,
            'student':student,
            'subject_class':subject_class,
            'subject':subject,

            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'questions': questions,
            'answ': answ,
            'thelist': thelist,
            'logos': logos,
            'title': title
        }
        return render(request,'result.html', context)
    else:
        title ='NECO'
        questions=NECO.objects.order_by('?').filter(author_subject = pk)
        context = {
            'questions':questions,
            'logos': logos,
            'title': title

        }
        return render(request,'home.html',context)
    
    
class CreateSubject(LoginRequiredMixin,  CreateView):
    model = Subject
    template_name ='createsubject.html'
    fields = ['name', 'subject_class' ,'tag', 'slug' ]
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('choose')
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super(CreateSubject, self).form_valid(form)
   
    
class Premium(LoginRequiredMixin,  ListView):
    model = Subject
    template_name ='premium.html'
    fields = '__all__'
    redirect_authenticated_user =True
    
    def get_success_url(self):
        return reverse_lazy('choose')
    
    def form_valid(self, form):
        return super(Premium, self).form_valid(form)#
    
    
class Pollview(LoginRequiredMixin,  ListView):
    model = Poll
    template_name ='poll.html'


@csrf_exempt
def polls(request, pk):
    title ='polls'
    logos = Logo.objects.all()
    u=Poll.objects.get(pk =pk)

    voterlist =[]
    
    if request.method == 'POST':
        voterlist.append(request.user.username)
        u.voter =voterlist
        if u.op1==request.POST.get('option'):
            u.op1score+=1
            u.save()
        elif  u.op2 == request.POST.get('option'):
            u.op2score+=1
            u.save()
        elif u.op3 == request.POST.get('option'): 
            u.op3score+=1
            u.save()
        elif u.op4 == request.POST.get('option'): 
            u.op4score+=1
            u.save()
            
        exam =title
        
        
        context = {
            'u':u,
            'exam':exam,
            
            'title': title
        }
        return render(request,'result copy.html', context)
    else:
        u=Poll.objects.get(pk =pk)
        context = {
            'u':u,
            'logos': logos,
            'title': title
        }
        return render(request,'home copy.html', context)