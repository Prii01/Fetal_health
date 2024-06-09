from django import forms
from fetal_health.models import *

class FetalHealthDataForm(forms.ModelForm):
    class Meta:
        model = FetalHealthInput
        exclude = ['user','fetal_health', 'delivery_type','created_at']
        widgets = {
            'baseline_value': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'accelerations': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'fetal_movement': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'uterine_contractions': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'light_decelerations': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'severe_decelerations': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'prolongued_decelerations': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'abnormal_short_term_variability': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'mean_value_of_short_term_variability': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'percentage_of_time_with_abnormal_long_term_variability': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
            'mean_value_of_long_term_variability': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Adjust max value as needed
        }
        required = '__all__'
