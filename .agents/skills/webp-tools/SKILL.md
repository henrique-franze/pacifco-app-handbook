# WebP Processor Skill

Esta skill capacita o agente a processar arquivos de vídeo WebP animado (como alterar a velocidade e aplicar compressão) usando a biblioteca `Pillow` do Python.

## Como Usar

O script principal está localizado em `scripts/process_webp.py`.

### Comandos de Exemplo

- **Acelerar e comprimir**:
  ```bash
  python .agents/skills/webp-tools/scripts/process_webp.py <input.webp> <output.webp> --speed 2.0 --quality 40
  ```

- **Apenas comprimir**:
  ```bash
  python .agents/skills/webp-tools/scripts/process_webp.py <input.webp> <output.webp> --quality 40
  ```

### Requisitos
- É necessário ter o `Pillow` instalado: `pip install Pillow`
