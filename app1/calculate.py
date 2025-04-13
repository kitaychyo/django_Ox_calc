import math


def calculate_nox_coal_boiler(params):
    """
    Расчет выбросов NOx для пылеугольного котла
    params: словарь с параметрами котла
    Возвращает: удельные выбросы (г/МДж), концентрацию (г/м3), мощность выброса (г/с)
    """
    try:
        # Расчет топливных оксидов азота
        C_SV = 100 - params['Wr'] - params['Ar'] - params['Vr']
        FR = C_SV / params['Vr']
        xi_NOx = FR ** 0.6 + (1 + params['Nd'])

        if params['burner_type'] == 'вихревые':
            beta_alpha_g = (0.35 * params['alpha_g'] + 0.4) ** 2
            beta_mix = 0.4 * (params['w2_w1']) ** 2 + 0.32

        else:  # прямоточные
            beta_alpha_g = (0.53 * params['alpha_g'] + 0.12) ** 2
            beta_mix = 0.98 * params['w2_w1'] - 0.47

        beta_alpha_1 = 1.73 * params['alpha_1'] + 0.48
        beta_R = 1 - 0.016 * math.sqrt(params['R'])
        beta_theta = 0.11 * (params['T_zag'] - 1100) ** (1 / 3)

        K_NO2_topl = 0.12 * xi_NOx * beta_alpha_g * beta_alpha_1 * beta_R * beta_theta * beta_mix

        # Расчет воздушных оксидов азота
        alpha_ZAG = params['alpha_g'] + 0.5 * params['delta_alpha_T']
        K_NO2_vzd = (1.54e16 / math.sqrt(params['T_zag'])) * \
                    math.sqrt((alpha_ZAG - 1) / alpha_ZAG) * \
                    math.exp(-67000 / params['T_zag'])

        # Суммарный удельный выброс
        K_NO2 = K_NO2_topl + K_NO2_vzd

        # Концентрация NOx в сухих дымовых газах
        V_sg = params['Vr0'] + (1.4 - 1) * params['Vv0'] - params['V_H2O0']
        if params['extra_fuel'] == 'газ':
            A = 1 - (params['delta']/2.5)**0.5
        elif params['extra_fuel'] == 'мазут':
            A = 1 - (params['delta'] / 1.65) ** 0.5
        else: A = 1

        C_NO2 = A * K_NO2 * params['Qi_r'] / V_sg

        # Мощность выброса
        M_NOx = C_NO2 * params['Vg'] * params['Bp'] * params['Kp']
        if type(K_NO2) is complex: f = 0
        elif K_NO2 < 0: f = 0
        else: f = 1

        return {
            'specific_emissions': K_NO2,
            'concentration': C_NO2,
            'emission_power': M_NOx,
            'flag':f
        }

    except Exception as e:
        return {'error': str(e)}


def calculate_nox_gas_oil_boiler(params):
    """
    Расчет выбросов NOx для газового/мазутного котла
    params: словарь с параметрами котла
    Возвращает: концентрацию (г/м3), мощность выброса (г/с)
    """
    try:
        # Среднеинтегральная температура
        T_ZAG_avg = params['T_ad'] * (1 - params['psi_ZAG']) ** 0.25

        # Время пребывания в ЗАГ
        tau_ZAG = (params['a_T'] * params['b_T'] * params['h_ZAG']) / \
                  (params['Bp'] * params['Vr_Rg'] * (T_ZAG_avg / 273)) * \
                  params['xi']

        # Отраженный тепловой поток
        q_ZAG_otr = params['q_ZAG'] * (1 - params['psi_ZAG'])

        if params['fuel_type'] == 'газ':
            # Расчет для газа
            NO2 = 2.05e-3 * params['Kg'] * \
                  (26.0 * math.exp(0.26 * (T_ZAG_avg - 1700) / 100) - 4.7) * \
                  (math.exp(q_ZAG_otr) - 1) * \
                  (13.0 - 79.8 * (params['alpha_ZAG'] - 1.07) ** 4 +
                   18.1 * (params['alpha_ZAG'] - 1.07) ** 3 +
                   59.4 * (params['alpha_ZAG'] - 1.07) ** 2 +
                   9.6 * (params['alpha_ZAG'] - 1.07)) * \
                  tau_ZAG
        else:
            # Расчет для мазута
            delta_NO2_topl = 650 * (params['Nr'] - 0.3) / params['Vr'] if params['Nr'] > 0.3 else 0

            NO2 = 2.05e-3 * params['Kg'] * \
                  ((24.3 * math.exp(0.19 * (T_ZAG_avg - 1650) / 100) - 12.3) * \
                   (math.exp(q_ZAG_otr) - 1) * \
                   (15.1 - 131.7 * (params['alpha_ZAG'] - 1.09) ** 4 +
                    72.3 * (params['alpha_ZAG'] - 1.09) ** 3 +
                    73.0 * (params['alpha_ZAG'] - 1.09) ** 2 +
                    2.8 * (params['alpha_ZAG'] - 1.09)) * \
                   tau_ZAG + delta_NO2_topl)

        # Пересчет на стандартные условия
        NO2_std = NO2 * params['Vr_Rg'] / \
                  ((params['Vsg0'] + (1.4 - 1) * params['Vv0']) * (1 + params['R']))

        # Мощность выброса
        M_NOx = NO2_std * params['Vg'] * params['Bp'] * params['Kp']

        if type(NO2) is complex:f = 0
        elif NO2 < 0: f = 0
        else: f = 1

        return {
            'concentration': NO2,
            'standard_concentration': NO2_std,
            'emission_power': M_NOx,
            'flag':f
        }

    except Exception as e:
        return {'error': str(e)}


