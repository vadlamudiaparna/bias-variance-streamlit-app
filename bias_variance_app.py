import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# --- Dart Throw Generation ---
# --- Dart Throw Generation ---
def generate_throws(dart_set, num_throws):
    if dart_set == 'A - High Bias/High Variance':
        # High Bias/High Variance: Random throws with bias towards outer circles
        radius = np.random.uniform(1.1, 1.8, num_throws)  # Random radius between 1.3 and 2
        angle = np.random.uniform(0, 2*np.pi, num_throws)  # Random angle
        dart_x = radius * np.cos(angle)
        dart_y = radius * np.sin(angle)
    elif dart_set == 'B - Low Bias/High Variance':
        # Low Bias/High Variance: Clustered throws with spread
        center = (0.1, 0.1)  # Adjusted center point closer to the bullseye
        radius = np.random.uniform(0.5, 1.0, num_throws)  # Adjusted radius range
        angle = np.random.uniform(0, 2*np.pi, num_throws)  # Random angle
        dart_x = radius * np.cos(angle) + center[0]
        dart_y = radius * np.sin(angle) + center[1]
    elif dart_set == 'C - High Bias/Low Variance':
        # High Bias/Low Variance: Clustered throws without spread
        center = (0.5, 0.5)
        dart_x = np.random.normal(center[0], 0.1, num_throws)
        dart_y = np.random.normal(center[1], 0.1, num_throws)
    else:  # 'D - Low Bias/Low Variance'
        # Low Bias/Low Variance: Clustered throws around bullseye
        dart_x = np.random.normal(0, 0.1, num_throws)
        dart_y = np.random.normal(0, 0.1, num_throws)
    return dart_x, dart_y


# --- Dartboard Visualization ---
def create_dartboard_plot():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim([-3, 3])  # Fixing x-axis limit
    ax.set_ylim([-3, 3])  # Fixing y-axis limit
    
    # Draw circles representing dartboard rings
    circle_colors = ['lightblue', 'skyblue', 'royalblue', 'purple']
    circle_radii = [1.8, 1.3, 0.8, 0.3]  # reversed order
    for color, radius in zip(circle_colors, circle_radii):
        circle = patches.Circle((0, 0), radius, color=color, fill=True)
        ax.add_patch(circle)
        
    ax.set_title('Dartboard')
    return fig

def update_plot(dart_x, dart_y):
    dartboard_fig = create_dartboard_plot() 
    plt.scatter(dart_x, dart_y, color='yellow', edgecolor='black', alpha=0.8)
    return dartboard_fig

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

# Scenario-Specific Explanations
st.header("Scenario Analysis") 
if dart_set == 'A - High Bias/High Variance':
    st.write("**Scenario Analysis:** This represents a **severely underfit** model with **high bias** (consistently inaccurate) and **high variance** (inconsistent predictions). Think of a dart player who throws wildly, rarely hitting the target.")
elif dart_set == 'B - Low Bias/High Variance':
    st.write("**Scenario Analysis:** This represents a **potentially overfit** model with **low bias** (generally accurate) but **high variance** (inconsistent predictions). Think of a player who aims well but has unsteady hands, leading to scattered throws around the target.")
elif dart_set == 'C - High Bias/Low Variance':
    st.write("**Scenario Analysis:** This represents an **underfit** model with **high bias** (consistently inaccurate) and **low variance** (consistently but wrongly predicted results). Think of a player who consistently aims at the wrong spot with precision.")
else:  # 'D - Low Bias/Low Variance'
    st.write("**Scenario Analysis:**  This represents the **ideal** model with **low bias** (consistently accurate) and **low variance** (consistent and reliable predictions). Think of a highly skilled player who consistently hits the bullseye.")
