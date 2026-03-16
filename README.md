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
- [Scrapers](#scrapers)
- [Keywords Monitoradas](#keywords-monitoradas)
- [Roadmap](#roadmap)
- [Contribuição](#contribuição)

---

## 🎯 Visão Geral

O Grant Monitor é um sistema Python que automatiza a busca por editais de pesquisa em múltiplas agências de fomento. Ele:

- 🔍 **Scraping automatizado**: Busca em 11+ portais simultaneamente
- 🗄️ **Persistência**: Armazena oportunidades em banco de dados SQLite
- ⏰ **Alertas de prazo**: Notifica sobre deadlines próximos
- 🏷️ **Filtragem inteligente**: Busca por 65+ keywords relevantes
- 🌍 **Cobertura global**: Brasil, Europa, EUA e China

---

## 🌐 Portais Monitorados

### 🇧🇷 Brasil
| Portal | URL | Status | Tecnologia |
|--------|-----|--------|------------|
| **FAPESP** | https://fapesp.br/oportunidades/ | 🟢 Live | BeautifulSoup |
| **CNPq** | https://www.gov.br/cnpq/pt-br/edicitais | 🟢 Live | BeautifulSoup |
| **FAPERJ** | https://www.faperj.br/ | 🟢 Live | BeautifulSoup |
| **FAPEMIG** | https://fapemig.br/ | 🟢 Live | BeautifulSoup |

### 🌍 Internacional
| Portal | URL | Status | Tecnologia |
|--------|-----|--------|------------|
| **NIH** | https://grants.nih.gov/ | 🟢 Live | BeautifulSoup |
| **Wellcome Trust** | https://wellcome.org/grant-funding/ | 🟢 Live | BeautifulSoup |
| **ERC** | https://erc.europa.eu/ | 🟢 Live | BeautifulSoup |
| **Gates Foundation** | https://www.gatesfoundation.org/ | 🟢 Live | BeautifulSoup |

### 🇨🇳 China
| Portal | URL | Status | Tecnologia |
|--------|-----|--------|------------|
| **NSFC** | https://www.nsfc.gov.cn/english/ | 🟢 Live | BeautifulSoup |
| **MOST** | http://www.most.gov.cn/ | 🟢 Live | BeautifulSoup |
| **CAS** | https://www.cas.cn/ | 🟢 Live | BeautifulSoup |
| **China Medical Board** | https://www.chinamedicalboard.org/ | 🟢 Live | BeautifulSoup |

> 🟢 **Live** = Implementação com scraping real
> 🟡 **Beta** = Implementação inicial, pode precisar de ajustes

---

## 🚀 Instalação

### Via pip (recomendado)

```bash
# Clone o repositório
git clone https://github.com/fccoelho/grant-monitor.git
cd grant-monitor

# Instale com pip (usa pyproject.toml)
pip install -e .

# Ou com uv (mais rápido)
uv pip install -e .
```

### Ambiente virtual (opcional)

```bash
# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale no modo de desenvolvimento
pip install -e ".[dev]"
```

### Dependências
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser
- `python-dateutil` - Date parsing

---

## 💻 Uso

### Verificar todos os portais

```bash
# Busca padrão (dengue, epidemiologia, global health)
python3 scripts/check_all.py

# Busca com keywords específicas
python3 scripts/check_all.py --keywords "machine learning, saúde digital"

# Ver apenas portais específicos
python3 scripts/check_all.py --portals FAPESP,NIH

# Modo verbose (mostra detalhes de cada oportunidade)
python3 scripts/check_all.py --verbose

# Salvar no banco de dados
python3 scripts/check_all.py --save

# Exportar para JSON
python3 scripts/check_all.py --output grants.json
```

### Listar oportunidades armazenadas

```bash
# Todas as oportunidades
python3 scripts/list_grants.py

# Por portal específico
python3 scripts/list_grants.py --portal fapesp

# Com deadline próximo (30 dias)
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
├── LICENSE                   # Licença MIT
├── pyproject.toml            # Configuração do projeto
├── SKILL.md                  # Documentação da skill
├── references/
│   ├── keywords.txt          # Keywords de busca (~65 termos)
│   └── database-schema.md    # Esquema do banco de dados
├── scripts/
│   ├── check_all.py          # Script principal de verificação
│   ├── list_grants.py        # Lista oportunidades
│   ├── check_deadlines.py    # Alerta de prazos
│   ├── grant_database.py     # Módulo de banco de dados
│   └── scrapers/             # Módulo de scrapers
│       ├── __init__.py       # Inicialização e exports
│       ├── base.py           # Classe base e modelos
│       ├── brazil.py         # Scrapers brasileiros
│       ├── international.py  # Scrapers internacionais
│       └── china.py          # Scrapers chineses
└── grants.db                 # Banco SQLite (criado automaticamente)
```

---

## 🕷️ Scrapers

### Arquitetura

Cada scraper herda da classe `BaseScraper` e implementa o método `search(keywords)`:

```python
from scrapers import FAPESPScraper

scraper = FAPESPScraper()
results = scraper.search(["dengue", "epidemiologia"])

for grant in results:
    print(f"{grant.title} - {grant.agency}")
```

### Classes de Scraper

| Classe | Portal | País |
|--------|--------|------|
| `FAPESPScraper` | FAPESP | 🇧🇷 BR |
| `CNPqScraper` | CNPq | 🇧🇷 BR |
| `FAPERJScraper` | FAPERJ | 🇧🇷 BR |
| `FAPEMIGScraper` | FAPEMIG | 🇧🇷 BR |
| `NIHScraper` | NIH | 🇺🇸 US |
| `WellcomeScraper` | Wellcome Trust | 🇬🇧 UK |
| `ERCScraper` | ERC | 🇪🇺 EU |
| `GatesScraper` | Gates Foundation | 🇺🇸 US |
| `NSFCScraper` | NSFC | 🇨🇳 CN |
| `MOSTScraper` | MOST | 🇨🇳 CN |
| `CASScraper` | CAS | 🇨🇳 CN |
| `ChinaMedicalBoardScraper` | China Medical Board | 🇺🇸 US |

### Implementando um Novo Scraper

```python
from scrapers.base import BaseScraper, GrantOpportunity

class NewAgencyScraper(BaseScraper):
    BASE_URL = "https://agency.org/funding"
    
    def search(self, keywords):
        soup = self.fetch_page(self.BASE_URL)
        opportunities = []
        
        # Parse the page
        for item in soup.find_all('div', class_='grant'):
            title = item.find('h2').get_text()
            
            # Check if matches keywords
            matched = self.matches_keywords(title, keywords)
            if matched:
                opportunities.append(GrantOpportunity(
                    title=title,
                    agency='New Agency',
                    description=...,
                    url=...,
                    keywords=matched,
                    country='BR',
                ))
        
        return opportunities
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

### Fase 2: Scraping Brasil ✅
- [x] Implementar scraping FAPESP
- [x] Implementar scraping CNPq
- [x] Implementar scraping FAPERJ
- [x] Implementar scraping FAPEMIG

### Fase 3: Scraping Internacional ✅
- [x] Implementar API/scraping NIH
- [x] Implementar scraping Wellcome Trust
- [x] Implementar ERC
- [x] Gates Foundation

### Fase 4: Scraping China ✅
- [x] Implementar scraping NSFC
- [x] Implementar scraping MOST
- [x] Implementar CAS
- [x] China Medical Board

### Fase 5: Aprimoramentos 🔄
- [ ] Rate limiting e retry logic
- [ ] Selenium/Playwright para sites JavaScript-heavy
- [ ] Validação e testes automatizados
- [ ] Docker containerization

### Fase 6: Automação ⏳
- [ ] Agendamento automático (cron)
- [ ] Notificações por email/Telegram
- [ ] Dashboard web
- [ ] Exportação para CSV/Excel
- [ ] API REST

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Guidelines
- Siga PEP 8 para código Python
- Adicione docstrings às funções
- Inclua testes quando possível
- Documente novos scrapers no README

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
