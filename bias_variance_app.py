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

# Text Explainers - During Simulation
if dart_set == 'A - High Bias/High Variance':
    st.write("This dart set represents high bias and high variance. The dart throws are widely scattered and consistently far from the bullseye. In machine learning, this scenario signifies a model that is uncertain and inaccurate on average.")
elif dart_set == 'B - Low Bias/High Variance':
    st.write("This dart set represents low bias and high variance. The dart throws are clustered around a specific area but are spread out. In machine learning, this scenario signifies a model that is consistent but inaccurate.")
elif dart_set == 'C - High Bias/Low Variance':
    st.write("This dart set represents high bias and low variance. The dart throws are tightly clustered but consistently miss the bullseye. In machine learning, this scenario signifies a model that is uncertain but accurate.")
else:  # 'D - Low Bias/Low Variance'
    st.write("This dart set represents low bias and low variance. The dart throws are tightly clustered around the bullseye. In machine learning, this scenario signifies a model that is consistent and accurate (IDEAL).")
