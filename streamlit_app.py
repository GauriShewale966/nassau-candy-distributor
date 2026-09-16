import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(page_title="Nassau Candy Analytics",layout="wide")
st.title("Nassau Candy Distributor — Analytics Dashboard")
st.caption("Upload the validated CSV to explore business, division, product, Pareto and margin performance.")
f=st.file_uploader("Upload validated CSV",type=["csv"])
if f is None:
    st.info("Upload Nassau_Candy_Distributor_Validated_Analysis.csv to begin.")
    st.stop()
df=pd.read_csv(f)
for c in ["Sales","Cost","Gross Profit","Units"]: df[c]=pd.to_numeric(df[c],errors="coerce")
prod=df.groupby("Product Name",as_index=False).agg(Sales=("Sales","sum"),Cost=("Cost","sum"),Gross_Profit=("Gross Profit","sum"),Units=("Units","sum"))
prod["Gross Margin %"]=prod.Gross_Profit/prod.Sales
prod["Cost % of Sales"]=prod.Cost/prod.Sales
benchmark=prod.Gross_Profit.sum()/prod.Sales.sum()
a,b,c,d=st.columns(4)
a.metric("Total Sales",f"${prod.Sales.sum():,.2f}")
b.metric("Gross Profit",f"${prod.Gross_Profit.sum():,.2f}")
c.metric("Gross Margin",f"{benchmark:.2%}")
d.metric("Units",f"{prod.Units.sum():,.0f}")
st.subheader("Division Performance")
div=df.groupby("Division",as_index=False).agg(Sales=("Sales","sum"),Cost=("Cost","sum"),Gross_Profit=("Gross Profit","sum"),Units=("Units","sum"))
div["Gross Margin %"]=div.Gross_Profit/div.Sales
st.dataframe(div.style.format({"Sales":"${:,.2f}","Cost":"${:,.2f}","Gross_Profit":"${:,.2f}","Gross Margin %":"{:.2%}"}),use_container_width=True)
st.bar_chart(div.set_index("Division")[["Sales","Gross_Profit"]])
st.subheader("Product Profitability")
st.dataframe(prod.sort_values("Gross_Profit",ascending=False).style.format({"Sales":"${:,.2f}","Cost":"${:,.2f}","Gross_Profit":"${:,.2f}","Gross Margin %":"{:.2%}","Cost % of Sales":"{:.2%}"}),use_container_width=True)
st.subheader("Sales vs Gross Margin")
st.scatter_chart(prod.set_index("Product Name")[["Sales","Gross Margin %"]],x="Sales",y="Gross Margin %")
st.subheader("Pareto")
p=prod.sort_values("Sales",ascending=False).copy()
p["Revenue Contribution %"]=p.Sales/p.Sales.sum();p["Cumulative Revenue %"]=p["Revenue Contribution %"].cumsum()
p["Profit Contribution %"]=p.Gross_Profit/p.Gross_Profit.sum();p["Cumulative Profit %"]=p["Profit Contribution %"].cumsum()
st.dataframe(p.style.format({"Sales":"${:,.2f}","Gross_Profit":"${:,.2f}","Revenue Contribution %":"{:.2%}","Cumulative Revenue %":"{:.2%}","Profit Contribution %":"{:.2%}","Cumulative Profit %":"{:.2%}"}),use_container_width=True)
st.download_button("Download Product Analysis CSV",prod.to_csv(index=False).encode(),file_name="product_profitability.csv",mime="text/csv")
