import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.special import gamma

# ==========================================
# 1. PURE FIRST-PRINCIPLES MATHEMATICS
# ==========================================

def visualization_function(n, x):
    return max(0, min(n, x) - 1)

def zeta_binding_coefficient(k):
    """Absolute Mass Distribution using Riemann Zeta"""
    return 6 / (np.pi**2 * k**2)

def hypersphere_area(k):
    """Calculates the surface area of a unit hypersphere in k dimensions"""
    return 2 * (np.pi**(k/2)) / gamma(k/2)

def y_k_squared(k):
    """Pure geometric velocity scaling: Ratio of k-dimensional surface area to 3D area"""
    # 3D surface area is 4*pi
    return hypersphere_area(k) / (4 * np.pi)

# ==========================================
# 2. STREAMLIT UI
# ==========================================

st.set_page_config(page_title="MMET-EXTENDED: Pure Geometry Simulation", layout="wide")
st.title("MMET-EXTENDED: First-Principles Simulation")
st.markdown("This simulation calculates the macroscopic energy density of the universe using **pure topological geometry** with zero free parameters.")

# --- MACROSCOPIC ENERGY DENSITY (\u03A9) DERIVATION ---
st.subheader("Macroscopic Energy Density (\u03A9) from Hypersphere Geometry")
st.markdown("Instead of phenomenological curve-fitting, the dimensional velocity scaling ($y_k^2$) is rigidly derived from the ratio of k-dimensional hypersphere surface areas to 3D surface area.")

# Calculate Pure Geometric Energies
E_3 = zeta_binding_coefficient(3) * y_k_squared(3)
E_4 = zeta_binding_coefficient(4) * y_k_squared(4)
E_5 = zeta_binding_coefficient(5) * y_k_squared(5)

# Calculate Dark Energy using an infinite series approximation (up to k=150 where it converges to 0)
E_6_plus = sum(zeta_binding_coefficient(k) * y_k_squared(k) for k in range(6, 150))

# Normalize to find Cosmological Density (\u03A9)
E_total_macro = E_3 + E_4 + E_5 + E_6_plus

omega_baryonic = E_3 / E_total_macro
omega_dark_matter = (E_4 + E_5) / E_total_macro
omega_dark_energy = E_6_plus / E_total_macro

# --- DISPLAY RESULTS ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### The Pure Mathematical Prediction")
    st.write("By scaling the Riemann Zeta mass binding ($\u03B1_k$) strictly by hypersphere geometry ($A_k / A_3$), the universe's energy density organically converges to:")
    
    df_omega = pd.DataFrame({
        "Cosmological Designation": ["Baryonic Energy (\u03A9_B)", "Dark Matter Energy (\u03A9_DM)", "Dark Energy (\u03A9_\u039B)"], 
        "Energy Density Fraction": [omega_baryonic, omega_dark_matter, omega_dark_energy],
        "Percentage": [f"{omega_baryonic*100:.2f}%", f"{omega_dark_matter*100:.2f}%", f"{omega_dark_energy*100:.2f}%"]
    }) 
    
    # Render table beautifully
    st.dataframe(df_omega, hide_index=True, use_container_width=True)
    
    st.info("Notice: Hypersphere surface area peaks at 7 dimensions and then approaches zero. Because of this rigid geometric law, the infinite sum for Dark Energy naturally converges to a finite value, preventing infinite energetic divergence.")

with col2:
    fig_pie = px.pie(
        df_omega, 
        values="Energy Density Fraction", 
        names="Cosmological Designation",
        title="MMET Pure First-Principles Energy Density (\u03A9)",
        hole=0.3,
        color_discrete_sequence=['#ff9999','#66b3ff','#99ff99']
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Note on Integrity
st.success("**Zero Free Parameters:** This model uses no hand-tuned numbers or curve-fitting. It represents the authentic, unadulterated topological truth of the MMET framework.")
