from django.shortcuts import render
from django.http import HttpResponse
from . import calculate as calc
from .models import SOx_save, NOx_save, NOx_fuel_save


def handle_save(model, data):
    """Сохраняет расчет в модель."""
    return model.objects.create(**{k: v for k, v in data.items() if k != 'itog'}, itog=data.get('itog', 0))


def handle_download(data, filename, title):
    """Создает текстовый файл для скачивания."""
    content = f"=== {title} ===\n\n" + "\n".join(f"{k}: {v}" for k, v in data.items()) + "\n\n==============\n"
    response = HttpResponse(content_type='text/plain', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
    response.write(content.encode('utf-8'))
    return response


def handle_load(model, calc_id):
    """Загружает расчет из модели."""
    calc = model.objects.get(id=calc_id)
    return {field: getattr(calc, field) for field in [f.name for f in model._meta.fields] if field != 'id'}


def NOx(request):
    form_data, saved_calculations = {}, NOx_save.objects.all().order_by('-created_at')
    params = ['Wr', 'Ar', 'Vr', 'Nd', 'alpha_g', 'alpha_1', 'R', 'T_zag', 'w2_w1', 'delta_alpha_T', 'Vr0', 'Vv0', 'V_H2O0', 'Qi_r', 'Vg', 'Bp', 'Kp', 'delta']
    str_params = ['burner_type', 'extra_fuel', 'name']

    if request.method == 'POST':
        if 'load' not in request.POST:
            form_data = {k: float(request.POST.get(k)) for k in params}
            form_data.update({k: request.POST.get(k, '') for k in str_params})
            form_data.update(calc.calculate_nox_coal_boiler(form_data))

            if 'save' in request.POST:
                handle_save(NOx_save, form_data)
            elif 'download' in request.POST:
                return handle_download(form_data, "NOx_calculation.txt", "Расчет выбросов NOx (угольный котел)")
        else:
            form_data = handle_load(NOx_save, request.POST.get('calculation_id'))

    return render(request, 'NOx.html', {'form_data': form_data, 'saved_calculations': saved_calculations})


def NOx_fuel(request):
    form_data, saved_calculations = {}, NOx_fuel_save.objects.all().order_by('-created_at')
    params = ['T_ad', 'psi_ZAG', 'a_T', 'b_T', 'h_ZAG', 'Bp', 'Vr_Rg', 'xi', 'q_ZAG', 'Kg', 'alpha_ZAG', 'Nr', 'Vr', 'Vsg0', 'Vv0', 'R', 'Vg', 'Kp']
    str_params = ['fuel_type', 'name']

    if request.method == 'POST':
        if 'load' not in request.POST:
            form_data = {k: float(request.POST.get(k)) for k in params}
            form_data.update({k: request.POST.get(k, '') for k in str_params})
            form_data.update(calc.calculate_nox_gas_oil_boiler(form_data))

            if 'save' in request.POST:
                handle_save(NOx_fuel_save, form_data)
            elif 'download' in request.POST:
                return handle_download(form_data, "NOx_fuel_calculation.txt", "Расчет выбросов NOx (газ/мазут)")
        else:
            form_data = handle_load(NOx_fuel_save, request.POST.get('calculation_id'))

    return render(request, 'NOx_fuel.html', {'form_data': form_data, 'saved_calculations': saved_calculations})


def SOx(request):
    form_data, saved_calculations = {}, SOx_save.objects.all().order_by('-created_at')
    params = ['B', 'S_r', 'n1_SO2', 'n2_SO2']

    if request.method == 'POST':
        if 'load' not in request.POST:
            form_data = {k: float(request.POST.get(k, 0)) for k in params}
            form_data['name'] = request.POST.get('name', '')
            form_data['itog'] = 0.02 * form_data['B'] * form_data['S_r'] * (1 - form_data['n1_SO2']) * (1 - form_data['n2_SO2']) * 1000

            if 'save' in request.POST:
                handle_save(SOx_save, form_data)
            elif 'download' in request.POST:
                return handle_download(form_data, "SOx_calculation.txt", "Расчет выбросов SOx")
        else:
            form_data = handle_load(SOx_save, request.POST.get('calculation_id'))

    return render(request, 'SOx.html', {'form_data': form_data, 'saved_calculations': saved_calculations})


def home(request):
    return render(request, 'home.html')