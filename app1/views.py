from django.shortcuts import render
from django.http import HttpResponse
from . import calculate as calc


def NOx(request):
    coal_params = {}
    if request.method == 'POST':
        coal_params = {
            'Wr': float(request.POST.get('Wr')),
            'Ar': float(request.POST.get('Ar')),
            'Vr': float(request.POST.get('Vr')),
            'Nd': float(request.POST.get('Nd')),
            'alpha_g': float(request.POST.get('alpha_g')),
            'alpha_1': float(request.POST.get('alpha_1')),
            'R': float(request.POST.get('R')),
            'T_zag': float(request.POST.get('T_zag')),
            'w2_w1': float(request.POST.get('w2_w1')),
            'delta_alpha_T': float(request.POST.get('delta_alpha_T')),
            'Vr0': float(request.POST.get('Vr0')),
            'Vv0': float(request.POST.get('Vv0')),
            'V_H2O0': float(request.POST.get('V_H2O0')),
            'Qi_r': float(request.POST.get('Qi_r')),
            'Vg': float(request.POST.get('Vg')),
            'Bp': float(request.POST.get('Bp')),
            'Kp': float(request.POST.get('Kp')),
            'burner_type': request.POST.get('burner_type'),
            'extra_fuel': request.POST.get('extra_fuel'),
            'delta': float(request.POST.get('delta'))
        }
        itog = calc.calculate_nox_coal_boiler(coal_params)

        coal_params = {**coal_params, **itog}

    return render(request, 'NOx.html', {'form_data': coal_params})

def NOx_fuel(request):
    coal_params = {}
    if request.method == 'POST':
        coal_params = {
            'T_ad': float(request.POST.get('T_ad')),  # Ожидаемая адиабатная температура, К
            'psi_ZAG': float(request.POST.get('psi_ZAG')),  # Коэффициент отражения теплового потока (1 - тепловая эффективность)
            'a_T': float(request.POST.get('a_T')),  # Ширина топки в свету, м
            'b_T': float(request.POST.get('b_T')),  # Глубина топки в свету, м
            'h_ZAG': float(request.POST.get('h_ZAG')),  # Высота зоны активного горения, м
            'Bp': float(request.POST.get('Bp')),  # Расход топлива, м3/с
            'Vr_Rg': float(request.POST.get('Vr_Rg')),  # Объем продуктов сгорания, м3/м3
            'xi': float(request.POST.get('xi')),  # Коэффициент заполнения топочной камеры
            'q_ZAG': float(request.POST.get('q_ZAG')),  # Тепловая нагрузка зоны активного горения, перевели МВт/м2 -> Вт/м2
            'fuel_type': request.POST.get('fuel_type'),  # Тип топлива: газ
            'Kg': float(request.POST.get('Kg')),  # Коэффициент конструкции горелочного устройства
            'alpha_ZAG': float(request.POST.get('alpha_ZAG')),  # Коэффициент избытка воздуха в горелках
            'Nr': float(request.POST.get('Nr')),  # Содержание азота, перевели в долю
            'Vr': float(request.POST.get('Vr')),  # Объем продуктов сгорания, м3/м3
            'Vsg0': float(request.POST.get('Vsg0')),  # Теоретический объем сухих газов, м3/м3
            'Vv0': float(request.POST.get('Vv0')),  # Теоретический объем воздуха для полного сжигания топлива, м3/м3
            'R': float(request.POST.get('R')),  # Доля газов рециркуляции
            'Vg': float(request.POST.get('Vg')),  # Объем дымовых газов, м3/м3
            'Kp': float(request.POST.get('Kp'))  # Коэффициент конструкции горелочного устройства (как поправочный)
        }

        itog = calc.calculate_nox_gas_oil_boiler(coal_params)
        coal_params = {**coal_params, **itog}
    return render(request, 'NOx_fuel.html', {'form_data': coal_params})


def SOx(request):
    form_data = {}
    if request.method == 'POST':
        form_data = {
            'B': float(request.POST.get('B', '')),
            'S_r': float(request.POST.get('S_r', '')),
            'n1_SO2': float(request.POST.get('n1_SO2', '')),
            'n2_SO2':float(request.POST.get('n2_SO2', '')),
            'itog': 0
        }
        form_data['itog'] = 0.02*form_data['B']*form_data['S_r']*(1-form_data['n1_SO2'])*(1-form_data['n2_SO2'])*1000
    return render(request, 'SOx.html', {'form_data':form_data})

def home(request):
    return render(request, 'home.html')

