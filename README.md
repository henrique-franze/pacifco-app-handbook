# Pacifco App4Dev - Handbook

Bem-vindo ao repositório de documentação do portal App4Dev Pacifco. 

Este projeto tem o objetivo de centralizar e automatizar a geração de tutoriais, guias e manuais para os usuários finais do sistema, mantendo um padrão visual consistente com a marca.

## Estrutura Atual
- `tutorial_cadastro_problema.md`: Passo a passo de como cadastrar um problema.
- `assets/`: Imagens e vídeos de demonstração utilizados nos tutoriais.
- `.agents/skills/`: Scripts e automações utilizadas para melhorar os arquivos, como processamento de vídeo WebP.

---

## Arquitetura e Pipeline
Toda a arquitetura das automações, incluindo geração de voz (ElevenLabs), edição de vídeo WebP e embutimento de legendas via ffmpeg/Pillow, está documentada no arquivo principal de arquitetura:
👉 **[PIPELINE.md](PIPELINE.md)**

Para gerar os vídeos, existe um orquestrador mestre (`doc-generator`). Antes de executá-lo, instale as dependências:
```bash
pip install -r requirements.txt
```

---

## TO-DO List (Próximas Versões)

Aqui estão as próximas melhorias mapeadas para o projeto:
- [ ] **Deploy em Site Estático**: Publicar esta documentação em uma página navegável na web (usando ferramentas como MkDocs ou Docusaurus via GitHub Pages).
- [ ] **Geração Automática de PDFs**: Criar um script para exportar os tutoriais `.md` formatados em PDF para envio offline.
