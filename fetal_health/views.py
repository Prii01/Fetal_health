from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from fetal_health.models import *  # Import the FetalHealthInput model
from fetal_health.forms import *
from django.http import JsonResponse
import numpy as np
import joblib


# Load the trained machine learning model
model = joblib.load(r"model\fetal_health\fetal.pkl")

# Import necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from .models import FetalHealthInput

# Define function to train the model
def train_histogram_model():
    # Load dataset
    dataset = FetalHealthInput.objects.all()  # Assuming FetalHealthInput is your model

    # Prepare input features and target values
    X = dataset[['baseline_value', 'accelerations', 'fetal_movement', 'uterine_contractions',
                 'light_decelerations', 'severe_decelerations', 'prolongued_decelerations',
                 'abnormal_short_term_variability', 'mean_value_of_short_term_variability',
                 'percentage_of_time_with_abnormal_long_term_variability', 'mean_value_of_long_term_variability']].values
    y = dataset[['histogram_width', 'histogram_min', 'histogram_max', 'histogram_number_of_peaks',
                 'histogram_number_of_zeroes', 'histogram_mode', 'histogram_mean', 'histogram_median',
                 'histogram_variance', 'histogram_tendency']].values

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor()  # You can use any regression algorithm here
    model.fit(X_train, y_train)

    # Evaluate the model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"Training Score: {train_score}")
    print(f"Testing Score: {test_score}")

    return model

# Define function to predict histogram values
def predict_histogram_values(input_features):
    # Load trained model
    model = train_histogram_model()

    # Convert input features to numpy array
    input_features = np.array([input_features])

    # Predict histogram values
    histogram_values = model.predict(input_features)

    return histogram_values


def predict_fetal_healthmod(request):
    if request.method == 'POST':
        # Extract input values from the POST request
        baseline_fhr = float(request.POST.get('Baseline_FHR'))
        accelerations = float(request.POST.get('Number_of_accelerations_per_second'))
        fetal_movement = float(request.POST.get('Number_of_fetal_movements_per_second'))
        uterine_contractions = float(request.POST.get('Number_of_uterine_contractions_per_second'))
        light_decelerations = float(request.POST.get('Number_of_LD_per_second'))
        severe_decelerations = float(request.POST.get('Number_of_SD_per_second'))
        prolonged_decelerations = float(request.POST.get('Number_of_PD_per_second'))
        abnormal_short_term_variability = float(request.POST.get('Percentage_of_time_with_abnormal_short_term_variability'))
        mean_value_of_short_term_variability = float(request.POST.get('Mean_value_of_short_term_variability'))
        percentage_of_time_with_abnormal_long_term_variability = float(request.POST.get('Percentage_of_time_with_abnormal_long_term_variability'))
        mean_value_of_long_term_variability = float(request.POST.get('Mean_value_of_long_term_variability'))
        histogram_width = float(request.POST.get('Width_of_the_histogram'))
        histogram_min = float(request.POST.get('Histogram_minimum_value'))
        histogram_max = float(request.POST.get('Histogram_maximum_value'))
        histogram_number_of_peaks = float(request.POST.get('Number_of_peaks_in_histogram'))
        histogram_number_of_zeroes = float(request.POST.get('Number_of_zeroes_in_histogram'))
        histogram_mode = float(request.POST.get('Hist_mode'))
        histogram_mean = float(request.POST.get('Hist_mean'))
        histogram_median = float(request.POST.get('Hist_Median'))
        histogram_variance = float(request.POST.get('Hist_variance'))
        histogram_tendency = float(request.POST.get('Histogram_trend'))

        # Convert input values into a numpy array
        input_data = np.array([[
            baseline_fhr, accelerations, fetal_movement, uterine_contractions,
            light_decelerations, severe_decelerations, prolonged_decelerations,
            abnormal_short_term_variability, mean_value_of_short_term_variability,
            percentage_of_time_with_abnormal_long_term_variability, mean_value_of_long_term_variability,
            histogram_width, histogram_min, histogram_max,
            histogram_number_of_peaks, histogram_number_of_zeroes,
            histogram_mode, histogram_mean, histogram_median,
            histogram_variance, histogram_tendency
        ]])

        # Make predictions using the loaded model
        fetal_health_prediction = model.predict(input_data)[0]
        
        # Define the fetal health labels
        fetal_health_labels = {1: "Normal", 2: "Suspect", 3: "Pathological"}
        fetal_health = fetal_health_labels[fetal_health_prediction]

        # Determine the type of delivery based on fetal health
        delivery_type = "Normal" if fetal_health_prediction == 1 else "Caesarean"

        # Return the prediction results as JSON response
        return JsonResponse({
            'fetal_health': fetal_health,
            'delivery_type': delivery_type
        })

    else:
        return JsonResponse({'error': 'Invalid request method. Please use POST.'})
