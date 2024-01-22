import streamlit as st
import numpy as np
import pandas as pd
import pdfkit
from datetime import date
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
from streamlit.components.v1 import iframe
#st.header("Estimated Battery Lifetime")

def app():

    st.title("EV Range Estimation")
    st.markdown("This application estimates the lifetime of an EV battery based on kilometer used, state of charge, and weather conditions.")
    left,right = st.columns(2)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")



    #left.write("Enter Parameters")
    form = left.form("template_form")
    #left.write("1. Kilometers Used (km)")

    kilometers_used = form.slider("Enter kilometers used:", 0, 100000, 50000)

    #left.write("2. State of Charge (SoC)")
    state_of_charge = form.slider("Enter state of charge (%):", 0, 50, 10)

    #left.write("3. Temperature")
    temperature = form.slider("Enter temperature (C):", -30, 60, 25)

    #left.write("4. Average Energy Demand")
    energy_demand = form.slider("Enter average energy demand (kWh):", 0.0, 100.0, 10.0)


    submit = form.form_submit_button("Save Data")

    #right.write("5. Depth of Discharge")
    form = right.form("Styles")
    state_of_health = form.slider("Enter State of Health (%):", 0, 100, 80)

    #right.write("6. Driving Pattern")
    driving_pattern = form.selectbox("Choose driving pattern:", ("Mixed", "City", "Highway"))

    #right.write("7. Environmental Conditions")
    environmental_conditions = form.selectbox("Choose environmental conditions:", ("Mixed", "City", "Highway"))

    #right.write("8. Weather Conditions")
    weather_conditions = form.selectbox("Choose weather conditions:", ("Clear", "Rainy", "Snowy"))


    submit = form.form_submit_button("Generate Report")
    # Here you would need to use a model or lookup table to get the estimated lifetime.
    # For this example, let's use a simplified approach where the estimated lifetime decreases as the kilometers used increase.
    estimated_lifetime = 1000000 - kilometers_used

    # Update the estimated lifetime based on weather conditions
    if weather_conditions == "Rainy":
        estimated_lifetime *= 0.95
    elif weather_conditions == "Snowy":
        estimated_lifetime *= 0.9


    if submit:
        html = template.render(
        kilometers_used = kilometers_used,
        state_of_charge = state_of_charge,
        temperature = temperature,
        energy_demand = energy_demand,
        state_of_health = state_of_health,
        driving_pattern = driving_pattern,
        environmental_conditions = environmental_conditions,
        weather_conditions = weather_conditions,
        date = date.today().strftime("%B %d, %Y"),

        )

        pdf = pdfkit.from_string(html,False)
        st.balloons()

        left.success("🎉 Your Report was generated!")

        left.download_button(
            "⬇️ Download PDF",
            data=pdf,
            file_name="Range Record.pdf",
            mime="application/octet-stream",
    )
    st.write(f"The estimated lifetime of your EV battery is: {estimated_lifetime:.0f} kilometers.")
