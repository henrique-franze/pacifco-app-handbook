from gtts import gTTS
import os

texto_narracao = """Bem-vindo ao tutorial de como cadastrar um problema no App 4 Dev Pacífico.
Primeiro, acesse o portal e faça o login com seu e-mail e senha.
Após o carregamento, expanda o menu lateral, vá na seção Cadastros, clique em Modelos e depois selecione Problemas.
Na tela de problemas, clique no botão azul Adicionar no canto superior direito.
No formulário que se abrirá, preencha o campo obrigatório Nome. Se desejar, você também pode detalhar o problema nos campos opcionais de Descrição e Recomendação.
Para finalizar o cadastro, clique no botão Salvar."""

print("Gerando áudio com gTTS...")
tts = gTTS(text=texto_narracao, lang='pt', tld='com.br')
output_path = "./assets/narracao_cadastro_problema.mp3"
tts.save(output_path)
print(f"Áudio gerado com sucesso em {output_path}!")
