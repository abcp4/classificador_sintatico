"""
Esse arquivo cumpre a função do código de divisão do texto em orações, ou seja,
gera um 'doc' de uma oração.
As ações (1) e (2) devem ser incorporadas na versão final.
"""
import spacy

nlp = spacy.load("pt_core_news_lg")
texto = "Maria gosta de Pedro."
# (1) Colocando a primeira letra em minúscula por conta de algumas dificuldades do Spacy com palavras em maiúsculas
# Ver o impacto que isso tem para nomes próprios (maria, pedro, são paulo, etc.)
texto = texto[0].lower() + texto[1:]

ts = texto.split()

# O Spacy trata casos como "precisa-se" como um todo, sem fazer a análise correta.
# (2) O código abaixo separa o "-se" do verbo para a análise correta ("precisa se").

for t in ts:
    if "-se" in t:
        texto = texto.replace("-se", " se")

texto_doc = nlp(texto)
