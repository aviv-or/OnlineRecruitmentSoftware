from django.conf.urls import url, include
from django.views import View
from django.conf import settings
from django.conf.urls.static import static

from home.views import home, profile
from login.views import LoginHandler, LogoutHandler, RegisterUser, RegisterOrg
from admin.views import AdminLogin, AdminLogout, AdminProfile, VerifyOrganization
from organization.views import AddEmployee, RemoveEmployee
from employee.views import CreateProblemSet, CreateTestModule
from tests.views import BrowseTest, ViewTest, StartTest
from service.organization import users_data
from service.test_module import find_tests, remaining_time, questions,\
                                save_response, save_review, reviews
from service.problem_set import find_problem_sets
from service.test import test
from service import user

urlpatterns = [
    url(r'^$', home),
    url(r'^admin/login$', AdminLogin.as_view()),
    url(r'^admin/logout$', AdminLogout.as_view()),
    url(r'^admin/profile$', AdminProfile.as_view()),
    url(r'^admin/verify/(?P<org>.*)$', VerifyOrganization.as_view()),

    url(r'^login$', LoginHandler.as_view()),
    url(r'^logout$', LogoutHandler.as_view()),
    url(r'^register/user$', RegisterUser.as_view()),
    url(r'^register/organization$', RegisterOrg.as_view()),

    url(r'^profile$', profile),

    url(r'^organization/add-employee/(?P<user>.*)$', AddEmployee.as_view()),
    url(r'^organization/remove-employee/(?P<user>.*)$', RemoveEmployee.as_view()),

    url(r'^create/problem-set$', CreateProblemSet.as_view()),
    url(r'^create/test-module$', CreateTestModule.as_view()),

    url(r'^tests$', BrowseTest.as_view()),
    url(r'^test/start/(?P<test_id>.*)$', StartTest.as_view()),
    url(r'^test/(?P<test_id>.*)$', ViewTest.as_view()),

    url(r'^service/problem-sets$', find_problem_sets),
    url(r'^service/tests/time$', remaining_time),
    url(r'^service/tests/question$', questions),
    url(r'^service/tests/reviews$', reviews),
    url(r'^service/tests/save_response$', save_response),
    url(r'^service/tests/save_review$', save_review),
    url(r'^service/tests$', find_tests),
    url(r'^service/user/update$', user.change),    
    url(r'^service/users-data$', users_data),    
    url(r'^test$', test),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
