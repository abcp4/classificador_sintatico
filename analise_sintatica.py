import spacy
from sentence_split import sentence_split
from utils import get_num_verbs
from analise_sujeito import analisa_sujeito




#Chamada principal 
# frase='a casa caiu'
frase='A noiva casa de branco e eu canto músicas.'
#Bugou denovo(Verificar)
# frase= 'O menino que comprou um carro escreveu um livro.'
nlp = spacy.load("pt_core_news_lg")

verb_count=get_num_verbs(frase,nlp)
print(verb_count)
if verb_count == 0:
	print('Trata-se de uma frase, não há análise sintática.')
elif verb_count == 1:
	print(frase)
	analisa_sujeito(nlp(frase),nlp)
else:
	oracoes=sentence_split(frase,nlp)
	for subfrase in oracoes:
		analisa_sujeito(subfrase,nlp)

