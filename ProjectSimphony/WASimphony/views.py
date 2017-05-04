from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from .models import FileDb
from Symphony.symphony_parser import parse_file
from django.views.decorators.csrf import csrf_exempt
import os.path
from os.path import join
import logging

# Create your views here.
def empty_view(request):
    return HttpResponseRedirect(reverse('home_page'))

def home_view(request):
    return render(request, 'home.html', {'page_title': 'Home'})

def course_view(request):
    return render(request, 'course.html', {'page_title': 'Course'})

def course_welcome_view(request):
    return render(request, 'course_welcome.html', {'page_title': 'Course | Welcome'})

def course_variables_view(request):
    return render(request, 'course_variables.html', {'page_title': 'Course | Variables'})

def course_booleans_view(request):
    return render(request, 'course_booleans.html', {'page_title': 'Course | Booleans'})

def course_assign_values_view(request):
    return render(request, 'course_assign_values.html', {'page_title': 'Course | Assign Values'})

def course_math_view(request):
    return render(request, 'course_math.html', {'page_title': 'Course | Math'})

def course_exponentation_view(request):
    return render(request, 'course_exponentation.html', {'page_title': 'Course | Exponentation'})

def course_modulo_view(request):
    return render(request, 'course_modulo.html', {'page_title': 'Course | Modulo'})

def course_strings_view(request):
    return render(request, 'course_strings.html', {'page_title': 'Course | Strings'})

def course_string_methods_view(request):
    return render(request, 'course_string_methods.html', {'page_title': 'Course | String Methods'})

def course_printing_strings_view(request):
    return render(request, 'course_printing_strings.html', {'page_title': 'Course | Printing Strings'})

def course_printing_variables_view(request):
    return render(request, 'course_printing_variables.html', {'page_title': 'Course | Printing Variables'})

def course_string_concatenation_view(request):
    return render(request, 'course_string_concatenation.html', {'page_title': 'Course | String Concatenation'})

def course_comparators_view(request):
    return render(request, 'course_comparators.html', {'page_title': 'Course | Comparators'})

def course_boolean_operators_view(request):
    return render(request, 'course_boolean_operators.html', {'page_title': 'Course | Boolean Operators'})

def course_if_else_elseif_view(request):
    return render(request, 'course_if_else_elseif.html', {'page_title': 'Course | IF, ELSE & ELSEIF'})

def course_functions_view(request):
    return render(request, 'course_functions.html', {'page_title': 'Course | Functions'})

def course_call_and_response_view(request):
    return render(request, 'course_call_and_response.html', {'page_title': 'Course | Call and Response'})

def course_parameters_and_arguments_view(request):
    return render(request, 'course_parameters_and_arguments.html', {'page_title': 'Course | Parameters and Arguments'})

def course_functions_calling_functions_view(request):
    return render(request, 'course_functions_calling_functions.html', {'page_title': 'Course | Functions Calling Functions'})

def course_built_in_functions_view(request):
    return render(request, 'course_built_in_functions.html', {'page_title': 'Course | Built-In Functions'})

def course_while_loops_view(request):
    return render(request, 'course_while_loops.html', {'page_title': 'Course | While Loops'})

def simphony_view(request):
    return render(request, 'simphony.html', {'page_title': 'Symphony'})

def simphony_iterative_factorial_view(request):
    return render(request, 'simphony_iterative_factorial.html', {'page_title': 'Symphony | Iterative Factorial'})

def simphony_recursive_factorial_view(request):
    return render(request, 'simphony_recursive_factorial.html', {'page_title': 'Symphony | Recursive Factorial'})

def simphony_iterative_fibonacci_view(request):
    return render(request, 'simphony_iterative_fibonacci.html', {'page_title': 'Symphony | Iterative Fibonacci'})

def simphony_recursive_fibonacci_view(request):
    return render(request, 'simphony_recursive_fibonacci.html', {'page_title': 'Symphony | Recursive Fibonacci'})

def simphony_bubble_sort_view(request):
    return render(request, 'simphony_bubble_sort.html', {'page_title': 'Symphony | Bubble Sort'})

def simphony_find_vector_view(request):
    return render(request, 'simphony_find_vector.html', {'page_title': 'Symphony | Find Vector'})

def simphony_musical_loop_view(request):
    return render(request, 'simphony_musical_loop.html', {'page_title': 'Symphony | Musical Loop'})


@csrf_exempt
def execute_code_view(request):

    if request.is_ajax():
        logger = logging.getLogger(__name__)
        #extract your params (also, remember to validate them)
        program = request.POST.get('program', None)
        inputs = request.POST.get('inputs', None)

        BASE = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE, "test.sym")
        #print(file_path)
        with open(file_path, 'w+') as f:
            f.write(program)

        try:
            if inputs == '':
                inputs = None

            prints, notes = parse_file(file_path, inputs)
            prints = prints.replace('\n', '<br>')
            logger.critical(prints)
            logger.critical(notes)
        except Exception as e:
            prints = str(e)
            notes = None
        else:
            logger.critical("Success")

        return JsonResponse({'result': 'OK', 'data': {'prints' : prints, 'notes' : notes}})
    return HttpResponseBadRequest()

def single_file(request,id):
    file = FileDb.objects.get(id=id)
    filename = file.source.read()
    #save edited file:
    if request.method == "POST":
        from django.core.files import File
        f = open(file.source.path, 'w')
        content = request.POST['content']
        f.write(content)
        f = File(f)
        file.source = f
        file.save()


    return render_to_response('single_file.html',{'file':file,'filename':filename},context_instance=RequestContext(request))

def aboutus_view(request):
    return render(request, 'about_us.html', {'page_title': 'Home'})

def create_code_file(code_string, path):
    with open(path, 'w+') as file:
        file.write(code_string)

def login_view(request):
    if request.method == 'POST':
        # We get POST arguments.
        username = request.POST.get('inputUsername', '')
        password = request.POST.get('inputPassword', '')
        nextTo = request.POST.get('next', reverse('home_page'))
        if nextTo == 'None':
            nextTo = None
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            if nextTo is None:
                nextTo = reverse('home_page')
            return HttpResponseRedirect(nextTo)
        else:
            nextTo = None
    else:
        nextTo = request.GET.get('next', None)

    return render(request, 'login.html', {'page_title': 'Login', 'next': nextTo})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simphony.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simphony.html')

def logout_view(request):
    logout(request)
    #messages.success(request, 'Successfully logged out')
    return HttpResponseRedirect(reverse('login_page'))
