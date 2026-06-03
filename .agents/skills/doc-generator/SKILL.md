# Doc Generator Skill

Esta skill atua como orquestradora do nosso pipeline de documentação.
Ela junta as outras três skills (`webp-tools`, `tts-tools` e `video-tools`) em um único comando automatizado.

## Como Usar

O script principal está em `scripts/generate_doc.py`.

Ele recebe 3 parâmetros obrigatórios:
1. O caminho do roteiro `.txt`
2. O caminho do vídeo bruto `.webp`
3. O nome do arquivo MP4 final de saída.

### Exemplo
```bash
python .agents/skills/doc-generator/scripts/generate_doc.py assets/roteiro.txt assets/gravacao.webp assets/video_final.mp4
```

## O que ele faz por trás:
1. **TTS + Legendas**: Aciona a skill de TTS enviando o roteiro para a ElevenLabs. Ele gera o áudio MP3 e o SRT de legenda no mesmo local do script TXT.
2. **Merge**: Aciona a skill de edição de vídeo enviando o WebP, o áudio e a legenda para juntar tudo em um MP4 final pelo ffmpeg.
