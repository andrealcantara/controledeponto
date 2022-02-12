from controle_de_ponto import settings


def runtime_variable(request):
    data = {}
    data['DJANGO_LANG'] = 'lang={}'.format(settings.LANGUAGE_CODE)
    return data
