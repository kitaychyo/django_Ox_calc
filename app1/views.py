import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import calculate as calc
from .models import SOx_save, NOx_save, NOx_fuel_save
from django.views.decorators.http import require_http_methods

# Общая функция для извлечения данных формы
def extract_form_data(request, fields):
    form_data = {}
    for field, field_type in fields.items():
        value = request.POST.get(field)
        try:
            form_data[field] = field_type(value) if value else 0
        except (ValueError, TypeError):
            form_data[field] = value or ''
    return form_data

# Общая функция для создания текстового контента
def create_text_content(title, form_data):
    content = f"=== {title} ===\n\n"
    for key, value in form_data.items():
        content += f"{key}: {value}\n"
    content += "\n=====================================\n"
    return content

# Общая функция для сохранения в модель
def save_to_model(model_class, form_data, fields):
    article = model_class(**{k: form_data[k] for k in fields})
    article.save()

# Поля для каждой формы
NOX_FIELDS = {
    'Wr': float, 'Ar': float, 'Vr': float, 'Nd': float, 'alpha_g': float, 'alpha_1': float,
    'R': float, 'T_zag': float, 'w2_w1': float, 'delta_alpha_T': float, 'Vr0': float,
    'Vv0': float, 'V_H2O0': float, 'Qi_r': float, 'Vg': float, 'Bp': float, 'Kp': float,
    'burner_type': str, 'extra_fuel': str, 'delta': float, 'name': str
}

NOX_FUEL_FIELDS = {
    'T_ad': float, 'psi_ZAG': float, 'a_T': float, 'b_T': float, 'h_ZAG': float, 'Bp': float,
    'Vr_Rg': float, 'xi': float, 'q_ZAG': float, 'fuel_type': str, 'Kg': float, 'alpha_ZAG': float,
    'Nr': float, 'Vr': float, 'Vsg0': float, 'Vv0': float, 'R': float, 'Vg': float, 'Kp': float, 'name': str
}

SOX_FIELDS = {
    'B': float, 'S_r': float, 'n1_SO2': float, 'n2_SO2': float, 'name': str
}

@require_http_methods(["GET", "POST"])
def NOx(request):
    form_data = {}
    saved_calculations = NOx_save.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'load' in request.POST:
            try:
                selected_calc = NOx_save.objects.get(id=request.POST.get('calculation_id'))
                form_data = {field: getattr(selected_calc, field) for field in NOX_FIELDS}
                form_data['flag'] = 1
            except NOx_save.DoesNotExist:
                form_data['error'] = "Calculation not found."
        else:
            form_data = extract_form_data(request, NOX_FIELDS)
            itog = calc.calculate_nox_coal_boiler(form_data)
            form_data.update(itog)

            if 'save' in request.POST:
                all_fields = set(NOX_FIELDS.keys()) | {'specific_emissions', 'concentration', 'emission_power'}
                save_to_model(NOx_save, form_data, all_fields)
            elif 'download' in request.POST:
                content = create_text_content("Расчет выбросов NOx (угольный котел)", form_data)
                return HttpResponse(
                    content_type='application/text',
                    headers={'Content-Disposition': 'attachment; filename="NOx_calculation.txt"'},
                    content=content.encode('utf-8')
                )

    return render(request, 'NOx.html', {'form_data': form_data, 'saved_calculations': saved_calculations})

@require_http_methods(["GET", "POST"])
def NOx_fuel(request):
    form_data = {}
    saved_calculations = NOx_fuel_save.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'load' in request.POST:
            try:
                selected_calc = NOx_fuel_save.objects.get(id=request.POST.get('calculation_id'))
                form_data = {field: getattr(selected_calc, field) for field in NOX_FUEL_FIELDS}
                form_data['flag'] = 1
            except NOx_fuel_save.DoesNotExist:
                form_data['error'] = "Calculation not found."
        else:
            form_data = extract_form_data(request, NOX_FUEL_FIELDS)
            itog = calc.calculate_nox_gas_oil_boiler(form_data)
            form_data.update(itog)

            if 'save' in request.POST:
                save_to_model(NOx_fuel_save, form_data, NOX_FUEL_FIELDS | {'concentration', 'standard_concentration', 'emission_power'})
            elif 'download' in request.POST:
                content = create_text_content("Расчет выбросов NOx (газ/мазут)", form_data)
                return HttpResponse(
                    content_type='application/text',
                    headers={'Content-Disposition': 'attachment; filename="NOx_fuel_calculation.txt"'},
                    content=content.encode('utf-8')
                )

    return render(request, 'NOx_fuel.html', {'form_data': form_data, 'saved_calculations': saved_calculations})

