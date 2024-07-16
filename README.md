# Consultor Financeiro com Análise de Faturas

Este projeto é um consultor financeiro baseado em IA que oferece dicas sobre onde o usuário pode economizar. O objetivo é realizar a análise de faturas mensais de diferentes fontes, incluindo planilhas do Google Sheets, arquivos Excel, PDFs e dados de mercado.

## Funcionalidades

### Funcionalidades em Andamento

- **Análise de Faturas**: Analisa faturas mensais e fornece conselhos financeiros detalhados.
- **Suporte para Diferentes Fontes**: Suporta a análise de faturas a partir de Google Sheets, arquivos Excel e PDFs.
- **Informações de Mercado**: Analisa ações e fornece conselhos de posição no mercado.

### Funcionalidades Implementadas

- **Integração com o Banco Central**: Utiliza dados atualizados do Banco Central do Brasil para enriquecer os conselhos financeiros.

## Requisitos

- Python 3.6 ou superior
- Conta no Google Cloud com credenciais para acessar a API do Google Sheets
- Chave API para Google Generative AI (`gemini-pro`)

## Instalação

### Passo 1: Instalar Docker

Baixar e instalar Docker através do link [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Passo 2: Instalar Extensão Docker no VSCode

Instalar a extensão Docker no VSCode para facilitar o gerenciamento do container.

### Passo 3: Clonar o Repositório

Clonar o repositório do projeto para sua máquina local:

```bash
git clone https://github.com/Lucas28reis/agente_financeiro.git
cd agente_financeiro
