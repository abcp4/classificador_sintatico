import spacy
from sentence_split import sentence_split
from utils import get_num_verbs
from analise_sujeito import analisa_sujeito

nlp = spacy.load("pt_core_news_lg")

def preprocess(texto):
    # (1) Colocando a primeira letra em minúscula por conta de algumas dificuldades do Spacy com palavras em maiúsculas
    # Ver o impacto que isso tem para nomes próprios (maria, pedro, são paulo, etc.)
    # texto = texto[0].lower() + texto[1:]

    ts = texto.split()

    # O Spacy trata casos como "precisa-se" como um todo, sem fazer a análise correta.
    # (2) O código abaixo separa o "-se" do verbo para a análise correta ("precisa se").

    for t in ts:
        if "-se" in t:
            texto = texto.replace("-se", " se")
    return texto



def processa(frase):

    #Chamada principal 
    # frase='a casa caiu'
    # frase='A noiva casa de branco e eu canto músicas.'
    # frase='vende-se uma casa'
    # frase='Ele fugiu e ela correu.'
    #Bugou denovo(Verificar)
    # frase= 'O menino que comprou um carro escreveu um livro.'

    frase=preprocess(frase)

    verb_count=get_num_verbs(frase,nlp)
    print(verb_count)
    return_message=''
    if verb_count == 0:
        return_message='Trata-se de uma frase, não há análise sintática.'
    elif verb_count == 1:
        return_message=analisa_sujeito(nlp(frase),nlp)
    else:
        oracoes=sentence_split(frase,nlp)
        for subfrase in oracoes:
            return_message+=analisa_sujeito(subfrase,nlp)+'\n'
    return return_message
