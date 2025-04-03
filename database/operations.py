from .db import DatabaseManager
import streamlit as st
from datetime import datetime, timedelta

class DBOperations:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_sale(self, user_id, product_name, amount, quantity, sale_date, platform, cost=0.0):
        """Registra uma nova venda no banco de dados"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO sales 
                (user_id, product_name, amount, quantity, cost, sale_date, platform) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user_id, product_name, amount, quantity, cost, sale_date, platform)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao registrar venda: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    # Operações de Usuário
    def get_user_by_username(self, username):
        """Obtém um usuário pelo nome de usuário"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
        except Exception as e:
            st.error(f"Erro ao buscar usuário: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def create_user(self, username, email, password):
        """Cria um novo usuário no banco de dados"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao criar usuário: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    # Operações de Produtos
    def create_product(self, user_id, name, description, price, platform):
        """Cria um novo produto"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO products 
                (user_id, name, description, price, platform) 
                VALUES (%s, %s, %s, %s, %s)""",
                (user_id, name, description, price, platform)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao criar produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_product(self, product_id):
        """Exclui um produto do banco de dados"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Verifica se existem vendas associadas
            cursor.execute("SELECT COUNT(*) FROM sales WHERE product_name IN (SELECT name FROM products WHERE id = %s)", (product_id,))
            if cursor.fetchone()[0] > 0:
                return {"success": False, "message": "Este produto possui vendas associadas"}
            
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            return {"success": True, "message": "Produto excluído com sucesso"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao excluir produto: {e}"}
        finally:
            cursor.close()
            conn.close()
    
    def get_user_products(self, user_id):
        """Obtém todos os produtos de um usuário"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM products WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def update_product(self, product_id, name, description, price, platform):
        """Atualiza um produto existente"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE products 
                SET name = %s, description = %s, price = %s, platform = %s
                WHERE id = %s""",
                (name, description, price, platform, product_id)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def delete_product(self, product_id):
        """Exclui um produto"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao excluir produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    # Operações de Campanhas
    def create_campaign(self, user_id, name, platform, budget, start_date, end_date=None):
        """Cria uma nova campanha de marketing"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO campaigns 
                (user_id, name, platform, budget, start_date, end_date) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, name, platform, budget, start_date, end_date)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            st.error(f"Erro ao criar campanha: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def delete_campaign(self, campaign_id):
        """Exclui uma campanha do banco de dados"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Verifica se existem despesas associadas
            cursor.execute("SELECT COUNT(*) FROM expenses WHERE campaign_id = %s", (campaign_id,))
            if cursor.fetchone()[0] > 0:
                return {"success": False, "message": "Esta campanha possui despesas associadas"}
            
            cursor.execute("DELETE FROM campaigns WHERE id = %s", (campaign_id,))
            conn.commit()
            return {"success": True, "message": "Campanha excluída com sucesso"}
        except Exception as e:
            return {"success": False, "message": f"Erro ao excluir campanha: {e}"}
        finally:
            cursor.close()
            conn.close()
    
    def get_user_campaigns(self, user_id):
        """Obtém todas as campanhas de um usuário"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM campaigns WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    # Operações de Vendas
    def create_sale(self, user_id, product_name, amount, quantity, sale_date, platform, cost=0.0):
        """Registra uma nova venda no banco de dados"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO sales 
                (user_id, product_name, amount, quantity, cost, sale_date, platform) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user_id, product_name, amount, quantity, cost, sale_date, platform)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao registrar venda: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def get_user_sales(self, user_id, limit=None):
        """Obtém vendas do usuário com suporte a limite"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM sales WHERE user_id = %s ORDER BY created_at DESC"
            params = (user_id,)
        
            if limit is not None:
                query += " LIMIT %s"
                params = (user_id, limit)
        
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def get_sales_date_range(self, user_id):
        """Obtém o intervalo de datas das vendas"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT MIN(sale_date), MAX(sale_date) 
                FROM sales 
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    
    # Operações de Análise
    def calculate_roi(self, user_id):
        """Calcula ROI básico: (Receita - Despesas) / Despesas * 100"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            # Total de despesas
            cursor.execute("""
                SELECT COALESCE(SUM(e.amount), 0)
                FROM expenses e
                JOIN campaigns c ON e.campaign_id = c.id
                WHERE c.user_id = %s
            """, (user_id,))
            expenses = cursor.fetchone()[0]

            # Total de vendas
            cursor.execute("""
                SELECT COALESCE(SUM(amount * quantity), 0)
                FROM sales
                WHERE user_id = %s
            """, (user_id,))
            revenue = cursor.fetchone()[0]

            # Cálculo do ROI
            roi = ((revenue - expenses) / expenses * 100) if expenses > 0 else 0
            
            return {
                "revenue": revenue,
                "expenses": expenses,
                "profit": revenue - expenses,
                "roi": roi
            }
        except Exception as e:
            print(f"Erro ao calcular ROI: {e}")
            return {
                "revenue": 0,
                "expenses": 0,
                "profit": 0,
                "roi": 0
            }
        finally:
            cursor.close()
            conn.close()
    
    def calculate_detailed_roi(self, user_id):
        """Calcula ROI detalhado com dados por período e campanha"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            # Dados totais consolidados
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(s.amount * s.quantity), 0) as total_revenue,
                    COALESCE(SUM(e.amount), 0) as total_investment,
                    COALESCE(SUM(s.amount * s.quantity) - SUM(e.amount), 0) as total_profit,
                    CASE 
                        WHEN COALESCE(SUM(e.amount), 0) > 0 THEN 
                            (COALESCE(SUM(s.amount * s.quantity), 0) - COALESCE(SUM(e.amount), 0)) / 
                            COALESCE(SUM(e.amount), 1) * 100
                        ELSE 0
                    END as roi
                FROM sales s
                LEFT JOIN expenses e ON e.campaign_id IN (
                    SELECT id FROM campaigns WHERE user_id = %s
                )
                WHERE s.user_id = %s
            """, (user_id, user_id))
            totals = cursor.fetchone()

            # ROI por período mensal
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(s.sale_date, '%%Y-%%m') as period,
                    COALESCE(SUM(s.amount * s.quantity), 0) as revenue,
                    COALESCE(SUM(e.amount), 0) as investment,
                    CASE 
                        WHEN COALESCE(SUM(e.amount), 0) > 0 THEN 
                            (COALESCE(SUM(s.amount * s.quantity), 0) - COALESCE(SUM(e.amount), 0)) / 
                            COALESCE(SUM(e.amount), 1) * 100
                        ELSE 0
                    END as roi
                FROM sales s
                LEFT JOIN expenses e ON e.campaign_id IN (
                    SELECT id FROM campaigns WHERE user_id = %s
                ) AND DATE_FORMAT(e.date, '%%Y-%%m') = DATE_FORMAT(s.sale_date, '%%Y-%%m')
                WHERE s.user_id = %s
                GROUP BY DATE_FORMAT(s.sale_date, '%%Y-%%m')
                ORDER BY period
            """, (user_id, user_id))
            roi_by_period = cursor.fetchall()

            # ROI por campanha individual
            cursor.execute("""
                SELECT 
                    c.id,
                    c.name as campaign_name,
                    c.platform,
                    c.budget,
                    COALESCE(SUM(s.amount * s.quantity), 0) as revenue,
                    COALESCE(SUM(e.amount), 0) as investment,
                    CASE 
                        WHEN COALESCE(SUM(e.amount), 0) > 0 THEN 
                            (COALESCE(SUM(s.amount * s.quantity), 0) - COALESCE(SUM(e.amount), 0)) / 
                            COALESCE(SUM(e.amount), 1) * 100
                        ELSE 0
                    END as roi,
                    c.start_date,
                    IFNULL(c.end_date, CURDATE()) as end_date
                FROM campaigns c
                LEFT JOIN expenses e ON e.campaign_id = c.id
                LEFT JOIN sales s ON s.user_id = c.user_id 
                    AND s.platform = c.platform 
                    AND s.sale_date BETWEEN c.start_date AND IFNULL(c.end_date, CURDATE())
                WHERE c.user_id = %s
                GROUP BY c.id, c.name, c.platform, c.budget, c.start_date, c.end_date
            """, (user_id,))
            campaigns_roi = cursor.fetchall()

            return {
                "total_revenue": float(totals['total_revenue']),
                "total_investment": float(totals['total_investment']),
                "total_profit": float(totals['total_profit']),
                "roi": float(totals['roi']),
                "roi_by_period": roi_by_period,
                "campaigns_roi": campaigns_roi
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "total_revenue": 0,
                "total_investment": 0,
                "total_profit": 0,
                "roi": 0,
                "roi_by_period": [],
                "campaigns_roi": []
            }
        finally:
            cursor.close()
            conn.close()
        
    def get_sales_profit_data(self, user_id, start_date=None, end_date=None):
        """Obtém dados de vendas e lucros com cálculo do profit"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    s.id,
                    s.product_name,
                    s.amount,
                    s.quantity,
                    s.sale_date,
                    s.platform,
                    s.amount * s.quantity as total_sale,
                    (s.amount * s.quantity) - (IFNULL(p.cost, 0) * s.quantity) as profit,
                    IFNULL(p.cost, 0) as cost
                FROM sales s
                LEFT JOIN products p ON s.product_name = p.name AND s.user_id = p.user_id
                WHERE s.user_id = %s
            """
            params = [user_id]
            
            if start_date and end_date:
                query += " AND s.sale_date BETWEEN %s AND %s"
                params.extend([start_date, end_date])
            
            query += " ORDER BY s.sale_date DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            import traceback
            traceback.print_exc()
            st.error(f"Erro ao buscar dados de vendas: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    def execute_fetch_query(self, query, params=None):
        """Para queries SELECT que retornam dados"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def execute_update_query(self, query, params=None):
        """Para INSERT/UPDATE/DELETE"""
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()