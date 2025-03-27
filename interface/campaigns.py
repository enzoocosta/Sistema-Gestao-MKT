import streamlit as st
from database.operations import DBOperations
from datetime import datetime
from interface.components.delete_modal import delete_modal  # Adicione este import

class CampaignManager:
    def __init__(self):
        """Gerenciador de campanhas de marketing"""
        self.db_ops = DBOperations()
    
    def show_campaign_form(self, user_id):
        """Exibe o formulário para criação de novas campanhas"""
        with st.form("campaign_form"):
            st.subheader("Nova Campanha de Marketing")
            
            name = st.text_input("Nome da Campanha*")
            platform = st.selectbox(
                "Plataforma*", 
                ["Facebook Ads", "Google Ads", "Instagram", "TikTok", "Outros"]
            )
            budget = st.number_input("Orçamento (R$)*", min_value=0.01, step=0.01)
            start_date = st.date_input("Data de Início*", datetime.now())
            end_date = st.date_input("Data de Término (opcional)", None)
            
            submitted = st.form_submit_button("Salvar Campanha")
            
            if submitted:
                if not name or not platform or not budget:
                    st.error("Por favor, preencha todos os campos obrigatórios (*)")
                else:
                    campaign_id = self.db_ops.create_campaign(
                        user_id, name, platform, budget, start_date, end_date
                    )
                    if campaign_id:
                        st.success("Campanha criada com sucesso!")

    def show_campaign_list(self, user_id):
        """Exibe a lista de campanhas do usuário com ações"""
        st.subheader("Suas Campanhas")
        campaigns = self.db_ops.get_user_campaigns(user_id)
        
        if not campaigns:
            st.info("Você ainda não criou nenhuma campanha.")
            return
        
        for campaign in campaigns:
            with st.expander(f"{campaign['name']} - {campaign['platform']}"):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**Orçamento:** R$ {campaign['budget']:,.2f}")
                    st.write(f"**Status:** {campaign['status']}")
                    st.write(f"**Início:** {campaign['start_date']}")
                    if campaign['end_date']:
                        st.write(f"**Término:** {campaign['end_date']}")
                
                with col2:
                    if st.button("Editar", key=f"edit_{campaign['id']}"):
                        st.session_state['editing_campaign'] = campaign['id']
                
                with col3:
                    delete_modal(
                        item_type="Campanha",
                        item_id=campaign['id'],
                        item_name=campaign['name'],
                        delete_callback=self.db_ops.delete_campaign
                    )

    def show_edit_form(self, campaign_id, user_id):
        """Exibe o formulário de edição (opcional)"""
        # Implemente conforme necessário
        pass

    def show_campaigns_page(self, user_id):
        """Página principal de campanhas"""
        tab1, tab2 = st.tabs(["Lista de Campanhas", "Nova Campanha"])
        
        with tab1:
            self.show_campaign_list(user_id)
        
        with tab2:
            self.show_campaign_form(user_id)