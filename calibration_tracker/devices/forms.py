from django import forms
from .models import MeasurementDevice
from devices.constants import UNIT_CHOICES

class MeasurementDeviceForm(forms.ModelForm):
    # Списки единиц измерений
    ELECTRICAL_UNITS = UNIT_CHOICES['electrical']
    PRESSURE_UNITS = UNIT_CHOICES['pressure']
    THERMAL_UNITS = UNIT_CHOICES['thermal']
    LINEAR_UNITS = UNIT_CHOICES['linear_and_angular_dimensions']
    MECHANICAL_UNITS = UNIT_CHOICES['mechanical']
    FLOW_UNITS = UNIT_CHOICES['flow']

    custom_unit = forms.CharField(
        max_length=255,
        required=False,
        label='Единица измерения',
        widget=forms.TextInput(attrs={'placeholder': 'Введите единицу измерения'})
    )

    class Meta:
        model = MeasurementDevice
        fields = '__all__'
        widgets = {
            'last_calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'next_calibration_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'measure_range': forms.TextInput(attrs={'placeholder': 'Например: 0–100'})
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        measure_type = kwargs.get('initial', {}).get('measure_type')
        if not measure_type and self.data.get('measure_type'):
            measure_type = self.data.get('measure_type')
        elif self.instance.pk:
            measure_type = self.instance.measure_type

        # Обновляем поле measurement_unit
        self._update_measurement_unit_field(measure_type)

        # Логика для роли пользователя
        if not (hasattr(self.user, 'profile') and self.user.is_authenticated):
            return

        role = self.user.profile.role

        # Только метрологи и админы могут менять ответственного
        if role not in ['metrologist', 'admin'] and not self.user.is_superuser:
            if 'responsible_person' in self.fields:
                self.fields['responsible_person'].disabled = True
                self.fields['responsible_person'].help_text = 'Вы не можете изменить ответственное лицо'

        # Только метрологи и админы выбирать менять подразделение
        if role not in ['metrologist', 'admin'] and not self.user.is_superuser:
            if 'owner_department' in self.fields:
                self.fields['owner_department'].disabled = True
                self.fields['owner_department'].help_text = 'Вы не можете изменить подразделение'

        # Автозаполнение для кладовщика
        if role == 'storekeeper':
            self.fields['responsible_person'].initial = self.user
            self.fields['owner_department'].initial = self.user.profile.department

    def _get_unit_choices(self, measure_type):
        """Возвращает список единиц измерения в зависимости от типа"""
        choices = [('', '---------')]
        if measure_type == 'electrical':
            choices += [(unit, unit) for unit in self.ELECTRICAL_UNITS]
        elif measure_type == 'pressure':
            choices += [(unit, unit) for unit in self.PRESSURE_UNITS]
        elif measure_type == 'thermal':
            choices += [(unit, unit) for unit in self.THERMAL_UNITS]
        elif measure_type == 'linear_and_angular_dimensions':
            choices += [(unit, unit) for unit in self.LINEAR_UNITS]
        elif measure_type == 'mechanical':
            choices += [(unit, unit) for unit in self.MECHANICAL_UNITS]
        elif measure_type == 'flow':
            choices += [(unit, unit) for unit in self.FLOW_UNITS]

        return choices

    def _update_measurement_unit_field(self, measure_type):
        """Обновляет поле measurement_unit в зависимости от measure_type"""

        # Удаляем старое поле
        if 'measurement_unit' in self.fields:
            del self.fields['measurement_unit']

        if measure_type == 'other':
            self.fields['measurement_unit'] = forms.CharField(
                max_length=255,
                required=False,
                label='Единица измерения',
                widget=forms.TextInput(attrs={'placeholder': 'Введите единицу измерения'})
            )
        else:
            choices = self._get_unit_choices(measure_type)
            self.fields['measurement_unit'] = forms.ChoiceField(
                choices=choices,
                required=False,
                label='Единица измерения',
                initial=self.instance.measurement_unit
            )

    def clean(self):
        cleaned_data = super().clean()
        measure_type = cleaned_data.get('measure_type')
        custom_unit = cleaned_data.get('custom_unit')

        if measure_type == 'other' and custom_unit:
            cleaned_data['measurement_unit'] = custom_unit

        return cleaned_data