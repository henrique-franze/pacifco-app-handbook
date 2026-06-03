# Pacifco App Handbook - Pipeline de Geração de Documentação

Este documento explica como o pipeline automatizado de geração de tutoriais funciona para o Pacifco App.

## Arquitetura das Skills

Para que a documentação de funcionalidades seja reprodutível, o pipeline foi dividido em diversas **Skills**:

### 1. `webp-tools`
Processa e edita vídeos em formato `.webp` que são extraídos diretamente do navegador. Pode acelerar o tempo do vídeo (time-lapse) e prepará-lo para a união com o áudio.

### 2. `tts-tools` (ElevenLabs)
Lê o roteiro (`.txt`) da documentação e bate na API da ElevenLabs para gerar uma narração realista.
- **Configuração:** O Voice ID deve estar no arquivo público `config.json`, e a sua Chave da API no arquivo privado `.env`.
- **Inovação:** Ele extrai os *timestamps* precisos por palavra diretamente do JSON da ElevenLabs e gera automaticamente um arquivo `.srt` de legendas no mesmo momento em que cria o `.mp3`.

### 3. `video-tools`
É o responsável pela montagem final. Usando Python + Pillow + ffmpeg, esse script:
1. Extrai todos os frames do WebP animado.
2. Calcula o framerate original.
3. Monta um arquivo de vídeo puro com codec `h264`.
4. Embuti o áudio da narração (`.mp3`).
5. Embuti as legendas geradas como *soft subtitles* (formato `mov_text`).
6. Exporta tudo para o `.mp4` final.

### 4. `doc-generator` (O Maestro)
Um orquestrador em Python que recebe o arquivo do roteiro e o vídeo webp bruto, e chama sequencialmente todas as ferramentas acima até entregar o vídeo MP4 renderizado na pasta `assets` e o template do Markdown preenchido com as mídias!

## Variáveis de Ambiente Necessárias (`.env`)

Copie o `.env.example` para `.env` e preencha as variáveis de ambiente com as chaves corretas:
```env
ELEVENLABS_API_KEY=sua_chave_aqui
PACIFCO_USERNAME=seu_usuario
PACIFCO_PASSWORD=sua_senha
```
