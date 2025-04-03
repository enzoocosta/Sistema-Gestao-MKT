# dashboard.py
import streamlit as st
from datetime import datetime
import time
from database.operations import DBOperations
import pandas as pd
import plotly.express as px

class Dashboard:
    def __init__(self):
        self.db_ops = DBOperations()
        self.last_checked = datetime.now()
    
    def show_dashboard(self, user_id):
        """Dashboard com atualização automática"""
        st.title("📊 Dashboard em Tempo Real")
        
        # Configurações de atualização
        auto_refresh = st.sidebar.checkbox("Atualização Automática", value=True)
        refresh_rate = st.sidebar.slider("Intervalo (segundos)", 2, 60, 5)
        
        # Container principal
        placeholder = st.empty()
        
        while auto_refresh:
            self._update_ui(placeholder, user_id)
            time.sleep(refresh_rate)  # Agora usando o módulo time correto
            
            # Verifica se o usuário desativou a atualização
            if not st.session_state.get('auto_refresh', True):
                break
    
    def _update_ui(self, placeholder, user_id):
        """Atualiza o conteúdo do dashboard"""
        with placeholder.container():
            # Seu conteúdo existente aqui
            pass
    
    def _check_new_sales(self, user_id):
        """Verifica novas vendas e mostra notificações"""
        query = """
            SELECT product_name, amount, quantity 
            FROM sales 
            WHERE user_id = %s AND created_at > %s
            ORDER BY created_at DESC
        """
        results = self.db_ops.execute_fetch_query(query, (user_id, self.last_checked))
        
        if results:
            for sale in results:
                total = float(sale['amount']) * int(sale['quantity'])
                st.toast(f"✅ Nova venda: {sale['product_name']} - R$ {total:.2f}", icon="💰")
            self.last_checked = datetime.now()
    
    def _update_ui(self, placeholder, user_id):
        """Atualiza todo o conteúdo do dashboard"""
        with placeholder.container():
            # Seção de métricas
            st.header("📈 Métricas Principais")
            self._show_key_metrics(user_id)
            
            # Seção de gráficos
            st.header("📊 Visualizações")
            self._show_sales_charts(user_id)
            
            # Últimas transações
            st.header("🔄 Atividade Recente")
            self._show_recent_activity(user_id)
    
    def _show_key_metrics(self, user_id):
        """Mostra os cards com as métricas principais"""
        metrics = self.db_ops.calculate_roi(user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Receita Total", f"R$ {metrics['revenue']:,.2f}")
        with col2:
            st.metric("Investimento", f"R$ {metrics['expenses']:,.2f}")
        with col3:
            st.metric("Lucro", f"R$ {metrics['profit']:,.2f}")
        with col4:
            st.metric("ROI", f"{metrics['roi']:.1f}%")
    
    def _show_sales_charts(self, user_id):
        """Mostra os gráficos de vendas"""
        sales = self.db_ops.get_user_sales(user_id)
        
        if sales:
            df = pd.DataFrame(sales)
            df['total'] = df['amount'] * df['quantity']
            
            tab1, tab2 = st.tabs(["Por Plataforma", "Histórico"])
            
            with tab1:
                fig = px.pie(df, names='platform', values='total', 
                            title='Distribuição por Plataforma')
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                fig = px.line(df.groupby('sale_date')['total'].sum().reset_index(), 
                             x='sale_date', y='total',
                             title='Vendas ao Longo do Tempo')
                st.plotly_chart(fig, use_container_width=True)
    
    def _show_recent_activity(self, user_id):
        """Mostra as últimas vendas registradas (versão corrigida)"""
        try:
            sales = self.db_ops.get_user_sales(user_id, limit=5)
            
            if not sales:
                st.warning("Nenhuma venda registrada ainda")
                return
                
            st.subheader("🔄 Últimas Vendas")
            
            for sale in sales:
                cols = st.columns([2, 1, 1, 1, 1])  # Adicionei uma coluna extra para status
                
                with cols[0]:
                    st.markdown(f"**{sale.get('product_name', 'N/A')}**")
                with cols[1]:
                    st.markdown(f"R$ {float(sale.get('amount', 0)):.2f}")
                with cols[2]:
                    st.markdown(f"x{sale.get('quantity', 1)}")
                with cols[3]:
                    st.markdown(f"`{sale.get('sale_date', 'Data desconhecida')}`")
                with cols[4]:
                    st.markdown(f"`{sale.get('status', 'Concluído')}`")
                
                st.divider()
                
        except Exception as e:
            st.error(f"Erro ao carregar vendas recentes: {str(e)}")

    def _update_ui(self, placeholder, user_id):
        with placeholder.container():
            # ... outros componentes
            self._show_recent_activity(user_id)

# Adicione este método ao seu DBOperations
"""
def get_user_sales(self, user_id, limit=None):
    conn = self.db.connect()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM sales WHERE user_id = %s ORDER BY created_at DESC"
        if limit:
            query += f" LIMIT {limit}"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
"""