@login_required
def predict_fetal_health(request):
    if request.method == 'POST':
        form = FetalHealthDataForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            fetal_health_data = form.save(commit=False)
            fetal_health_data.user = request.user
            
            # Get input values
            input_values = form.cleaned_data
            
            # Predict fetal health and delivery type
            fetal_health, delivery_type = predict_fetal_health_function(input_values)
            
            # Assign predicted values
            fetal_health_data.fetal_health = fetal_health
            fetal_health_data.delivery_type = delivery_type
            
            # Save the complete data to the database
            fetal_health_data.save()
            
            # Retrieve the logged-in user's data
            current_user = request.user
            
            # Determine recommendation based on delivery type
            if delivery_type == 'Normal':
                recommendation = "Recommendation for normal delivery: Consult a doctor and follow their advice. Eat a balanced diet and avoid strenuous activities."
            elif delivery_type == 'Cesarean':
                recommendation = "Recommendation for cesarean delivery: Consult a doctor and prepare for the surgical procedure. Follow their advice for pre and post-operative care."
            else:
                recommendation = "Recommendation not available."

            if fetal_health == 1:
                fetal_health_val = "Normal"
            elif fetal_health == 2:
                fetal_health_val = "Suspect"
            else:
                fetal_health_val = "Pathological"

            result_list = [
                {"Fetal Health": fetal_health_val},
                {"Delivery Type": delivery_type}
                # {"Recommendation": recommendation}
            ]

            return render(request, 'resultf.html', {'result_list': result_list, 'recommendation': recommendation,'input_values': input_values})
    else:
        form = FetalHealthDataForm()
    return render(request, 'fetal_health_form.html', {'form': form})


@login_required
def view_fetal_health_data(request):
    # Retrieve the logged-in user
    current_user = request.user

    # Retrieve fetal health data associated with the logged-in user
    fetal_health_data = FetalHealthInput.objects.filter(user=current_user)

    return render(request, 'fetal_health_data.html', {'fetal_health_data': fetal_health_data})


def predict_fetal_health_function(input_values):
    # Extract input values
    baseline_value = input_values['baseline_value']
    accelerations = input_values['accelerations']
    fetal_movement = input_values['fetal_movement']
    uterine_contractions = input_values['uterine_contractions']
    light_decelerations = input_values['light_decelerations']
    severe_decelerations = input_values['severe_decelerations']
    prolongued_decelerations = input_values['prolongued_decelerations']
    abnormal_short_term_variability = input_values['abnormal_short_term_variability']
    mean_value_of_short_term_variability = input_values['mean_value_of_short_term_variability']
    percentage_of_time_with_abnormal_long_term_variability = input_values['percentage_of_time_with_abnormal_long_term_variability']
    mean_value_of_long_term_variability = input_values['mean_value_of_long_term_variability']

    # Define thresholds for each feature
    baseline_threshold = 50
    accelerations_threshold = 10
    fetal_movement_threshold = 5
    uterine_contractions_threshold = 10
    light_decelerations_threshold = 5
    severe_decelerations_threshold = 2
    prolongued_decelerations_threshold = 2
    abnormal_short_term_variability_threshold = 10
    mean_value_of_short_term_variability_threshold = 5
    percentage_of_time_with_abnormal_long_term_variability_threshold = 10
    mean_value_of_long_term_variability_threshold = 5

    # Predict fetal health based on input values
    if (baseline_value >= baseline_threshold and
        accelerations >= accelerations_threshold and
        fetal_movement >= fetal_movement_threshold and
        uterine_contractions >= uterine_contractions_threshold and
        light_decelerations >= light_decelerations_threshold and
        severe_decelerations >= severe_decelerations_threshold and
        prolongued_decelerations >= prolongued_decelerations_threshold and
        abnormal_short_term_variability >= abnormal_short_term_variability_threshold and
        mean_value_of_short_term_variability >= mean_value_of_short_term_variability_threshold and
        percentage_of_time_with_abnormal_long_term_variability >= percentage_of_time_with_abnormal_long_term_variability_threshold and
        mean_value_of_long_term_variability >= mean_value_of_long_term_variability_threshold):
        fetal_health = 1  # Normal
        delivery_type = 'Normal'
    elif (baseline_value >= baseline_threshold and
          accelerations >= accelerations_threshold and
          fetal_movement >= fetal_movement_threshold and
          uterine_contractions >= uterine_contractions_threshold and
          light_decelerations >= light_decelerations_threshold and
          severe_decelerations >= severe_decelerations_threshold):
        fetal_health = 2  # Suspect
        delivery_type = 'Normal'
    else:
        fetal_health = 3  # Pathological
        delivery_type = 'Cesarean'

    return fetal_health, delivery_type
