import streamlit as st
from database.operations import DBOperations
import plotly.express as px
import pandas as pd

class Analytics:
    def __init__(self):
        """Ferramentas de análise de desempenho"""
        self.db_ops = DBOperations()
    
    def show_sales_analytics(self, user_id):
        """Exibe análises detalhadas de vendas"""
        st.title("📈 Análise de Vendas")
        
        sales = self.db_ops.get_user_sales(user_id)
        if not sales:
            st.warning("Nenhuma venda registrada para análise.")
            return
        
        df = pd.DataFrame(sales)
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        
        # Filtros
        st.sidebar.subheader("Filtros")
        min_date = df['sale_date'].min().date()
        max_date = df['sale_date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Período",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['sale_date'].dt.date >= start_date) & 
                    (df['sale_date'].dt.date <= end_date)]
        
        # Métricas
        total_sales = df['amount'].sum()
        avg_sale = df['amount'].mean()
        total_units = df['quantity'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total em Vendas", f"R$ {total_sales:,.2f}")
        col2.metric("Ticket Médio", f"R$ {avg_sale:,.2f}")
        col3.metric("Unidades Vendidas", total_units)
        
        # Gráfico de vendas ao longo do tempo
        st.subheader("Vendas ao Longo do Tempo")
        df_time = df.groupby(pd.Grouper(key='sale_date', freq='D'))['amount'].sum().reset_index()
        fig = px.line(df_time, x='sale_date', y='amount', title='Vendas Diárias')
        st.plotly_chart(fig)
        
        # Gráfico de produtos mais vendidos
        st.subheader("Produtos Mais Vendidos")
        df_products = df.groupby('product_name')['quantity'].sum().reset_index()
        fig = px.bar(df_products, x='product_name', y='quantity', 
                     title='Quantidade Vendida por Produto')
        st.plotly_chart(fig)