from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import calculate as calc
from .models import SOx_save, NOx_save, NOx_fuel_save
import json
import csv


def NOx(request):
    form_data = {}
    saved_calculations = NOx_save.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'load' not in request.POST:
            form_data = {
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
                'delta': float(request.POST.get('delta')),
                'name': request.POST.get('name', '')
            }
            itog = calc.calculate_nox_coal_boiler(form_data)
            form_data = {**form_data, **itog}

            if 'save' in request.POST:
                # Сохранение расчета в базу данных
                article = NOx_save(
                    name=form_data['name'],
                    Wr=form_data['Wr'],
                    Ar=form_data['Ar'],
                    Vr=form_data['Vr'],
                    Nd=form_data['Nd'],
                    alpha_g=form_data['alpha_g'],
                    alpha_1=form_data['alpha_1'],
                    R=form_data['R'],
                    T_zag=form_data['T_zag'],
                    w2_w1=form_data['w2_w1'],
                    delta_alpha_T=form_data['delta_alpha_T'],
                    Vr0=form_data['Vr0'],
                    Vv0=form_data['Vv0'],
                    V_H2O0=form_data['V_H2O0'],
                    Qi_r=form_data['Qi_r'],
                    Vg=form_data['Vg'],
                    Bp=form_data['Bp'],
                    Kp=form_data['Kp'],
                    burner_type=form_data['burner_type'],
                    extra_fuel=form_data['extra_fuel'],
                    delta=form_data['delta'],
                    specific_emissions=form_data.get('specific_emissions', 0),
                    concentration=form_data.get('concentration', 0),
                    emission_power=form_data.get('emission_power', 0)
                )
                article.save()

            elif 'download' in request.POST:
                # Скачивание результатов в текстовом формате
                content = (
                    "=== Расчет выбросов NOx (угольный котел) ===\n"
                    "\n"
                    f"Название: {form_data['name']}\n"
                    f"Wr: {form_data['Wr']}\n"
                    f"Ar: {form_data['Ar']}\n"
                    f"Vr: {form_data['Vr']}\n"
                    f"Nd: {form_data['Nd']}\n"
                    f"alpha_g: {form_data['alpha_g']}\n"
                    f"alpha_1: {form_data['alpha_1']}\n"
                    f"R: {form_data['R']}\n"
                    f"T_zag: {form_data['T_zag']}\n"
                    f"w2_w1: {form_data['w2_w1']}\n"
                    f"delta_alpha_T: {form_data['delta_alpha_T']}\n"
                    f"Vr0: {form_data['Vr0']}\n"
                    f"Vv0: {form_data['Vv0']}\n"
                    f"V_H2O0: {form_data['V_H2O0']}\n"
                    f"Qi_r: {form_data['Qi_r']}\n"
                    f"Vg: {form_data['Vg']}\n"
                    f"Bp: {form_data['Bp']}\n"
                    f"Kp: {form_data['Kp']}\n"
                    f"Тип горелки: {form_data['burner_type']}\n"
                    f"Дополнительное топливо: {form_data['extra_fuel']}\n"
                    f"delta: {form_data['delta']}\n"
                    f"specific_emissions (г/с): {form_data.get('specific_emissions', 0):.2f}\n"
                    f"concentration (г/с): {form_data.get('concentration', 0):.2f}\n"
                    f"emission_power (г/с): {form_data.get('emission_power', 0):.2f}\n"
                    "\n"
                    "=====================================\n"
                )
                response = HttpResponse(
                    content_type='application/text',
                    headers={'Content-Disposition': 'attachment; filename="NOx_calculation.txt"'}
                )
                response.write(content.encode('utf-8'))
                return response

        elif 'load' in request.POST:
            calculation_id = request.POST.get('calculation_id')
            if calculation_id:
                # Загрузка сохраненного расчета из базы данных
                selected_calc = NOx_save.objects.get(id=calculation_id)
                form_data = {
                    'name': selected_calc.name,
                    'Wr': selected_calc.Wr,
                    'Ar': selected_calc.Ar,
                    'Vr': selected_calc.Vr,
                    'Nd': selected_calc.Nd,
                    'alpha_g': selected_calc.alpha_g,
                    'alpha_1': selected_calc.alpha_1,
                    'R': selected_calc.R,
                    'T_zag': selected_calc.T_zag,
                    'w2_w1': selected_calc.w2_w1,
                    'delta_alpha_T': selected_calc.delta_alpha_T,
                    'Vr0': selected_calc.Vr0,
                    'Vv0': selected_calc.Vv0,
                    'V_H2O0': selected_calc.V_H2O0,
                    'Qi_r': selected_calc.Qi_r,
                    'Vg': selected_calc.Vg,
                    'Bp': selected_calc.Bp,
                    'Kp': selected_calc.Kp,
                    'burner_type': selected_calc.burner_type,
                    'extra_fuel': selected_calc.extra_fuel,
                    'delta': selected_calc.delta,
                    'specific_emissions': selected_calc.specific_emissions,
                    'concentration': selected_calc.concentration,
                    'emission_power': selected_calc.emission_power,
                    'flag': 1
                }

    return render(request, 'NOx.html', {'form_data': form_data, 'saved_calculations': saved_calculations})


