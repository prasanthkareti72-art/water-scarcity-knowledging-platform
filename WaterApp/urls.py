from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),
			path("Signup.html", views.Signup, name="Signup"),
			path("SignupAction", views.SignupAction, name="SignupAction"),	    	
			path("UserLogin.html", views.UserLogin, name="UserLogin"),
			path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
			path("ShareKnowledge.html", views.ShareKnowledge, name="ShareKnowledge"),
			path("ShareKnowledgeAction", views.ShareKnowledgeAction, name="ShareKnowledgeAction"),
			path("AccessAdvice", views.AccessAdvice, name="AccessAdvice"),
			path("Download", views.Download, name="Download"),
			path("AccessMap", views.AccessMap, name="AccessMap"),
			path("Videos", views.Videos, name="Videos"),
]