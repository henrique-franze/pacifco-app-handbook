# TTS Processor Skill

Esta skill utiliza a API da ElevenLabs para transformar textos (roteiros) em áudios incrivelmente naturais.
Ela lê as credenciais diretamente do arquivo `.env`.

## Como Usar

O script principal está localizado em `scripts/elevenlabs_tts.py`.

### Comandos de Exemplo

```bash
python .agents/skills/tts-tools/scripts/elevenlabs_tts.py caminho/para/o/texto.txt caminho/para/saida.mp3
```

Opcionalmente, você pode mudar o modelo de voz (o padrão é o super rápido e econômico `eleven_flash_v2_5`):
```bash
python .agents/skills/tts-tools/scripts/elevenlabs_tts.py texto.txt saida.mp3 --model eleven_multilingual_v2
```

### Requisitos
- Instalar bibliotecas: `pip install requests python-dotenv`
- Arquivo `.env` na raiz contendo `ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID`
