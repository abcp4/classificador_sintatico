
import spacy


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
        if child.text in ancestrals_sibling:
            continue
        subtree.append(child.text)
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
                ancestrals_sibling.append(sibling.text)
        paths(child,c+1,ancestrals_sibling,subtree,lemma_list)


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
        words.append(t.text)
    # print('words: ',words)

    for i,w in enumerate(words):
        next_word=False
        for j,sub in enumerate(subtrees):
            if w in sub:
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


