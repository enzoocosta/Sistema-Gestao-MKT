import streamlit as st
from database.operations import DBOperations
import plotly.express as px
import pandas as pd

class ROIAnalysis:
    def __init__(self):
        """Análise detalhada de ROI"""
        self.db_ops = DBOperations()
    
    def show_roi_analysis(self, user_id):
        """Exibe análise detalhada de ROI"""
        st.title("📊 Análise de ROI (Retorno sobre Investimento)")
        
        try:
            # Obter dados de ROI
            roi_data = self.db_ops.calculate_detailed_roi(user_id)
            
            if not roi_data or not roi_data.get('roi_by_period'):
                st.warning("Nenhum dado disponível para análise de ROI. Cadastre campanhas e vendas primeiro.")
                return
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Receita Total", f"R$ {roi_data['total_revenue']:,.2f}")
            col2.metric("Investimento Total", f"R$ {roi_data['total_investment']:,.2f}")
            col3.metric("Lucro Total", f"R$ {roi_data['total_profit']:,.2f}")
            col4.metric("ROI", f"{roi_data['roi']:.2f}%")
            
            # Gráfico de ROI por período
            st.subheader("ROI ao Longo do Tempo")
            df_roi = pd.DataFrame(roi_data['roi_by_period'])
            
            # Verifica se temos dados válidos para o gráfico
            if not df_roi.empty and 'period' in df_roi.columns and 'roi' in df_roi.columns:
                fig = px.line(
                    df_roi, 
                    x='period', 
                    y='roi', 
                    title='Evolução do ROI',
                    labels={'period': 'Período', 'roi': 'ROI (%)'},
                    markers=True
                )
                fig.update_layout(
                    xaxis_title='Período',
                    yaxis_title='ROI (%)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig)
            else:
                st.warning("Dados insuficientes para gerar gráfico de evolução do ROI.")
            
            # Tabela detalhada por campanha
            st.subheader("Detalhes por Campanha")
            if roi_data.get('campaigns_roi'):
                df_campaigns = pd.DataFrame(roi_data['campaigns_roi'])
                
                # Formata as colunas numéricas
                numeric_cols = ['budget', 'revenue', 'investment', 'roi']
                for col in numeric_cols:
                    if col in df_campaigns.columns:
                        if col == 'roi':
                            df_campaigns[col] = df_campaigns[col].apply(lambda x: f"{x:.2f}%")
                        else:
                            df_campaigns[col] = df_campaigns[col].apply(lambda x: f"R$ {x:,.2f}")
                
                st.dataframe(df_campaigns)
            else:
                st.warning("Nenhuma campanha disponível para análise.")
                
        except Exception as e:
            st.error(f"Erro ao gerar análise de ROI: {str(e)}")
            st.error("Verifique se existem campanhas e vendas registradas no sistema.")