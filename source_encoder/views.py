from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, HttpResponse

from py3.py3_encode_utils import encode_py3
from js.js_encode_utils import encode_js
from .forms import UploadSourceCodeForm


def homepage(request):
    form = UploadSourceCodeForm()
    return render(request, 'homepage.html', {'form': form})


@require_http_methods(['POST'])
def encode_file(request):
    form = UploadSourceCodeForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest('Invalid submission')

    language_choice = int(request.POST.get('language'))
    source_text = request.FILES['source_file'].read().decode('utf-8')
    result_text = source_text
    file_name = 'unknown_language.txt'
    if language_choice == UploadSourceCodeForm.LANGUAGE_PYTHON_3:
        result_text = encode_py3(source_text, is_eval_wrap=False)
        file_name = 'encoded.py'
    elif language_choice == UploadSourceCodeForm.LANGUAGE_JS:
        result_text = encode_js(source_text, is_eval_wrap=False)
        file_name = 'encoded.js'

    response = HttpResponse(result_text, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
    return response