@require_http_methods(["GET", "POST"])
def SOx(request):
    form_data = {}
    saved_calculations = SOx_save.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'load' in request.POST:
            try:
                selected_calc = SOx_save.objects.get(id=request.POST.get('calculation_id'))
                form_data = {field: getattr(selected_calc, field) for field in SOX_FIELDS}
                form_data['itog'] = selected_calc.itog
            except SOx_save.DoesNotExist:
                form_data['error'] = "Calculation not found."
        else:
            form_data = extract_form_data(request, SOX_FIELDS)
            try:
                form_data['itog'] = 0.02 * form_data['B'] * form_data['S_r'] * (1 - form_data['n1_SO2']) * (1 - form_data['n2_SO2']) * 1000
            except (ValueError, TypeError):
                form_data['error'] = "Invalid input data."

            if 'save' in request.POST:
                save_to_model(SOx_save, form_data, SOX_FIELDS | {'itog'})
            elif 'download' in request.POST:
                content = create_text_content("Расчет выбросов SOx", form_data)
                return HttpResponse(
                    content_type='application/text',
                    headers={'Content-Disposition': 'attachment; filename="SOx_calculation.txt"'},
                    content=content.encode('utf-8')
                )

    return render(request, 'SOx.html', {'form_data': form_data, 'saved_calculations': saved_calculations})

def home(request):
    if request.method == 'POST' and 'file' in request.FILES:
        try:
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            result = {}
            for line in content.splitlines():
                if line.strip().startswith('===') or not line.strip():
                    continue
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                    result[key] = value

            # Проверка для NOx (угольный котел)
            if len(result) == len(NOX_FIELDS) + 3 or len(result) == len(NOX_FIELDS):
                saved_calculations = NOx_save.objects.all().order_by('-created_at')
                if len(result) == len(NOX_FIELDS):  # Выполнить расчет, если результатов нет
                    result.update(calc.calculate_nox_coal_boiler(result))
                return render(request, 'NOx.html', {'form_data': result, 'saved_calculations': saved_calculations})

            # Проверка для SOx
            elif len(result) == len(SOX_FIELDS) + 1 or len(result) == len(SOX_FIELDS):
                saved_calculations = SOx_save.objects.all().order_by('-created_at')
                if len(result) == len(SOX_FIELDS):  # Выполнить расчет, если результата нет
                    result['itog'] = 0.02 * result['B'] * result['S_r'] * (1 - result['n1_SO2']) * (1 - result['n2_SO2']) * 1000
                return render(request, 'SOx.html', {'form_data': result, 'saved_calculations': saved_calculations})

            # Проверка для NOx (газ/мазут)
            elif len(result) == len(NOX_FUEL_FIELDS) + 3 or len(result) == len(NOX_FUEL_FIELDS):
                saved_calculations = NOx_fuel_save.objects.all().order_by('-created_at')
                if len(result) == len(NOX_FUEL_FIELDS):  # Выполнить расчет, если результатов нет
                    result.update(calc.calculate_nox_gas_oil_boiler(result))
                return render(request, 'NOx_fuel.html', {'form_data': result, 'saved_calculations': saved_calculations})

            else:
                return render(request, 'home.html', {'error': f'Invalid file format or number of parameters. Found {len(result)} parameters.'})

        except Exception as e:
            return render(request, 'home.html', {'error': f'Error processing file: {str(e)}'})

    return render(request, 'home.html')