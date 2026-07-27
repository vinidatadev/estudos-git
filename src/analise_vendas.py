#!/usr/bin/env python3
"""
Módulo para análise de dados de vendas.

Este script realiza análise estatística e visualização de dados de vendas,
gerando insights sobre performance por produto, vendedor e região.

Autor: Vinicius Data Dev
Data: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os


class AnalisadorVendas:
    """
    Classe responsável pela análise de dados de vendas.
    
    Attributes:
        df (pd.DataFrame): DataFrame contendo os dados de vendas
        data_path (str): Caminho para o arquivo de dados
    """
    
    def __init__(self, data_path: str):
        """
        Inicializa o analisador de vendas.
        
        Args:
            data_path (str): Caminho para o arquivo CSV de vendas
        """
        self.data_path = data_path
        self.df = None
    
    def carregar_dados(self) -> bool:
        """
        Carrega os dados do arquivo CSV.
        
        Returns:
            bool: True se os dados foram carregados com sucesso, False caso contrário
        """
        try:
            self.df = pd.read_csv(self.data_path)
            self.df['data'] = pd.to_datetime(self.df['data'])
            print(f"✅ Dados carregados com sucesso! {len(self.df)} registros encontrados.")
            return True
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo {self.data_path} não encontrado!")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def estatisticas_basicas(self) -> None:
        """Exibe estatísticas básicas dos dados de vendas."""
        if self.df is None:
            print("❌ Dados não carregados. Execute carregar_dados() primeiro.")
            return
        
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS BÁSICAS DE VENDAS")
        print("="*50)
        
        # Estatísticas gerais
        total_vendas = self.df['valor'].sum()
        media_vendas = self.df['valor'].mean()
        num_vendas = len(self.df)
        
        print(f"💰 Total de Vendas: R$ {total_vendas:,.2f}")
        print(f"📈 Média por Venda: R$ {media_vendas:,.2f}")
        print(f"🔢 Número de Vendas: {num_vendas}")
        
        # Top produtos
        print(f"\n🏆 TOP 3 PRODUTOS:")
        top_produtos = self.df.groupby('produto')['valor'].sum().sort_values(ascending=False).head(3)
        for i, (produto, valor) in enumerate(top_produtos.items(), 1):
            print(f"  {i}. {produto}: R$ {valor:,.2f}")
        
        # Top vendedores
        print(f"\n🏆 TOP 3 VENDEDORES:")
        top_vendedores = self.df.groupby('vendedor')['valor'].sum().sort_values(ascending=False).head(3)
        for i, (vendedor, valor) in enumerate(top_vendedores.items(), 1):
            print(f"  {i}. {vendedor}: R$ {valor:,.2f}")
    
    def gerar_visualizacoes(self) -> None:
        """Gera gráficos de análise das vendas."""
        if self.df is None:
            print("❌ Dados não carregados. Execute carregar_dados() primeiro.")
            return
        
        # Configuração do estilo
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Criar figura com subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('📊 Dashboard de Análise de Vendas', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Vendas por Produto
        vendas_produto = self.df.groupby('produto')['valor'].sum()
        ax1.bar(vendas_produto.index, vendas_produto.values, color='skyblue')
        ax1.set_title('💼 Vendas por Produto', fontweight='bold')
        ax1.set_xlabel('Produto')
        ax1.set_ylabel('Valor (R$)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Vendas por Região
        vendas_regiao = self.df.groupby('regiao')['valor'].sum()
        ax2.pie(vendas_regiao.values, labels=vendas_regiao.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title('🗺️ Distribuição por Região', fontweight='bold')
        
        # Gráfico 3: Vendas por Vendedor
        vendas_vendedor = self.df.groupby('vendedor')['valor'].sum().sort_values(ascending=True)
        ax3.barh(vendas_vendedor.index, vendas_vendedor.values, color='lightcoral')
        ax3.set_title('👥 Performance dos Vendedores', fontweight='bold')
        ax3.set_xlabel('Valor (R$)')
        
        # Gráfico 4: Tendência Temporal
        vendas_diarias = self.df.groupby('data')['valor'].sum()
        ax4.plot(vendas_diarias.index, vendas_diarias.values, marker='o', linewidth=2, markersize=6)
        ax4.set_title('📅 Tendência de Vendas no Tempo', fontweight='bold')
        ax4.set_xlabel('Data')
        ax4.set_ylabel('Valor (R$)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Salvar gráfico
        output_path = 'docs/dashboard_vendas.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📈 Dashboard salvo em: {output_path}")
        
        plt.show()


def main():
    """Função principal do programa."""
    print("🚀 Iniciando Análise de Vendas...")
    print("-" * 40)
    
    # Caminho para os dados
    data_path = os.path.join('data', 'vendas_sample.csv')
    
    # Criar instância do analisador
    analisador = AnalisadorVendas(data_path)
    
    # Executar análise
    if analisador.carregar_dados():
        analisador.estatisticas_basicas()
        
        # Perguntar se deseja gerar gráficos
        resposta = input("\n📊 Deseja gerar visualizações? (s/n): ").lower().strip()
        if resposta in ['s', 'sim', 'y', 'yes']:
            analisador.gerar_visualizacoes()
        
        print(f"\n✅ Análise concluída em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        print("❌ Falha na análise devido a problemas com os dados.")


if __name__ == "__main__":
    main()