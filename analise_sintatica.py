import spacy
from sentence_split import sentence_split
from utils import get_num_verbs


def tem_sujeito(doc,nlp):
	sujeito = [t for t in doc if t.dep_ == "nsubj"]
	# Checando se tem sujeito. O código final vai ter várias subdivisões dos casos com sujeito e dos casos sem sujeito
	return sujeito

def syntatic_analysis(doc,nlp):
	if tem_sujeito(doc,nlp):
		print('frase: ',doc,' tem sujeito')

#Chamada principal 
frase='a casa caiu'
# frase='A noiva casa de branco e eu canto músicas.'
#Bugou denovo(Verificar)
# frase= 'O menino que comprou um carro escreveu um livro.'
nlp = spacy.load("pt_core_news_lg")

verb_count=get_num_verbs(frase,nlp)
print(verb_count)
if verb_count == 0:
	print('Trata-se de uma frase, não há análise sintática.')
elif verb_count == 1:
	print(frase)
	syntatic_analysis(nlp(frase),nlp)
else:
	oracoes=sentence_split(frase,nlp)
	for subfrase in oracoes:
		syntatic_analysis(subfrase,nlp)

