import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CORE MMET MATHEMATICAL FUNCTIONS
# ==========================================

def visualization_function(n, x):
    """Calculates the Universal Visualization Function: V(n,x) = max(0, min(n,x) - 1)"""
    return max(0, min(n, x) - 1)

def zeta_binding_coefficient(k):
    """Calculates Binding Coefficient using Riemann Zeta: alpha_k = 6 / (pi^2 * k^2)"""
    return 6 / (np.pi**2 * k**2)

def exponential_binding_coefficient(k, k0, lam):
    """Calculates Binding Coefficient using Exponential Decay: alpha_k = e^(-lambda|k-k0|) / Z"""
    # Calculate normalization constant Z (summing up to dimension 100 for accuracy)
    Z = sum(np.exp(-lam * abs(j - k0)) for j in range(1, 101))
    return np.exp(-lam * abs(k - k0)) / Z

def effective_mass(m_total, n, x):
    """Calculates Effective Measured Mass: m_eff = M_total * sum(alpha_k)"""
    v_gate = visualization_function(n, x)
    if v_gate == 0:
        return 0
    # Using the primary Zeta model for the main simulation
    alpha_sum = sum(zeta_binding_coefficient(k) for k in range(1, v_gate + 1))
    return m_total * alpha_sum

# Speed of light dimensional scaling
def get_c_k(k):
    c_3 = 299792458
    y_k = {1: 0.5, 2: 0.8, 3: 1.0, 4: 1.5, 5: 2.0}
    scaling = y_k.get(k, 1.0 + (k-3)*0.5) 
    return scaling * c_3


# ==========================================
# 2. STREAMLIT USER INTERFACE & SIDEBAR
# ==========================================

st.set_page_config(page_title="MMET-EXTENDED Simulation", layout="wide")
st.title("MMET-EXTENDED: Multidimensional Simulation")
st.markdown("Interactive mathematical simulation of the Multidimensional Mass-Energy Theory (MMET) framework.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Core Observation Parameters")
n_obs = st.sidebar.slider("Observer Dimension (n)", min_value=1, max_value=10, value=3)
x_obj = st.sidebar.slider("Object Dimension (x)", min_value=1, max_value=10, value=3)
m_total = st.sidebar.number_input("Total Universal Mass (M_total) in kg", value=100.0)

st.sidebar.markdown("---")
st.sidebar.header("2. Relativistic Parameters")
v_frac = st.sidebar.slider("Velocity (v as fraction of c)", min_value=0.0, max_value=0.999, value=0.0, step=0.01)

st.sidebar.markdown("---")
st.sidebar.header("3. Gravitational Parameters")
r_max = st.sidebar.slider("Max Distance Radius (r)", min_value=10, max_value=100, value=50, step=10)

