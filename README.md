# 🎯 Grant Monitor

Sistema automatizado de monitoramento de oportunidades de financiamento para pesquisa em epidemiologia, saúde global e inteligência artificial para ciência.

[![GitHub](https://img.shields.io/badge/GitHub-fccoelho%2Fgrant--monitor-blue)](https://github.com/fccoelho/grant-monitor)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Portais Monitorados](#portais-monitorados)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Keywords Monitoradas](#keywords-monitoradas)
- [Roadmap](#roadmap)
- [Contribuição](#contribuição)

---

## 🎯 Visão Geral

O Grant Monitor é um sistema Python que automatiza a busca por editais de pesquisa em múltiplas agências de fomento. Ele:

- 🔍 Busca automaticamente novos editais
- 🗄️ Armazena oportunidades em banco de dados SQLite
- ⏰ Alerta sobre prazos próximos
- 🏷️ Filtra por keywords relevantes
- 🌍 Cobre portais do Brasil, Internacional e China

---

## 🌐 Portais Monitorados

### 🇧🇷 Brasil
| Portal | URL | Status |
|--------|-----|--------|
| FAPESP | https://fapesp.br/oportunidades/ | 🟡 Mock |
| CNPq | https://www.gov.br/cnpq/pt-br/edicitais | 🟡 Mock |
| FAPERJ | https://www.faperj.br/ | 🟡 Mock |
| FAPEMIG | https://fapemig.br/ | 🟡 Mock |

### 🌍 Internacional
| Portal | URL | Status |
|--------|-----|--------|
| NIH | https://grants.nih.gov/ | 🟡 Mock |
| Wellcome Trust | https://wellcome.org/grant-funding/ | 🟡 Mock |
| ERC | https://erc.europa.eu/ | 🟡 Mock |
| Gates Foundation | https://www.gatesfoundation.org/ | 🟡 Mock |

### 🇨🇳 China
| Portal | URL | Status |
|--------|-----|--------|
| NSFC | https://www.nsfc.gov.cn/english/ | 🟡 Mock |
| MOST | http://www.most.gov.cn/ | 🟡 Mock |
| CAS | https://www.cas.cn/ | 🟡 Mock |
| China Medical Board | https://www.chinamedicalboard.org/ | 🟡 Mock |

> 🟡 **Mock** = Implementação simulada (a ser substituída por scraping real)
> 🟢 **Live** = Implementação com scraping/API real

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/fccoelho/grant-monitor.git
cd grant-monitor

# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale dependências (quando houver)
pip install -r requirements.txt
```

---

## 💻 Uso

### Verificar todos os portais

```bash
python3 scripts/check_all.py --keywords "dengue,epidemiologia"
```

### Listar oportunidades armazenadas

```bash
# Todas as oportunidades
python3 scripts/list_grants.py

# Por portal específico
python3 scripts/list_grants.py --portal fapesp

# Com deadline próximo
python3 scripts/list_grants.py --days 30
```

### Verificar prazos

```bash
# Prazos nos próximos 30 dias
python3 scripts/check_deadlines.py --days 30
```

---

## 📁 Estrutura do Projeto

```
grant-monitor/
├── README.md                 # Este arquivo
├── SKILL.md                  # Documentação da skill
├── references/
│   ├── keywords.txt          # Keywords de busca (~65 termos)
│   └── database-schema.md    # Esquema do banco de dados
├── scripts/
│   ├── check_all.py          # Verifica todos os portais
│   ├── list_grants.py        # Lista oportunidades
│   ├── check_deadlines.py    # Alerta de prazos
│   └── grant_database.py     # Módulo de banco de dados
└── grants.db                 # Banco SQLite (criado automaticamente)
```

---

## 🏷️ Keywords Monitoradas

### Epidemiologia & Doenças
- dengue, epidemiologia, arboviroses
- zika, chikungunya, febre amarela, malária
- doenças infecciosas, vigilância epidemiológica
- transmissão de doenças

### Saúde Global
- global health, saúde global
- one health, planetary health
- saúde pública, public health
- digital health, mHealth, telemedicine

### AI for Science
- artificial intelligence, inteligência artificial
- AI for science, AI for health
- machine learning, deep learning
- computational biology, bioinformatics
- data science, predictive modeling

### Cooperação Internacional
- international cooperation, belt and road
- global south, south-south cooperation
- tropical diseases, emerging infectious diseases

> Veja o arquivo completo: [`references/keywords.txt`](references/keywords.txt)

---

## 🗺️ Roadmap

### Fase 1: Estrutura Base ✅
- [x] Sistema de banco de dados SQLite
- [x] Scripts de verificação
- [x] Lista de portais e keywords
- [x] Documentação inicial

### Fase 2: Scraping Brasil 🔄
- [ ] Implementar scraping FAPESP
- [ ] Implementar scraping CNPq
- [ ] Implementar scraping FAPERJ/FAPEMIG
- [ ] Testes e validação

### Fase 3: Scraping Internacional ⏳
- [ ] Implementar API NIH
- [ ] Implementar scraping Wellcome Trust
- [ ] Implementar ERC
- [ ] Gates Foundation

### Fase 4: Scraping China ⏳
- [ ] Implementar scraping NSFC
- [ ] Implementar scraping MOST
- [ ] Implementar CAS
- [ ] China Medical Board

### Fase 5: Automação ⏳
- [ ] Agendamento automático (cron)
- [ ] Notificações por email/Telegram
- [ ] Dashboard web
- [ ] Exportação para CSV/Excel

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**Flávio Codeço Coelho** - [@fccoelho](https://github.com/fccoelho)

Pesquisador em epidemiologia e saúde pública | Fiocruz

---

## 🙏 Agradecimentos

- Nanobot AI - Assistente de desenvolvimento
- Comunidade de código aberto

---

<p align="center">🚀 Boa caçada aos editais! 🎯</p>
