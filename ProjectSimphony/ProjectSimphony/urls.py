"""ProjectSimphony URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from WASimphony import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.empty_view),
    url(r'^home/$', views.home_view, name='home_page'),
    url(r'^course/$', views.course_view, name='course_page'),
    url(r'^course/syntax/welcome/$', views.course_welcome_view, name='course_welcome_page'),
    url(r'^course/syntax/variables/$', views.course_variables_view, name='course_variables_page'),
    url(r'^course/syntax/booleans/$', views.course_booleans_view, name='course_booleans_page'),
    url(r'^course/syntax/assign-values/$', views.course_assign_values_view, name='course_assign_variables_page'),
    url(r'^course/syntax/math/$', views.course_math_view, name='course_math_page'),
    url(r'^course/syntax/exponentation/$', views.course_exponentation_view, name='course_exponentation_page'),
    url(r'^course/syntax/modulo/$', views.course_modulo_view, name='course_modulo_page'),
    url(r'^course/strings/strings/$', views.course_strings_view, name='course_strings_page'),
    url(r'^course/strings/string-methods/$', views.course_string_methods_view, name='course_string_methods_page'),
    url(r'^course/console-output/printing-strings/$', views.course_printing_strings_view, name='course_printing_strings_page'),
    url(r'^course/console-output/printing-variables/$', views.course_printing_variables_view, name='course_printing_variables_page'),
    url(r'^course/strings/string-concatenation/$', views.course_string_concatenation_view, name='course_string_concatenation_page'),
    url(r'^course/conditionals/comparators/$', views.course_comparators_view, name='course_comparators_page'),
    url(r'^course/conditionals/boolean-operators/$', views.course_boolean_operators_view, name='course_boolean_operators_page'),
    url(r'^course/control-flow/IF-ELSE-ELSEIF/$', views.course_if_else_elseif_view, name='course_if_else_elseif_page'),
    url(r'^course/functions/functions/$', views.course_functions_view, name='course_functions_page'),
    url(r'^course/functions/call-and-response/$', views.course_call_and_response_view, name='course_call_and_response_page'),
    url(r'^course/functions/parameters-and-arguments/$', views.course_parameters_and_arguments_view, name='course_parameters_and_arguments_page'),
    url(r'^course/functions/functions-calling-functions/$', views.course_functions_calling_functions_view, name='course_unctions_calling_functions_page'),
    url(r'^course/functions/built-in-functions/$', views.course_built_in_functions_view, name='course_built_in_functions_page'),
    url(r'^course/loops/while-loops/$', views.course_while_loops_view, name='course_while_loops_page'),
    url(r'^symphony/$', views.simphony_view, name='symphony_page'),
    url(r'^symphony/examples/iterative-factorial/$', views.simphony_iterative_factorial_view, name='symphony_iterative_factorial_page'),
    url(r'^symphony/examples/recursive-factorial/$', views.simphony_recursive_factorial_view, name='symphony_recursive_factorial_page'),
    url(r'^symphony/examples/iterative-fibonacci/$', views.simphony_iterative_fibonacci_view, name='symphony_iterative_fibonacci_page'),
    url(r'^symphony/examples/recursive-fibonacci/$', views.simphony_recursive_fibonacci_view, name='symphony_recursive_fibonacci_page'),
    url(r'^symphony/examples/bubble-sort/$', views.simphony_bubble_sort_view, name='symphony_bubble_sort_page'),
    url(r'^symphony/examples/find-vector/$', views.simphony_find_vector_view, name='symphony_find_vector_page'),
    url(r'^symphony/examples/musical-loop/$', views.simphony_musical_loop_view, name='symphony_musical_loop_page'),
    url(r'^symphony/exec/$', views.execute_code_view, name='execute_code_view'),
    url(r'^about-us/$', views.aboutus_view, name='about_us_page'),
    url(r'^login/$', views.login_view, name='login_page'),
    url(r'^logout/$', views.logout_view),
    url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)