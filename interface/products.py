import streamlit as st
from database.operations import DBOperations

class ProductManager:
    def __init__(self):
        """Gerenciador de produtos do infoproduto"""
        self.db_ops = DBOperations()
    
    def show_product_form(self, user_id):
        """Exibe formulário para cadastro de novos produtos"""
        with st.form("product_form"):
            st.subheader("Cadastrar Novo Produto")
            
            name = st.text_input("Nome do Produto*")
            description = st.text_area("Descrição")
            price = st.number_input("Preço (R$)*", min_value=0.01, step=0.01)
            platform = st.selectbox(
                "Plataforma Principal*",
                ["Kirvano", "Hotmart", "Monetizze", "Eduzz", "Outros"]
            )
            
            submitted = st.form_submit_button("Salvar Produto")
            
            if submitted:
                if not name or not price:
                    st.error("Por favor, preencha os campos obrigatórios (*)")
                else:
                    if self.db_ops.create_product(user_id, name, description, price, platform):
                        st.success("Produto cadastrado com sucesso!")
                    else:
                        st.error("Erro ao cadastrar produto")
    
    def show_product_list(self, user_id):
        """Exibe lista de produtos cadastrados"""
        st.subheader("Seus Produtos")
        products = self.db_ops.get_user_products(user_id)
        
        if not products:
            st.info("Você ainda não cadastrou nenhum produto.")
            return
        
        for product in products:
            with st.expander(f"{product['name']} - R$ {product['price']:.2f}"):
                st.write(f"**Plataforma:** {product['platform']}")
                if product['description']:
                    st.write(f"**Descrição:** {product['description']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Editar {product['name']}", key=f"edit_{product['id']}"):
                        self._show_edit_form(product)
                with col2:
                    if st.button(f"Excluir {product['name']}", key=f"delete_{product['id']}"):
                        if self.db_ops.delete_product(product['id']):
                            st.success("Produto excluído com sucesso!")
                            st.rerun()
    
    def _show_edit_form(self, product):
        """Exibe formulário de edição de produto"""
        with st.form(f"edit_form_{product['id']}"):
            st.subheader(f"Editando {product['name']}")
            
            name = st.text_input("Nome do Produto*", value=product['name'])
            description = st.text_area("Descrição", value=product['description'])
            price = st.number_input("Preço (R$)*", min_value=0.01, step=0.01, value=float(product['price']))
            platform = st.selectbox(
                "Plataforma Principal*",
                ["Kirvano", "Hotmart", "Monetizze", "Eduzz", "Outros"],
                index=["Kirvano", "Hotmart", "Monetizze", "Eduzz", "Outros"].index(product['platform'])
            )
            
            submitted = st.form_submit_button("Atualizar Produto")
            
            if submitted:
                if not name or not price:
                    st.error("Por favor, preencha os campos obrigatórios (*)")
                else:
                    if self.db_ops.update_product(
                        product['id'], name, description, price, platform
                    ):
                        st.success("Produto atualizado com sucesso!")
                        st.rerun()

    def delete_product(self, product_id):
        """Exclui um produto do banco de dados"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Verifica se existem vendas associadas
            cursor.execute("SELECT COUNT(*) FROM sales WHERE product_name IN (SELECT name FROM products WHERE id = %s)", (product_id,))
            if cursor.fetchone()[0] > 0:
                st.warning("Este produto possui vendas associadas e não pode ser excluído.")
                return False
            
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            st.success("Produto excluído com sucesso!")
            return True
        except Exception as e:
            st.error(f"Erro ao excluir produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # Interface Streamlit para exclusão
    def delete_product_ui(self, user_id):
        """Mostra a interface para excluir produtos"""
        products = self.get_user_products(user_id)
        if not products:
            st.info("Nenhum produto cadastrado.")
            return

        with st.expander("🔴 Excluir Produto"):
            selected = st.selectbox(
                "Selecione o produto para excluir",
                options=[(p['id'], p['name']) for p in products],
                format_func=lambda x: f"{x[0]} - {x[1]}"
            )

            if st.button("Excluir Produto", type="primary"):
                product_id = selected[0]
                if self.delete_product(product_id):
                    st.rerun()