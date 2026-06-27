import pandas as pd
import plotly.express as px

sip = pd.read_csv("04_monthly_sip_inflows.csv")

sip["month"] = pd.to_datetime(sip["month"])

fig = px.line(
    sip,
    x="month",
    y="sip_inflow_crore",
    markers=True,
    title="Monthly SIP Inflows"
)

# Highest SIP
highest = sip.loc[sip["sip_inflow_crore"].idxmax()]

fig.add_annotation(
    x=highest["month"],
    y=highest["sip_inflow_crore"],
    text="Highest SIP",
    showarrow=True
)

fig.show()