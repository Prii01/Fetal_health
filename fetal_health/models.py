from django.db import models
from django.contrib.auth.models import User

class FetalHealthInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baseline_value = models.IntegerField()
    accelerations = models.IntegerField()
    fetal_movement = models.IntegerField()
    uterine_contractions = models.IntegerField()
    light_decelerations = models.IntegerField()
    severe_decelerations = models.IntegerField()
    prolongued_decelerations = models.IntegerField()
    abnormal_short_term_variability = models.FloatField()
    mean_value_of_short_term_variability = models.FloatField()
    percentage_of_time_with_abnormal_long_term_variability = models.FloatField()
    mean_value_of_long_term_variability = models.FloatField()
    fetal_health = models.IntegerField(choices=((1, 'Normal'), (2, 'Suspect'), (3, 'Pathological')))
    delivery_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
