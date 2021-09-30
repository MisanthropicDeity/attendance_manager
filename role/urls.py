from django.urls import path
from .views import home, register, dashboard, addcourse, CourseDetail, profile, get_data, room, api, mycourses, pdfview, studymaterial, leaverequest, save, delete, marks, cgpa, registerteacher, dashboardteacher, manualteacher, teacherroom, teacherleave, viewleave, teacherprofile
urlpatterns = [
    path('', home, name='home'),
    path('pdfview/',pdfview,name='pdfview'),
    path('register/', register, name='register'),
    path('dashboard/',dashboard, name='dashboard'),
    path('dashboard/addcourse',addcourse,name='addcourse'),
    path('dashboard/course<int:pk>',CourseDetail.as_view(),name='coursedetail'),
    path('dashboard/chart_data',get_data,name='chart_data'),
    path('profile/',profile,name='profile'),
    path('dashboard/course<int:pk>/room', room, name='room'),
    path('api/',api,name='api'),
    path('mycourses/',mycourses,name='mycourses'),
    path('dashboard/course<int:pk>/study',studymaterial,name='studymaterial'),
    path('dashboard/course<int:pk>/leave',leaverequest,name='leave'),
    path('save/',save,name="save"),
    path('delete/<int:course_pk>/<int:pk>/',delete,name="delete"),
    path('dashboard/course<int:pk>/marks/',marks,name='marks'),
    path('dashboard/cgpa',cgpa,name='cgpa'),
    path('registerteacher/',registerteacher,name='registerteacher'),
    path('dashboardteacher/',dashboardteacher,name='dashboardteacher'),
    path('dashboardteacher/manual',manualteacher,name='manualteacher'),
    path('dashboardteacher/teacherroom',teacherroom,name='teacherroom'),
    path('dashboardteacher/teacherleave',teacherleave,name='teacherleave'),
    path('view/<int:course_pk>/<int:pk>/',viewleave,name='viewleave'),
    path('dashboardteacher/teacherprofile/',teacherprofile,name='teacherprofile'),
]
