# Pacifco App4Dev - Handbook

Bem-vindo ao repositório de documentação do portal App4Dev Pacifco. 

Este projeto tem o objetivo de centralizar e automatizar a geração de tutoriais, guias e manuais para os usuários finais do sistema, mantendo um padrão visual consistente com a marca.

## Estrutura Atual
- `tutorial_cadastro_problema.md`: Passo a passo de como cadastrar um problema.
- `assets/`: Imagens e vídeos de demonstração utilizados nos tutoriais.
- `.agents/skills/`: Scripts e automações utilizadas para melhorar os arquivos, como processamento de vídeo WebP.

---

## TO-DO List e Próximos Passos

Aqui estão as próximas melhorias mapeadas para o projeto:

- [ ] **Edição de Vídeo (Corte)**: Criar uma skill (script) capaz de cortar a parte inicial dos vídeos, removendo a etapa de login, para ir direto ao ponto.
- [ ] **Ajuste de Aceleração**: Testar velocidades maiores que 2x (ex: 3x ou 4x) para deixar os vídeos WebP ainda mais rápidos e objetivos.
- [ ] **Roteirização**: Gerar os scripts de texto (narração) detalhando cada passo a ser falado nos tutoriais em vídeo.
- [ ] **Geração de Áudio (TTS)**: Incorporar uma solução de Text-to-Speech para narrar os tutoriais usando voz sintetizada.
- [ ] **Deploy em Site Estático**: Publicar esta documentação em uma página navegável na web (usando ferramentas como MkDocs ou Docusaurus via GitHub Pages).
- [ ] **Geração Automática de PDFs**: Criar um script para exportar os tutoriais `.md` formatados em PDF para envio offline.

## Sugestão Prática para Text-to-Speech (TTS)

Para gerar a narração de forma prática e com alta qualidade (item 4):
1. **gTTS (Google TTS)**: A opção mais fácil e **gratuita** para começar. Podemos fazer um script simples em Python usando a biblioteca `gTTS` que lê o texto e cospe um arquivo `.mp3`.
2. **OpenAI TTS API**: Se quiser uma voz absurdamente natural e humana, usar a API da OpenAI (modelo `tts-1`) ou ElevenLabs é o melhor caminho. O custo é baixíssimo por minuto de áudio e podemos criar uma "skill" do agente para rodar isso com um comando.
3. **Local (MacOS)**: Se quiser apenas rascunhar sem internet, podemos usar o comando nativo `say` do Mac.

Recomendo começarmos criando uma skill com o **gTTS** (gratuito) para testar o fluxo e, se precisarmos de qualidade premium, mudamos para a **OpenAI**.
