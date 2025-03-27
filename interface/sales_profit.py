import streamlit as st
from database.operations import DBOperations
import plotly.express as px
import pandas as pd
from datetime import datetime, date

class SalesProfitAnalysis:
    def __init__(self):
        """Análise de vendas e lucros"""
        self.db_ops = DBOperations()
    
    def show_sales_profit_analysis(self, user_id):
        """Exibe análise de vendas e lucros"""
        st.title("💰 Análise de Vendas e Lucros")
        
        try:
            # Filtros
            st.sidebar.subheader("Filtros")
            
            # Obtém intervalo de datas com tratamento de erros
            min_date, max_date = self._get_valid_date_range(user_id)
            
            # Widget de seleção de período
            date_range = st.sidebar.date_input(
                "Período",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            # Verifica se o usuário selecionou um intervalo válido
            if len(date_range) != 2:
                st.warning("Selecione um intervalo de datas válido")
                return
                
            start_date, end_date = date_range
            
            # Obter dados filtrados
            sales_data = self.db_ops.get_sales_profit_data(user_id, start_date, end_date)
            
            if not sales_data:
                st.warning("Nenhuma venda registrada no período selecionado.")
                return
            
            # Processa os dados para análise
            df = self._process_sales_data(sales_data)
            
            # Exibe métricas e visualizações
            self._display_metrics(df)
            self._display_profit_chart(df)
            self._display_sales_table(df)
            
        except Exception as e:
            st.error(f"Erro ao carregar análise de vendas: {str(e)}")
            st.error("Verifique se existem vendas registradas e se as datas estão corretas no banco de dados.")

    def _get_valid_date_range(self, user_id):
        """Obtém e valida o intervalo de datas das vendas"""
        min_date, max_date = self.db_ops.get_sales_date_range(user_id)
        
        # Se não houver vendas, usa datas padrão
        if min_date is None or max_date is None:
            today = date.today()
            return today, today
            
        # Converte datetime para date se necessário
        if isinstance(min_date, datetime):
            min_date = min_date.date()
        if isinstance(max_date, datetime):
            max_date = max_date.date()
            
        return min_date, max_date

    def _process_sales_data(self, sales_data):
        """Processa os dados de vendas para análise"""
        if not sales_data:
            raise ValueError("Nenhuma venda registrada.")
        df = pd.DataFrame(sales_data)

        # Validação adicional dos dados
        if df['amount'].min() <= 0:
            st.warning("Atenção: Existem valores de venda negativos no banco de dados")
        if df['quantity'].min() <= 0:
            st.warning("Atenção: Existem quantidades inválidas (<0) no banco de dados")
        
        # Calcula totais e margens
        df['total_sale'] = df['amount'] * df['quantity']
        df['profit_margin'] = (df['profit'] / df['total_sale'] * 100).round(2)
        
        return df

    def _display_metrics(self, df):
        """Exibe as métricas principais"""
        total_sales = df['total_sale'].sum()
        total_profit = df['profit'].sum()
        avg_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Vendas Totais", f"R$ {total_sales:,.2f}")
        col2.metric("Lucro Total", f"R$ {total_profit:,.2f}")
        col3.metric("Margem de Lucro Média", f"{avg_profit_margin:.2f}%")

    def _display_profit_chart(self, df):
        """Exibe gráfico de vendas vs lucro"""
        st.subheader("Vendas vs Lucro por Produto")
        
        # Agrupa por produto
        df_grouped = df.groupby('product_name')[['total_sale', 'profit']].sum().reset_index()
        
        fig = px.bar(
            df_grouped, 
            x='product_name', 
            y=['total_sale', 'profit'], 
            barmode='group', 
            title='Comparação de Vendas e Lucro',
            labels={'value': 'Valor (R$)', 'variable': 'Tipo'}
        )
        
        # Melhora a formatação do gráfico
        fig.update_layout(
            xaxis_title='Produto',
            yaxis_title='Valor (R$)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig)

    def _display_sales_table(self, df):
        """Exibe tabela detalhada de vendas"""
        st.subheader("Detalhes das Vendas")
        
        # Seleciona e renomeia colunas para exibição
        display_df = df[[
            'product_name', 'sale_date', 'platform', 
            'quantity', 'amount', 'total_sale', 
            'profit', 'profit_margin'
        ]].copy()
        
        display_df.columns = [
            'Produto', 'Data Venda', 'Plataforma',
            'Quantidade', 'Preço Unitário', 'Total Venda',
            'Lucro', 'Margem (%)'
        ]
        
        # Formata valores monetários
        display_df['Preço Unitário'] = display_df['Preço Unitário'].apply(lambda x: f"R$ {x:,.2f}")
        display_df['Total Venda'] = display_df['Total Venda'].apply(lambda x: f"R$ {x:,.2f}")
        display_df['Lucro'] = display_df['Lucro'].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(display_df.sort_values('Data Venda', ascending=False))