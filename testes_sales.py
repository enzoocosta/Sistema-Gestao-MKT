import streamlit as st
from database.operations import DBOperations
from datetime import date

def test_sales_page():
    st.title("📝 Página de Teste de Vendas")
    
    db_ops = DBOperations()
    user_id = st.number_input("ID do Usuário", min_value=1, value=1)
    
    # Buscar produtos cadastrados
    produtos = db_ops.get_user_products(user_id)
    nomes_produtos = [prod['name'] for prod in produtos] if produtos else []
    
    if not nomes_produtos:
        st.warning("⚠️ Cadastre produtos antes de registrar vendas!")
        return
    
    with st.form("test_sale_form"):
        # Seleção de produto
        product_name = st.selectbox("Produto*", options=nomes_produtos)
        
        # Dados do produto selecionado
        produto = next((p for p in produtos if p['name'] == product_name), None)
        
        # Campos do formulário
        amount = st.number_input("Preço*", 
                               min_value=0.01, 
                               value=float(produto['price']) if produto else 0.0)
        quantity = st.number_input("Quantidade*", min_value=1, value=1)
        cost = st.number_input("Custo*", 
                             min_value=0.0, 
                             value=float(produto['cost']) if produto else 0.0)
        sale_date = st.date_input("Data*", value=date.today())
        platform = st.selectbox("Plataforma*", ["Kirvano", "Hotmart", "Eduzz", "Outros"])
        
        if st.form_submit_button("Registrar Venda"):
            try:
                success = db_ops.create_sale(
                    user_id=user_id,
                    product_name=product_name,
                    amount=amount,
                    quantity=quantity,
                    cost=cost,
                    sale_date=sale_date,
                    platform=platform
                )
                if success:
                    st.success(f"✅ Venda registrada: {product_name}")
                    st.balloons()
                else:
                    st.error("❌ Falha ao registrar venda")
            except Exception as e:
                st.error(f"Erro: {str(e)}")

if __name__ == "__main__":
    test_sales_page()