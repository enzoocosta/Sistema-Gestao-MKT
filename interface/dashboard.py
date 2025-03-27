import streamlit as st
from database.operations import DBOperations  
import plotly.express as px
import pandas as pd

class Dashboard:
    def __init__(self):
        """Dashboard principal com métricas de marketing"""
        self.db_ops = DBOperations()
    
    def show_main_dashboard(self, user_id):
        """Exibe o dashboard principal com métricas e gráficos"""
        st.title("📊 Dashboard de Marketing Digital")
        
        try:
            # Métricas principais
            metrics = self.db_ops.calculate_roi(user_id)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Receita Total", f"R$ {metrics['revenue']:,.2f}")
            with col2:
                st.metric("Despesas Totais", f"R$ {metrics['expenses']:,.2f}")
            with col3:
                st.metric("Lucro Total", f"R$ {metrics['profit']:,.2f}")
            with col4:
                st.metric("ROI", f"{metrics['roi']:.2f}%")
            
            # Gráfico de vendas por plataforma
            st.subheader("Vendas por Plataforma")
            sales = self.db_ops.get_user_sales(user_id)
            if sales:
                df_sales = pd.DataFrame(sales)
                # Calcula o valor total por plataforma
                df_sales['total_sale'] = df_sales['amount'] * df_sales['quantity']
                fig = px.pie(df_sales, 
                            names='platform', 
                            values='total_sale', 
                            title='Distribuição de Vendas por Plataforma',
                            hole=0.3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig)
            else:
                st.warning("Nenhuma venda registrada ainda.")
            
            # Gráfico de campanhas
            st.subheader("Desempenho das Campanhas")
            campaigns = self.db_ops.get_user_campaigns(user_id)
            if campaigns:
                df_campaigns = pd.DataFrame(campaigns)
                fig = px.bar(df_campaigns, 
                            x='name', 
                            y='budget', 
                            color='platform',
                            title='Orçamento por Campanha',
                            text='budget')
                fig.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
                fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                st.plotly_chart(fig)
            else:
                st.warning("Nenhuma campanha criada ainda.")
                
        except Exception as e:
            st.error(f"Erro ao carregar dashboard: {str(e)}")
            st.info("Verifique se existem campanhas e vendas cadastradas")