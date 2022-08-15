import spacy
from dividir_oracoes_v2 import paths
from dividir_oracoes_v2 import reorder


def syntatic_analysis(x):
	pass

nlp = spacy.load("pt_core_news_lg")

# frase= 'O menino vê a mãe e a noiva casa de branco.'
frase= 'A noiva casa de branco e eu canto músicas.'
# frase= 'A menina conhece o menino que comprou um carro.' #[['A', 'menina', 'conhece', 'o', 'menino'], ['que', 'comprou', 'um', 'carro']]
# frase= 'O menino que comprou um carro escreveu um livro.'
# frase= 'O que o menino disse que a menina viu?'
# frase= 'Cuidado com o cão!'


doc = nlp(frase)
print('doc: ',doc)
for t in doc:
    print(t.text,': ',t.pos_,', ',t.dep_)

verb_count=0
subtrees=[]
lemma_list=["canto", "casa", "dúvida", "respeito", "como", "desejo", "morro", "fala", "ajuda", "volta", "compra"]
for t in doc:

    print('not filtered yet: ',t.text,' siblings: ',[r.text for r in t.rights])
    print('not filtered yet: ',t.text,' children: ',[c.text for c in t.children])
    print(t.text, ' class: ',t.pos_,', ',t.dep_)
    print([(c.text,c.pos_,c.dep_) for c in t.children])
    
    if t.pos_=="VERB" or (t.pos_=="ADJ" and t.dep_ == "conj") or (t.pos_=="ADJ" and t.dep_ in ("ccomp", "xcomp", "ROOT")) or (t.pos_ in ("NOUN") and t.dep_ in ("ccomp", "xcomp", "ROOT", "appos","conj") and t.lemma_ in lemma_list):
    # if t.pos_=="VERB" or (t.pos_=="AUX" and t.dep_ == "cop") or (t.pos_ in ("NOUN", "amod", "nmod") and t.dep_ == "ROOT" and t.lemma_ in lemma_list):
        print("Entered filter")
        verb_count+=1
        subtree=[t.text]

        #condicoes para eliminar irmao
        siblings=[r.text for r in t.rights 
                  if ( #Condicoes de similaridades para inclusao
                        (
                        (r.pos_=='VERB' and r.dep_ in ('advcl','acl:relcl','conj'))
                        )
                        #Condicoes de diferenças para inclusao
                       or(
                        (r.pos_!='ADJ') and r.dep_ in ("ccomp", "xcomp","conj") 
                        #caso 'O menino vê a mãe e a noiva casa de branco.'
                        or ((r.pos_!='ADJ') and r.dep_ in ("appos") and r.lemma_ in lemma_list)

                        or((r.pos_!='NOUN') and r.dep_ in ("ROOT","ccomp", "xcomp","conj"))
                       )
                       or r.pos_=='PUNCT'
                       # and (r.text not in lemma_list)
                     )]
        print(t.text,' siblings: ',siblings)
        print(t.text,' children: ',[c.text for c in t.children])
        paths(t,0,siblings,subtree,lemma_list)
        subtrees.append(subtree)
    print('*'*50)

print('subtrees')
#retirar pontuacao
filtered_subtrees=[]
for ora in subtrees:
    new_ora=[]
    for s in ora:
        if s not in ('.',',',';','!','?',':'):
            new_ora.append(s)
    filtered_subtrees.append(new_ora)
print(filtered_subtrees)

ordered_subtrees=reorder(doc,subtrees)
print(ordered_subtrees)


#Chamada principal 

if verb_count == 0:
    print('É uma frase')
else:
    #Analise sintatica em cada subtree
    for sub in ordered_subtrees:
        syntatic_analysis(sub)
