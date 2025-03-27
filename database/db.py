import mysql.connector
from mysql.connector import Error
import streamlit as st

class DatabaseManager:
    def __init__(self):
        """Inicializa o gerenciador de banco de dados com as credenciais do MySQL"""
        self.host = "localhost"
        self.database = "kirvano_manager"
        self.user = "root"
        self.password = "E2004!zo"
        self.connection = None

    def connect(self):
        """Estabelece conexão com o banco de dados MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            st.error(f"Erro ao conectar ao MySQL: {e}")
            return None

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def initialize_database(self):
        """Cria a estrutura inicial do banco de dados se não existir"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Criação das tabelas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                platform VARCHAR(50) NOT NULL,
                budget DECIMAL(10, 2) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE,
                status VARCHAR(20) DEFAULT 'active',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                campaign_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                description VARCHAR(255),
                date DATE NOT NULL,
                category VARCHAR(50) NOT NULL,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                quantity INT NOT NULL,
                sale_date DATE NOT NULL,
                platform VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                cost DECIMAL(10, 2) DEFAULT 0.00,
                platform VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            conn.commit()
            st.success("Banco de dados inicializado com sucesso!")
        except Error as e:
            st.error(f"Erro ao inicializar banco de dados: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()