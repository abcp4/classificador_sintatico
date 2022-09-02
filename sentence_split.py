import spacy


#A busca recursiva não retorna as palavras de forma ordenada. Necessário ordena-las de acordo com a sentenca original
#O algoritmo é o seguinte: 
#1:Criar marcacoes para todas as palavras na mesma estrutura da subtrees
#2:Criar o ordered_subtree, que ira armazenar as subtrees ordenadas. Uma estrutura identica a subtrees
#3:Percorrer todas as palavras da sentenca, se a palavra estiver entre uma das subtrees
#  e a palavra daquela subtree não estiver com marcacao(ou seja, igual a 0), adicionamos ela a ordered_subtree
#Tomar cuidado com casos que envolvam simbolos presentes na sentenca e não na subtrees...Checar pra ver se existe potenciais bugs.

def reorder(doc,subtrees):
    words=[]
    marks=[]
    ordered_subtrees = [['' for j in range(len(subtrees[i]))] for i in range(len(subtrees))]
    marks = [[0 for j in range(len(subtrees[i]))] for i in range(len(subtrees))]
    for t in doc:
        words.append(t)
    # print('words: ',words)

    for i,w in enumerate(words):
        next_word=False
        for j,sub in enumerate(subtrees):
            if w in sub:#verificar se a comparacao de tokens e como a comparacao de textos
                for k,s in enumerate(subtrees[j]):
                    if marks[j][k]==0:
                        ordered_subtrees[j][k]=w
                        marks[j][k]=1
                        next_word=True
                        break
            if next_word:
                break

    # print('ordered_subtrees: ',ordered_subtrees)
    return ordered_subtrees


#Percorre recursivamente a arvore, ignorando todos os nós tios
#Problema 1: 'Joao viu a menina saindo'
#            'saindo' NÃO tem como filho a palavra 'menina'. As subtrees ficam só:
#             ['Joao','viu'] e ['saindo']
#             Em 'Joao viu a menina sair', 'sair' tem 'menina' como filho. Nesse caso,
#             as subtrees sao:
#             ['Joao','viu'] e ['menina','sair'] 
#Fix 1: 
def paths(t,c,ancestrals_sibling,subtree,lemma_list):
    children = t.children
    # if len([c for c in children])==0:
    #     if t.text not in ancestrals_sibling:
    #         subtree.append(t.text)

    for child in children:
        if child in ancestrals_sibling:
            continue
        subtree.append(child)
        for sibling in child.rights:
            print('ancestral: ',sibling.text,', pos: ',sibling.pos_,', dep: ',sibling.dep_)
            if (    #Condicoes de similaridades para inclusao
                    (
                    (sibling.pos_=='VERB' and sibling.dep_ in ('advcl','acl:relcl','conj'))
                        # or (sibling.pos_=='NOUN' and sibling.dep_=='obj')
                    )
                    #Condicoes de diferenças para inclusao
                    or ((sibling.pos_!='ADJ') and sibling.dep_ in ("ccomp", "xcomp","conj"))  
                    or ((sibling.pos_!='ADJ') and sibling.dep_ in ("appos") and sibling.lemma_ in lemma_list)
                    or ((sibling.pos_!='NOUN') and sibling.dep_ in ("ROOT","ccomp", "xcomp","conj"))
                    # and (sibling.text not in lemma_list)
                    or sibling.pos_=='PUNCT'
                ):
                print('added ancestral!')
                ancestrals_sibling.append(sibling)
        paths(child,c+1,ancestrals_sibling,subtree,lemma_list)

def sentence_split(frase,nlp):
    
    doc = nlp(frase)
    print('doc: ',doc)
    for t in doc:
        print(t.text,': ',t.pos_,', ',t.dep_)

    verb_count=0
    subtrees=[]
    lemma_list=["canto", "casa", "dúvida", "respeito", "como", "desejo", "morro", "fala", "ajuda"]
    for t in doc:

        print('not filtered yet: ',t.text,' siblings: ',[r.text for r in t.rights])
        print('not filtered yet: ',t.text,' children: ',[c.text for c in t.children])
        print(t.text, ' class: ',t.pos_,', ',t.dep_)
        print([(c.text,c.pos_,c.dep_) for c in t.children])
        
        if t.pos_=="VERB" or (t.pos_=="ADJ" and t.dep_ == "conj") or (t.pos_=="ADJ" and t.dep_ in ("ccomp", "xcomp", "ROOT")) or (t.pos_ in ("NOUN") and t.dep_ in ("ccomp", "xcomp", "ROOT", "appos","conj") and t.lemma_ in lemma_list):
        # if t.pos_=="VERB" or (t.pos_=="AUX" and t.dep_ == "cop") or (t.pos_ in ("NOUN", "amod", "nmod") and t.dep_ == "ROOT" and t.lemma_ in lemma_list):
            print("Entered filter")
            verb_count+=1
            subtree=[t]

            #condicoes para eliminar irmao
            siblings=[r for r in t.rights 
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
    print(subtrees)
    #retirar pontuacao
    filtered_subtrees=[]
    for oracao in subtrees:
        new_oracao=[]
        for s in oracao:
            if s.text not in ('.',',',';','!','?',':'):
                new_oracao.append(s)
        filtered_subtrees.append(new_oracao)
    print(filtered_subtrees)
    print(type(filtered_subtrees[0][0]))

    ordered_subtrees=reorder(doc,subtrees)
    print(ordered_subtrees)
    return ordered_subtrees


# # frase= 'O menino vê a mãe e a noiva casa de branco.'
# frase= 'A noiva casa de branco e eu canto músicas.'
# # frase= 'A menina conhece o menino que comprou um carro.' #[['A', 'menina', 'conhece', 'o', 'menino'], ['que', 'comprou', 'um', 'carro']]
# # frase= 'O menino que comprou um carro escreveu um livro.'
# # frase= 'O que o menino disse que a menina viu?'
# # frase= 'Cuidado com o cão!'
# nlp = spacy.load("pt_core_news_lg")

# sentence_split(frase,nlp)