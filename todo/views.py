from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,ListView,DetailView,UpdateView,CreateView
from todo.forms import RegistrationForm,LoginForm,TaskForm,TaskChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from todo.models import Task
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"please login")
            return redirect("signin")
        return fn(request,*args,**kwargs)
    return wrapper

class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

    def form_valid(self,form):
        messages.success(self.request,"todo has been created")
        return super().form_valid(form)
    
    
    def form_invalid(self,form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)




    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"account has been created")
    #         return redirect("signin")
    #     messages.error(request,"failed to create account")
    #     return render(request,self.template_name,{"form":form})
    

class SignInView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pswd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            messages.error(request,"failed to login")
            return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"
    # def get(self,request,*args,**kwargs):
    #     return render(request,self.template_name)
    

@method_decorator(signin_required,name="dispatch")
class TaskCreateView(CreateView):
    model=Task
    form_class=TaskForm
    template_name="task-add.html"
    success_url=reverse_lazy("list")

    def form_valid(self,form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo has been created")
        return super().form_valid(form)

   
    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
            
    #         messages.success(request,"todo added successfully")
    #         return redirect("list")
    #     messages.error(request,"failed to create todo")
    #     return render(request,self.template_name,{"form":form})


@method_decorator(signin_required,name="dispatch")
class TaskListView(ListView):
    model=Task
    template_name="task-list.html"
    context_object_name="tasks"
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_date")
    # def get(self,request,*args,**kwargs):
    #     qs=Task.objects.filter(user=request.user).order_by("-created_date")
    #     return render(request,self.template_name,{"tasks":qs})


@method_decorator(signin_required,name="dispatch")
class TaskDetailView(DetailView):
    model=Task
    template_name="task-detail.html"
    context_object_name="task"

 

    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Task.objects.get(id=id)
    #     return render(request,self.template_name,{"task":qs})
    

@signin_required
def taskdelete_View(request,*args,**kwargs):
         id=kwargs.get("pk")
         obj=Task.objects.get(id=id)
         if obj.user==request.user:
            Task.objects.get(id=id).delete()
            messages.success(request,"task deleted")
            return redirect("list")
         else:
             messages.error(request,"you donot have the permission to perform this action")
             return redirect("signin")
    

@method_decorator(signin_required,name="dispatch")
class TaskUpdateView(UpdateView):
    model=Task
    template_name="task-edit.html"
    form_class=TaskChangeForm
    success_url=reverse_lazy("list")
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     task=Task.objects.get(id=id)
    #     form=self.form_class(instance=task)
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     task=Task.objects.get(id=id)
    #     form=self.form_class(instance=task,data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"task has been updated")
    #         return redirect("task-detail",pk=id)
    #     messages.error(request,"failed to update")
    #     return render(request,self.template_name,{"form":form})
    
def signout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logged out")
    return redirect("signin")


class PasswordResetView(FormView):
    model=User
    template_name="password-reset.html"
    form_class=PasswordResetForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pswd1=form.cleaned_data.get("password1")
            pswd2=form.cleaned_data.get("password2")

            if pswd1==pswd2:
                try:
                    usr=User.objects.get(username=uname,email=email)
                    usr.set_password(pswd1)
                    usr.save()
                    messages.success(request,"password has been changed")
                    return redirect("signin")
                except Exception as e:
                    messages.error(request,"invalid credentials")
                    return render(request,self.template_name,{"form":form})
            else:
                    messages.error(request,"password mismatch")
                    return render(request,self.template_name,{"form":form})

        