# Пример использования для пылеугольного котла
coal_params = {
    'Wr': 10.0,  # Влажность, %
    'Ar': 19.8,  # Зольность, %
    'Vr': 14.0,  # Выход летучих, %
    'Nd': 0.6,  # Содержание азота в сухой массе, %
    'alpha_g': 1.1,  # Коэффициент избытка воздуха в горелках
    'alpha_1': 0.3,  # Доля первичного воздуха
    'R': 0.0,  # Степень рециркуляции, %
    'T_zag': 1821,  # Температура на выходе из ЗАГ, К
    'w2_w1': 1.4,  # Соотношение скоростей в горелках
    'delta_alpha_T': 0.02,  # Присосы в топку, %
    'Vr0': 6.39,  # Теоретический объем газов, м3/кг
    'Vv0': 5.95,  # Теоретический объем воздуха, м3/кг
    'V_H2O0': 0.56,  # Объем водяных паров, м3/кг
    'Qi_r': 22.48,  # Теплота сгорания, МДж/кг
    'Vg': 14,  # Объем дымовых газов, м3/кг
    'Bp': 115,  # Расчетный расход топлива, м3/с
    'Kp': 0.00278,  # Коэффициент пересчета
    'burner_type': 'вихревые'  # Тип горелок
}

result = calculate_nox_coal_boiler(coal_params)

params = {
    'T_ad': 2270,               # Ожидаемая адиабатная температура, К
    'psi_ZAG': 0.432,       # Коэффициент отражения теплового потока (1 - тепловая эффективность)
    'a_T': 20.66,               # Ширина топки в свету, м
    'b_T': 10.26,               # Глубина топки в свету, м
    'h_ZAG': 11.04,             # Высота зоны активного горения, м
    'Bp': 55.9,                 # Расход топлива, м3/с
    'Vr_Rg': 11.915,            # Объем продуктов сгорания, м3/м3
    'xi': 0.8,                  # Коэффициент заполнения топочной камеры
    'q_ZAG': 2.014 ,            # Тепловая нагрузка зоны активного горения, перевели МВт/м2 -> Вт/м2
    'fuel_type': 'газ',         # Тип топлива: газ
    'Kg': 1,                    # Коэффициент конструкции горелочного устройства
    'alpha_ZAG': 1.07,          # Коэффициент избытка воздуха в горелках
    'Nr': 1.8 / 100,            # Содержание азота, перевели в долю
    'Vr': 11.915,               # Объем продуктов сгорания, м3/м3
    'Vsg0': 8.53,               # Теоретический объем сухих газов, м3/м3
    'Vv0': 9.52,                # Теоретический объем воздуха для полного сжигания топлива, м3/м3
    'R': 0.05,                  # Доля газов рециркуляции
    'Vg': 8.53,                 # Объем дымовых газов, м3/м3
    'Kp': 1                     # Коэффициент конструкции горелочного устройства (как поправочный)
}

result_fuel = calculate_nox_gas_oil_boiler(params)

print(result_fuel)
print("Результаты для пылеугольного котла:")
print(f"Удельные выбросы: {result_fuel['standard_concentration']:.3f} г/МДж")
print(f"Концентрация NOx: {result_fuel['concentration']:.3f} г/м3")
print(f"Мощность выброса: {result_fuel['emission_power']:.3f} г/с")