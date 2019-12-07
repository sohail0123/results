"""JNTU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alogin/',views.loginPage,name="alogin"),
    path('home/', views.homePage, name="home"),
    path('logout/', views.logOut, name="logout"),
    path('login_admin/',views.loginCheck,name="login_admin"),
    path('e_add/',views.addEmployee,name="e_add"),
    path('e_save/',views.saveEmployee,name="e_save"),
    path('e_view/',views.viewEmployee,name="e_view"),
    path('e_update&delete',views.update_Delete,name="e_update&delete"),
    path('e_update<int:e_id>/',views.updateEmployee,name='e_update'),
    path('f_update/',views.updateSave,name="f_update"),
    path('e_delete<int:e_id>/',views.deleteEmployee,name="e_delete"),
    path('elogin_check/',views.EmpLoginCeck.as_view()),
    path('s_marks/',views.SaveMarks.as_view()),
    path('update/<int:s_id>/',views.UpdateMarks.as_view()),
    path('s_update/',views.SaveMarks.as_view()),
    path('results/',views.results),
    path('get_result/',views.getResult,name="get_result"),
    path('print/',views.pdfGenerate,name="print"),
]

from django.conf.urls.static import static
from JNTU import settings

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
