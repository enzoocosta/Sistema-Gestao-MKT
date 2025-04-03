import streamlit as st
from database.operations import DBOperations
from datetime import datetime, date, time
from typing import Dict, Optional, Any, Union, List

class SalesManager:
    def __init__(self):
        self.db_ops = DBOperations()
        self.platform_commissions = {
            "Hotmart": 0.3,
            "Eduzz": 0.25,
            "Monetizze": 0.2,
            "Kirvano": 0.15,
            "Outros": 0.1
        }
    
    def show_sales_page(self, user_id: int):
        """Página principal de vendas com auto-preenchimento"""
        st.title("💰 Registro de Vendas")
        
        products = self.db_ops.get_user_products(user_id)
        if not products:
            st.warning("Cadastre produtos antes de registrar vendas")
            return
        
        # Usando st.session_state para armazenar o produto selecionado
        if 'selected_product' not in st.session_state:
            st.session_state.selected_product = products[0]
        
        # Atualiza o produto selecionado quando muda
        selected_product_name = st.selectbox(
            "Selecione o produto*",
            options=[p['name'] for p in products],
            index=0,
            key="product_select"
        )
        
        # Atualiza o produto na sessão
        st.session_state.selected_product = next(
            (p for p in products if p['name'] == selected_product_name),
            products[0]
        )
        
        current_product = st.session_state.selected_product
        
        with st.form("sale_form", border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Preço de venda (auto-preenchido)
                sale_price = st.number_input(
                    "Preço de Venda*",
                    min_value=0.01,
                    value=float(current_product['price']),
                    step=0.01,
                    key="sale_price"
                )
                
                quantity = st.number_input(
                    "Quantidade*", 
                    min_value=1, 
                    value=1,
                    key="quantity"
                )
                
                platform = st.selectbox(
                    "Plataforma*",
                    options=list(self.platform_commissions.keys()),
                    index=list(self.platform_commissions.keys()).index(
                        current_product.get('platform', 'Hotmart')
                    ),
                    key="platform"
                )
                
                sale_date = st.date_input(
                    "Data da Venda*",
                    value=date.today(),
                    key="sale_date"
                )
            
            with col2:
                commission_rate = self.platform_commissions.get(platform, 0.1)
                total_sale = sale_price * quantity
                commission_value = total_sale * commission_rate
                net_value = total_sale - commission_value
                
                st.metric("Total Bruto", f"R$ {total_sale:.2f}")
                st.metric(f"Comissão ({commission_rate*100}%)", f"-R$ {commission_value:.2f}")
                st.metric("Valor Líquido", f"R$ {net_value:.2f}", delta_color="off")
            
            if st.form_submit_button("📝 Registrar Venda", use_container_width=True):
                success = self.db_ops.create_sale(
                    user_id=user_id,
                    product_name=current_product['name'],
                    amount=sale_price,
                    quantity=quantity,
                    sale_date=sale_date,
                    platform=platform,
                    cost=float(current_product.get('cost', 0.0))
                )
                
                if success:
                    st.success("Venda registrada com sucesso!")
                    st.balloons()
                else:
                    st.error("Erro ao registrar venda")

if __name__ == "__main__":
    sales_mgr = SalesManager()
    sales_mgr.show_sales_page(user_id=1)  # Substitua pelo ID real

    # sales.py (adição no final do método _process_sale)
    def _process_sale(self, user_id: int, sale_data: Dict[str, Any]):
        """Processa o registro da venda e força atualização do dashboard"""
        if self.db_ops.create_sale(
            user_id=user_id,
            product_name=sale_data['product_name'],
            amount=sale_data['amount'],
            quantity=sale_data['quantity'],
            sale_date=sale_data['sale_date'],
            platform=sale_data['platform'],
            cost=sale_data.get('cost', 0.0)
        ):
            st.success("Venda registrada com sucesso! Atualizando dashboard...")
            st.balloons()
            st.session_state.last_sale_update = datetime.now()  # Marca tempo da última venda
            time.sleep(2)  # Tempo para visualizar a mensagem
            st.rerun()  # Força atualização da página
        else:
            st.error("Erro ao registrar venda")