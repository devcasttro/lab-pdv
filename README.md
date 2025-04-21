
# 🧾 LabPDV – Sistema de Ponto de Venda

**LabPDV** é um sistema moderno e modular de Ponto de Venda (PDV), desenvolvido com [Flet](https://flet.dev/) em Python, pensado para funcionar offline e com arquitetura escalável. Ele oferece recursos completos de vendas, estoque, relatórios e administração, com foco em facilidade de uso, segurança e performance.

---

## 🎯 Funcionalidades principais

- 🖥️ Interface local com Flet (desktop)
- 🌗 Tema claro/escuro com paleta personalizada
- 📦 Cadastro de produtos, unidades e categorias
- 🧾 Módulo PDV: vendas, descontos, parcelamento, recibo
- 🧑‍🤝‍🧑 Cadastro de clientes e fornecedores
- 📊 Relatórios de vendas, estoque e financeiro
- 🔄 Entrada e saída de estoque com histórico
- 🔐 Controle de permissões e níveis de acesso
- 🛡️ Sistema de assinatura/licença (offline e via painel)
- 📥 Exportação de recibos em PDF e opção de impressão
- 🔔 Notificações visuais com feedback e alertas
- 📏 Detecção automática de resolução de tela

---

## 🏗️ Estrutura do Projeto

```shell
labPDV/
├── app/
│   ├── main.py                  # Ponto de entrada da aplicação
│   ├── assets/                  # Logos, imagens e arquivos estáticos
│   ├── services/                # Lógica de tema, resolução, notificações
│   ├── views/                   # Telas e componentes
│   ├── models/                  # Modelos de dados
│   └── controllers/             # Regras de negócio
├── documentacao/
│   ├── index.html               # Documentação visual do projeto
│   ├── css/
│   ├── js/
│   └── assets/img/
├── requirements.txt            # Dependências
├── run_dev.bat                 # Execução Windows com hot reload
└── README.md
```

---

## 🚀 Como executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/labPDV.git
cd labPDV
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate  # Linux/macOS: source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
flet run --reload app/main.py
```

Ou use o script automático (Windows):

```bash
run_dev.bat
```

---

## 📌 Requisitos

- Python 3.10+
- [Flet](https://flet.dev/) 0.27+
- Windows (foco atual no modo desktop offline)

---

## 🔧 Roadmap Futuro

- [x] Tema dinâmico com paleta personalizada
- [x] Detecção de resolução automática
- [x] Sistema de backup manual e remoto
- [ ] Autenticação segura com login por usuário
- [ ] Controle de permissões avançadas
- [ ] Painel Administrativo Web (multiempresa)
- [ ] API REST para integração com app mobile
- [ ] Emissão de NFC-e + WhatsApp

---

## 📜 Histórico de Versões

### v1.0 - Abril 2024
- Módulo PDV
- Cadastro de produtos com margem e status
- Módulo de estoque com entradas/saídas
- Recibos e impressão local

### v1.1 - Abril 2024
- Contas a pagar e receber
- Vendas parceladas integradas com financeiro
- Relatórios de vendas e estoque

### v1.2 - Abril 2024
- Painel Administrativo Web
- Controle de licença e planos
- Backup remoto e gerenciamento de empresas
- Documentação oficial em HTML/SVG

### v1.3 - Previsto
- NFC-e e envio por WhatsApp
- App mobile Flet (Android)
- Login por permissão
- API pública para integração externa

---

## 👨‍💻 Autor

**Lucas Castro**  
🔗 Projeto mantido sob o selo **Lab do Analista**

---

## 📄 Licença

Este projeto é privado e licenciado para uso individual conforme definido por contrato.
