import streamlit as st
from auth.auth import AuthManager
from interface.dashboard import Dashboard
from interface.campaigns import CampaignManager
from interface.analytics import Analytics
from interface.products import ProductManager
from interface.roi import ROIAnalysis
from interface.sales_profit import SalesProfitAnalysis
from database.db import DatabaseManager
import extra_streamlit_components as stx
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from testes_sales import SalesManager


# Configuração inicial da página
st.set_page_config(
    page_title="Kirvano Manager",
    page_icon="📈",
    layout="wide"
)

# Inicializa o gerenciador de autenticação
auth = AuthManager()

# Verifica se o banco de dados está inicializado
db_manager = DatabaseManager()
db_manager.initialize_database()

# Página de login/cadastro
if not auth.is_authenticated():
    st.title("Marketing Manager - Login")
    
    tab1, tab2 = st.tabs(["Login", "Cadastro"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Nome de usuário", value=auth.check_remembered_user())
            password = st.text_input("Senha", type="password")
            remember_me = st.checkbox("Lembrar de mim")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                auth.login_user(username, password, remember_me)
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Escolha um nome de usuário")
            new_email = st.text_input("Seu e-mail")
            new_password = st.text_input("Crie uma senha", type="password")
            confirm_password = st.text_input("Confirme a senha", type="password")
            submitted = st.form_submit_button("Cadastrar")
            
            if submitted:
                if new_password == confirm_password:
                    auth.register_user(new_username, new_email, new_password)
                else:
                    st.error("As senhas não coincidem!")

# Páginas autenticadas
else:
    
    st.sidebar.title(f"Olá, {auth.get_current_username()}!")
    if st.sidebar.button("Logout"):
        auth.logout_user()
    
    menu_options = {
        "Dashboard": Dashboard(),
        "Produtos": ProductManager(),
        "Campanhas": CampaignManager(),
        "Vendas e Lucros": SalesProfitAnalysis(),
        "Análise de ROI": ROIAnalysis(),
        "Análises": Analytics()
    }
    
    selected_page = st.sidebar.radio(
        "Menu",
        list(menu_options.keys()))
    
    # Exibe a página selecionada
    page = menu_options[selected_page]
    user_id = auth.get_current_user_id()
    
    if selected_page == "Dashboard":
        page.show_dashboard(user_id)
    elif selected_page == "Produtos":
        page.show_product_form(user_id)
        page.show_product_list(user_id)
    elif selected_page == "Campanhas":
        page.show_campaign_form(user_id)
        page.show_campaign_list(user_id)
    elif selected_page == "Vendas e Lucros":
        page.show_sales_profit_analysis(user_id)
    elif selected_page == "Análise de ROI":
        page.show_roi_analysis(user_id)
    elif selected_page == "Análises":
        page.show_sales_analytics(user_id)