import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Dart Throw Generation ---
def generate_throws(dart_set, num_throws):
    center = (0, 0) 
    if dart_set == 'A - High Bias/High Variance':
        radius = 3  # Large spread
        offset = (np.random.rand() - 0.5, np.random.rand() - 0.5)  # Random offset
    elif dart_set == 'B - Low Bias/High Variance':
        radius = 1  # Smaller spread
        offset = (0.5, 0)  # Offset to the right
    elif dart_set == 'C - High Bias/Low Variance':
        radius = 0.5 # Small spread
        offset = (0.5, 0.5) # Fixed offset
    else:  # 'D - High Bias/High Variance'
        radius = 2 
        offset = (0.5, -0.5) 

    angles = np.linspace(0, 2*np.pi, num_throws, endpoint=False)
    x = radius * np.cos(angles) + offset[0] + np.random.randn(num_throws) * 0.4 
    y = radius * np.sin(angles) + offset[1] + np.random.randn(num_throws) * 0.4
    return x, y

# --- Dartboard Visualization ---
def create_dartboard_plot():
    fig, ax = plt.subplots()
    for radius in [1, 2, 3]:
        circle = plt.Circle((0, 0), radius, color='lightgray')
        ax.add_patch(circle)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_title('Dartboard')
    return fig, ax
    
def update_plot(dart_x, dart_y):
    dartboard_fig, dartboard_ax = create_dartboard_plot() 
    dartboard_ax.scatter(dart_x, dart_y, color='red')
    return dartboard_fig

# --- Error vs. Complexity Graph ---
def generate_error_complexity_graph():
    model_complexity = np.arange(1, 11)  
    error = np.exp(-model_complexity) + np.random.randn(10) * 0.2  
    fig, ax = plt.subplots()
    ax.plot(model_complexity, error)
    ax.set_xlabel('Model Complexity')
    ax.set_ylabel('Error')
    ax.set_title('Error vs. Model Complexity')
    return fig

# --- Streamlit App Structure ---
st.title("Variance-Bias Tradeoff: Dart Game Simulator")
st.sidebar.header("Dart Set Selection")
dart_set = st.sidebar.selectbox("Select Dart Set:", options=[
                                    'A - High Bias/High Variance', 
                                    'B - Low Bias/High Variance',
                                    'C - High Bias/Low Variance', 
                                    'D - Low Bias/Low Variance'])

num_throws = st.sidebar.slider("Number of Throws", 5, 100, 50)

# Dart Simulation & Visualization
dart_x, dart_y = generate_throws(dart_set, num_throws)
dartboard_fig = update_plot(dart_x, dart_y)
st.pyplot(dartboard_fig)

# Text Explainers - During Simulation
if dart_set in ['A - High Bias/High Variance', 'C - High Bias/Low Variance']:
    st.write("This dart set has high bias. Imagine a dart player who consistently aims far from the center. Even though some throws might hit the bullseye by chance, most will miss the target by a large margin. This translates to a model that consistently makes inaccurate predictions.")
elif dart_set in ['B - Low Bias/High Variance', 'D - Low Bias/Low Variance']:
    st.write("This dart set has low bias. The throws are generally centered around the bullseye. However, there's still variance (spread) in the throws. Imagine a player who aims well but has shaky hands, leading to some throws landing further away from the center. This translates to a model that makes accurate predictions on average, but the specific predictions can vary for the same input.")

# --- Advanced Discussion ---
st.header("Finding the Balance & Regularization")
st.write("In machine learning, models also face a bias-variance tradeoff. Bias refers to the model's tendency to underfit the training data, leading to consistently inaccurate predictions across the board. Variance refers to the model's sensitivity to small fluctuations in the training data, resulting in inconsistent predictions for the same input.")
st.write("The ideal scenario (sweet spot) is a model with low bias (accurate) and low variance (consistent).")
st.write("Regularization techniques (like L1/L2) can help reduce variance by adding a penalty for model complexity. Imagine a dart player who wears weighted wristbands to reduce shakiness, leading to more consistent throws. Regularization penalizes overly complex models, making them less sensitive to specific features in the training data and promoting better generalization.")
st.pyplot(generate_error_complexity_graph())
