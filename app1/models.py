from django.db import models

class SOx_save(models.Model):
    name = models.CharField(
        max_length=100,
        default='Unnamed Calculation',
        verbose_name='Название расчета'
    )
    B = models.FloatField(verbose_name='Параметр B')
    S_r = models.FloatField(verbose_name='Параметр S_r')
    n1_SO2 = models.FloatField(verbose_name='Коэффициент n1 SO2')
    n2_SO2 = models.FloatField(verbose_name='Коэффициент n2 SO2')
    itog = models.FloatField(verbose_name='Итоговый результат')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Расчет SOx'
        verbose_name_plural = 'Расчеты SOx'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.created_at})"

class NOx_save(models.Model):
    name = models.CharField(max_length=100, blank=True)
    Wr = models.FloatField()
    Ar = models.FloatField()
    Vr = models.FloatField()
    Nd = models.FloatField()
    alpha_g = models.FloatField()
    alpha_1 = models.FloatField()
    R = models.FloatField()
    T_zag = models.FloatField()
    w2_w1 = models.FloatField()
    delta_alpha_T = models.FloatField()
    Vr0 = models.FloatField()
    Vv0 = models.FloatField()
    V_H2O0 = models.FloatField()
    Qi_r = models.FloatField()
    Vg = models.FloatField()
    Bp = models.FloatField()
    Kp = models.FloatField()
    burner_type = models.CharField(max_length=50)
    extra_fuel = models.CharField(max_length=50)
    delta = models.FloatField()
    itog = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"NOx Calculation {self.id}"

class NOx_fuel_save(models.Model):
    name = models.CharField(max_length=100, blank=True)
    T_ad = models.FloatField()  # Адиабатная температура, К
    psi_ZAG = models.FloatField()  # Коэффициент отражения теплового потока
    a_T = models.FloatField()  # Ширина топки, м
    b_T = models.FloatField()  # Глубина топки, м
    h_ZAG = models.FloatField()  # Высота зоны горения, м
    Bp = models.FloatField()  # Расход топлива, м3/с
    Vr_Rg = models.FloatField()  # Объем продуктов сгорания, м3/м3
    xi = models.FloatField()  # Коэффициент заполнения
    q_ZAG = models.FloatField()  # Тепловая нагрузка, Вт/м2
    fuel_type = models.CharField(max_length=50)  # Тип топлива
    Kg = models.FloatField()  # Коэффициент горелки
    alpha_ZAG = models.FloatField()  # Коэффициент избытка воздуха
    Nr = models.FloatField()  # Содержание азота
    Vr = models.FloatField()  # Объем продуктов сгорания, м3/м3
    Vsg0 = models.FloatField()  # Объем сухих газов, м3/м3
    Vv0 = models.FloatField()  # Объем воздуха, м3/м3
    R = models.FloatField()  # Доля рециркуляции
    Vg = models.FloatField()  # Объем дымовых газов, м3/м3
    Kp = models.FloatField()  # Поправочный коэффициент
    itog = models.FloatField()  # Итоговый выброс, г/с
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"NOx Fuel Calculation {self.id}"