def NOx_fuel(request):
    form_data = {}
    saved_calculations = NOx_fuel_save.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'load' not in request.POST:
            form_data = {
                'T_ad': float(request.POST.get('T_ad')),  # Ожидаемая адиабатная температура, К
                'psi_ZAG': float(request.POST.get('psi_ZAG')),  # Коэффициент отражения теплового потока
                'a_T': float(request.POST.get('a_T')),  # Ширина топки в свету, м
                'b_T': float(request.POST.get('b_T')),  # Глубина топки в свету, м
                'h_ZAG': float(request.POST.get('h_ZAG')),  # Высота зоны активного горения, м
                'Bp': float(request.POST.get('Bp')),  # Расход топлива, м3/с
                'Vr_Rg': float(request.POST.get('Vr_Rg')),  # Объем продуктов сгорания, м3/м3
                'xi': float(request.POST.get('xi')),  # Коэффициент заполнения топочной камеры
                'q_ZAG': float(request.POST.get('q_ZAG')),  # Тепловая нагрузка зоны активного горения, Вт/м2
                'fuel_type': request.POST.get('fuel_type'),  # Тип топлива: газ
                'Kg': float(request.POST.get('Kg')),  # Коэффициент конструкции горелочного устройства
                'alpha_ZAG': float(request.POST.get('alpha_ZAG')),  # Коэффициент избытка воздуха в горелках
                'Nr': float(request.POST.get('Nr')),  # Содержание азота
                'Vr': float(request.POST.get('Vr')),  # Объем продуктов сгорания, м3/м3
                'Vsg0': float(request.POST.get('Vsg0')),  # Теоретический объем сухих газов, м3/м3
                'Vv0': float(request.POST.get('Vv0')),  # Теоретический объем воздуха, м3/м3
                'R': float(request.POST.get('R')),  # Доля газов рециркуляции
                'Vg': float(request.POST.get('Vg')),  # Объем дымовых газов, м3/м3
                'Kp': float(request.POST.get('Kp')),  # Поправочный коэффициент
                'name': request.POST.get('name', '')
            }
            itog = calc.calculate_nox_gas_oil_boiler(form_data)
            form_data = {**form_data, **itog}

            if 'save' in request.POST:
                # Сохранение расчета в базу данных
                article = NOx_fuel_save(
                    name=form_data['name'],
                    T_ad=form_data['T_ad'],
                    psi_ZAG=form_data['psi_ZAG'],
                    a_T=form_data['a_T'],
                    b_T=form_data['b_T'],
                    h_ZAG=form_data['h_ZAG'],
                    Bp=form_data['Bp'],
                    Vr_Rg=form_data['Vr_Rg'],
                    xi=form_data['xi'],
                    q_ZAG=form_data['q_ZAG'],
                    fuel_type=form_data['fuel_type'],
                    Kg=form_data['Kg'],
                    alpha_ZAG=form_data['alpha_ZAG'],
                    Nr=form_data['Nr'],
                    Vr=form_data['Vr'],
                    Vsg0=form_data['Vsg0'],
                    Vv0=form_data['Vv0'],
                    R=form_data['R'],
                    Vg=form_data['Vg'],
                    Kp=form_data['Kp'],
                    concentration=form_data.get('concentration', 0),
                    standard_concentration=form_data.get('standard_concentration', 0),
                    emission_power=form_data.get('emission_power', 0)
                )
                article.save()

            elif 'download' in request.POST:
                # Скачивание результатов в текстовом формате
                content = (
                    "=== Расчет выбросов NOx (газ/мазут) ===\n"
                    "\n"
                    f"Название: {form_data['name']}\n"
                    f"T_ad: {form_data['T_ad']}\n"
                    f"psi_ZAG: {form_data['psi_ZAG']}\n"
                    f"a_T: {form_data['a_T']}\n"
                    f"b_T: {form_data['b_T']}\n"
                    f"h_ZAG: {form_data['h_ZAG']}\n"
                    f"Bp: {form_data['Bp']}\n"
                    f"Vr_Rg: {form_data['Vr_Rg']}\n"
                    f"xi: {form_data['xi']}\n"
                    f"q_ZAG: {form_data['q_ZAG']}\n"
                    f"Тип топлива: {form_data['fuel_type']}\n"
                    f"Kg: {form_data['Kg']}\n"
                    f"alpha_ZAG: {form_data['alpha_ZAG']}\n"
                    f"Nr: {form_data['Nr']}\n"
                    f"Vr: {form_data['Vr']}\n"
                    f"Vsg0: {form_data['Vsg0']}\n"
                    f"Vv0: {form_data['Vv0']}\n"
                    f"R: {form_data['R']}\n"
                    f"Vg: {form_data['Vg']}\n"
                    f"Kp: {form_data['Kp']}\n"
                    f"concentration (г/с): {form_data.get('concentration', 0):.2f}\n"
                    f"standard_concentration: {form_data.get(' standard_concentration', 0):.2f}\n"
                    f"emission_power (г/с): {form_data.get('emission_power', 0):.2f}\n"
                    "\n"
                    "===================================\n"
                )
                response = HttpResponse(
                    content_type='application/text',
                    headers={'Content-Disposition': 'attachment; filename="NOx_fuel_calculation.txt"'}
                )
                response.write(content.encode('utf-8'))
                return response

        elif 'load' in request.POST:
            calculation_id = request.POST.get('calculation_id')
            if calculation_id:
                # Загрузка сохраненного расчета из базы данных
                selected_calc = NOx_fuel_save.objects.get(id=calculation_id)
                form_data = {
                    'name': selected_calc.name,
                    'T_ad': selected_calc.T_ad,
                    'psi_ZAG': selected_calc.psi_ZAG,
                    'a_T': selected_calc.a_T,
                    'b_T': selected_calc.b_T,
                    'h_ZAG': selected_calc.h_ZAG,
                    'Bp': selected_calc.Bp,
                    'Vr_Rg': selected_calc.Vr_Rg,
                    'xi': selected_calc.xi,
                    'q_ZAG': selected_calc.q_ZAG,
                    'fuel_type': selected_calc.fuel_type,
                    'Kg': selected_calc.Kg,
                    'alpha_ZAG': selected_calc.alpha_ZAG,
                    'Nr': selected_calc.Nr,
                    'Vr': selected_calc.Vr,
                    'Vsg0': selected_calc.Vsg0,
                    'Vv0': selected_calc.Vv0,
                    'R': selected_calc.R,
                    'Vg': selected_calc.Vg,
                    'Kp': selected_calc.Kp,
                    'concentration': selected_calc.concentration,
                    'standard_concentration': selected_calc.standard_concentration,
                    'emission_power': selected_calc.emission_power,
                    'flag':1
                }

    return render(request, 'NOx_fuel.html', {'form_data': form_data, 'saved_calculations': saved_calculations})