st.sidebar.markdown("---")
st.sidebar.header("4. Master Equation (Time)")
time_t = st.sidebar.slider("Time Evolution (t)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
decay_lambda = st.sidebar.slider("Decay Constant (\u03BB)", min_value=0.0, max_value=0.1, value=0.02, step=0.005)

st.sidebar.markdown("---")
st.sidebar.header("5. Dynamic Binding Calculator")
k_calc = st.sidebar.number_input("Target Dimension (k) to Calculate", min_value=1, max_value=100, value=12)
calc_model = st.sidebar.selectbox("Binding Model", ["Riemann Zeta", "Exponential Decay"])
k0_val = 3
lam_val = 0.5
if calc_model == "Exponential Decay":
    k0_val = st.sidebar.number_input("Center Dimension (k_0)", value=3)
    lam_val = st.sidebar.number_input("Exponential Decay (\u03BB)", value=0.5, step=0.1)


# ==========================================
# 3. MAIN APP DISPLAY & GRAPHS
# ==========================================

col1, col2 = st.columns(2)

with col1:
    # --- A. Visualization & Effective Mass ---
    st.subheader("A. Dimensional Visualization & Mass")
    v_val = visualization_function(n_obs, x_obj)
    m_eff = effective_mass(m_total, n_obs, x_obj)
    
    st.latex(r"V(n,x) = \max(0, \min(n,x) - 1)")
    st.info(f"**Visualization Gate V({n_obs}, {x_obj}) = {v_val}**")
    st.success(f"**Effective Measured Mass (m_eff) = {m_eff:.4f} kg** (out of {m_total} kg)")

    # --- B. Relativistic Equivalencies ---
    st.subheader("B. Relativistic Mass Dilation")
    if m_eff > 0:
        gamma = 1 / np.sqrt(1 - v_frac**2)
        m_rel = m_eff * gamma
        st.write(f"Lorentz Factor (\u03B3) = **{gamma:.4f}** | Relativistic Mass = **{m_rel:.4f} kg**")
        
        v_vals = np.linspace(0, 0.99, 100)
        m_rel_vals = m_eff * (1 / np.sqrt(1 - v_vals**2))
        fig_rel = px.line(x=v_vals, y=m_rel_vals, labels={'x': 'Velocity (v/c)', 'y': 'Relativistic Mass (kg)'})
        fig_rel.update_traces(line_color='red')
        st.plotly_chart(fig_rel, use_container_width=True)
    else:
        st.warning("Effective mass is 0. No relativistic effects visible.")

with col2:
    # --- C. Dynamic Binding Coefficient Calculator ---
    st.subheader("C. Binding Coefficient Calculator")
    if calc_model == "Riemann Zeta":
        st.latex(r"\alpha_k = \frac{6}{\pi^2 k^2}")
        alpha_val = zeta_binding_coefficient(k_calc)
    else:
        st.latex(r"\alpha_k = \frac{e^{-\lambda|k-k_0|}}{Z}")
        alpha_val = exponential_binding_coefficient(k_calc, k0_val, lam_val)
        
    st.info(f"Using **{calc_model}** for Dimension **k = {k_calc}**")
    st.success(f"Binding Coefficient (\u03B1_{k_calc}) = **{alpha_val:.6f}** ( **{alpha_val*100:.4f}%** of total mass)")

  # --- D. Cosmological Distribution & Dark Energy ---
    st.subheader("D. Mass-Energy Cosmological Distribution")
    st.markdown("Mass bound to dimensions **k \u2265 6** distributes across higher-order geometries. Because intersection with the 3D matrix is sparse, it acts as expansive boundary tension, manifesting as Dark Energy.")
    
    # Calculate exact fractions based on the Riemann Zeta function
    a1 = zeta_binding_coefficient(1)
    a2 = zeta_binding_coefficient(2)
    a3 = zeta_binding_coefficient(3)
    a4 = zeta_binding_coefficient(4)
    a5 = zeta_binding_coefficient(5)
    
    # Dark Energy is the infinite sum from k=6 to infinity.
    # Since total mass = 1, we subtract the sum of k=1 through 5.
    a_dark_energy = 1.0 - (a1 + a2 + a3 + a4 + a5)
    
    # Create the data for the chart
    k_labels = [
        "Quantum (k=1)", 
        "EM/Weak (k=2)", 
        "Baryonic (k=3)", 
        "Dark Matter (k=4)", 
        "Dark Matter (k=5)", 
        "Dark Energy (k \u2265 6)"
    ]
    alpha_values = [a1, a2, a3, a4, a5, a_dark_energy]
    
    df_dist = pd.DataFrame({
        "Cosmological Designation": k_labels, 
        "\u03B1_k Fraction": alpha_values,
        "Percentage": [f"{val*100:.2f}%" for val in alpha_values]
    })
    
    # Generate an interactive bar chart with percentage text on the bars
    fig_bar = px.bar(
        df_dist, 
        x="Cosmological Designation", 
        y="\u03B1_k Fraction", 
        color="Cosmological Designation",
        text="Percentage",
        title="MMET Cosmological Mass-Energy Distribution"
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(showlegend=False, yaxis_title="Binding Coefficient (\u03B1_k)")
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Explicit Dark Energy Calculation Callout
    st.success(f"**Dark Energy (\u03B1_{{k \u2265 6}}):** 100% - Sum(k=1 to 5) = **{a_dark_energy*100:.2f}%**")


# --- E. Gravitational Anomalies (Dark Matter) ---
st.markdown("---")
st.subheader("E. Gravitational Field Anomalies (Dark Matter Mapping)")
r_vals = np.linspace(1, r_max, 100)
G_sim = 6.67430e-11
m_3 = m_total * zeta_binding_coefficient(3)
m_dm = m_total * (zeta_binding_coefficient(4) + zeta_binding_coefficient(5))

fig_grav = go.Figure()
fig_grav.add_trace(go.Scatter(x=r_vals, y=(G_sim * m_3)/r_vals**2, name='Baryonic (k=3)', line=dict(dash='dash')))
fig_grav.add_trace(go.Scatter(x=r_vals, y=(G_sim * m_dm)/r_vals**2, name='Dark Matter (k=4, 5)', line=dict(dash='dot')))
fig_grav.add_trace(go.Scatter(x=r_vals, y=(G_sim * (m_3 + m_dm))/r_vals**2, name='Total Effective Gravity'))
fig_grav.update_layout(xaxis_title="Distance (r)", yaxis_title="Gravitational Acceleration (g)")
st.plotly_chart(fig_grav, use_container_width=True)


# --- F. Master Equation & Arrow of Time ---
st.markdown("---")
st.subheader("F. The Master Equation & Thermodynamic Arrow of Time")
st.latex(r"\Psi_{obs}(n,x)=V(n,x)\cdot\sum_{k=1}^{\infty}[\alpha_{k}M_{ref}c_{k}^{2}\cdot e^{-\lambda_{k}(t)}\cdot \max(0,\min(n,k)-1)]+\int\frac{d\alpha_{k}}{d\tau}d\tau")

t_array = np.linspace(0, 100, 200)
a3_init = zeta_binding_coefficient(3)
a4_init = zeta_binding_coefficient(4)
a3_t = a3_init * np.exp(-decay_lambda * t_array)
a4_t = a4_init + a3_init * (1 - np.exp(-decay_lambda * t_array))

fig_time = go.Figure()
fig_time.add_trace(go.Scatter(x=t_array, y=a3_t, name='Observable 3D Binding (\u03B1_3)'))
fig_time.add_trace(go.Scatter(x=t_array, y=a4_t, name='Cascade to Dark Matter (\u03B1_4)'))
fig_time.update_layout(title="Thermodynamic Cascade (Entropy)", xaxis_title="Time (\u03C4)", yaxis_title="Binding Magnitude (\u03B1)")
st.plotly_chart(fig_time, use_container_width=True)

# Instantaneous Master Equation Calculation
psi_obs = 0
for k in range(1, 11): 
    filt = max(0, min(n_obs, k) - 1)
    psi_obs += (zeta_binding_coefficient(k) * m_total * (get_c_k(k)**2) * np.exp(-decay_lambda * time_t) * filt)
psi_obs *= v_val

st.info(f"**Total Observable System State \u03A8_obs at time t={time_t} : {psi_obs:.4e} Joules**")