def SOx(request):
    form_data = {}
    saved_calculations = SOx_save.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if not 'load' in request.POST:
            form_data = {
                'B': float(request.POST.get('B', '')),
                'S_r': float(request.POST.get('S_r', '')),
                'n1_SO2': float(request.POST.get('n1_SO2', '')),
                'n2_SO2': float(request.POST.get('n2_SO2', '')),
                'itog': 0,
                'name': request.POST.get('name', '')
            }
            form_data['itog'] = 0.02 * form_data['B'] * form_data['S_r'] * (1 - form_data['n1_SO2']) * (1 - form_data['n2_SO2']) * 1000

            if 'save' in request.POST:
                article = SOx_save(
                    name=form_data['name'],
                    B=form_data['B'],
                    S_r=form_data['S_r'],
                    n1_SO2=form_data['n1_SO2'],
                    n2_SO2=form_data['n2_SO2'],
                    itog=form_data['itog'])
                article.save()

            elif 'download' in request.POST:
                content = (
                    "=== Расчет выбросов SOx ===\n"
                    "\n"
                    f"Название: {form_data['name']}\n"
                    f"Расход топлива (B): {form_data['B']}\n"
                    f"Содержание серы (S_r): {form_data['S_r']}\n"
                    f"Степень очистки 1 (η1_SO2): {form_data['n1_SO2']}\n"
                    f"Степень очистки 2 (η2_SO2): {form_data['n2_SO2']}\n"
                    f"Итоговый выброс (г/с): {form_data['itog']:.2f}\n"
                    "\n"
                    "===========================\n"
                )
                response = HttpResponse(
                    content_type='application/text',
                    headers={'Content-Disposition': 'attachment; filename="SOx_calculation.txt"'}
                )
                response.write(content.encode('utf-8'))
                return response
            elif 'upload' in request.POST:
                print("хуй")


        elif 'load' in request.POST:
            calculation_id = request.POST.get('calculation_id')
            if calculation_id:
                # Получаем объект из базы данных
                selected_calc = SOx_save.objects.get(id=calculation_id)
                form_data = {
                    'B': selected_calc.B,
                    'S_r': selected_calc.S_r,
                    'n1_SO2': selected_calc.n1_SO2,
                    'n2_SO2': selected_calc.n2_SO2,
                    'itog': selected_calc.itog,
                    'name': selected_calc.name
                }

    return render(request, 'SOx.html', {'form_data': form_data, 'saved_calculations': saved_calculations})


def home(request):
    return render(request, 'home.html')