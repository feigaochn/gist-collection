# https://codesachin.wordpress.com/2015/10/15/generating-rudimentary-mind-maps-from-word2vec-models/

from gensim.parsing import PorterStemmer
from gensim.models import Word2Vec
from nltk.corpus import stopwords

global_stemmer = PorterStemmer()


class StemmingHelper(object):
    """
    Class to aid the stemming process - from word to stemmed form and vice versa.
    The 'original' form of a stemmed word will be returned as the form in which
    its been used the most number of times in the text.
    """

    # this reverse lookup will remember the original forms of the stemmed words
    word_lookup = {}

    @classmethod
    def stem(cls, word):
        """Stems a word and updates the reverse lookup."""
        # stem the word
        stemmed = global_stemmer.stem(word)
        # update the word lookup
        if stemmed not in cls.word_lookup:
            cls.word_lookup[stemmed] = {}
        cls.word_lookup[stemmed][word] = cls.word_lookup[stemmed].get(word, 0) + 1
        return stemmed

    @classmethod
    def original_form(cls, word):
        """Returns original form of a word given the stemmed version, as stored in the word_lookup."""
        if word in cls.word_lookup:
            return max(cls.word_lookup[word].keys(), key=lambda x: cls.word_lookup[word][x])
        else:
            return word


def test_Stemming():
    print(StemmingHelper.stem('learning'))
    print(StemmingHelper.original_form('learn'))
    print(StemmingHelper.stem('prediction-making'))


def get_content(title):
    # from wikipedia import page, search
    # content = page(search(title)[0]).content

    with open('log.txt') as f:
        content = f.read()

    return content


def pre_processing(text):
    clean = ' '
    for c in text:
        if c.isalnum():
            clean += c.lower()
        elif c == '.':
            clean += c
        else:
            if clean[-1] != ' ':
                clean += ' '
    print(clean)
    lineofwords = [line.split() for line in clean.split('.')]
    sentences = [[StemmingHelper.stem(w) for w in line if w not in stopwords.words('english')] for line in lineofwords]
    print(sentences)
    return sentences


def gen_model(sentences):
    # Word2Vec API param
    min_count, size, window = 2, 50, 4
    model = Word2Vec(sentences, min_count=min_count, size=size, window=window)

    # print(model['learn'])
    # print(model.most_similar(StemmingHelper.stem('classification')))
    # print(model.similarity(StemmingHelper.stem('classification'), StemmingHelper.stem('supervise')))
    # print(model.similarity('unsupervis', 'supervis'))
    return model


def _get_param_matrices(vocabulary, sentence_terms):
    """Returns
    ===
    1. Top 300 (or lesser, if vocab is short) most frequent terms (list)
    2. co-occurrence matrix wrt the most frequent terms (dict)
    3. Dict containing Pg of most-frequent terms (dict)
    4. nw (no of terms affected) of each term (dict)

    :type vocabulary: dict[str, int]
    :type sentence_terms: list[dict[str, double]]
    """
    # Figure out top n terms with respect to mere occurrences
    n = min(300, len(vocabulary))
    topterms = list(vocabulary.keys())
    topterms.sort(key=lambda x: vocabulary[x], reverse=True)
    topterms = topterms[:n]

    # nw maps term to the number of terms it 'affects'
    # (sum of number of terms in all sentences it appears in)
    nw = {}
    # co-occurrence values are wrt top terms only
    co_occur = {}
    # initially, co-occurrence matrix is empty
    for x in vocabulary:
        co_occur[x] = [0 for i in range(len(topterms))]

    # iterate over list of all sentences vocabulary dictioniaries
    # build the co-occurrence matrix
    for sentence in sentence_terms:
        total_terms = sum(list(sentence.values()))
        # this list contains the indices of all terms from topterms
        # that are present in this sentence
        top_indices = []
        # populate top_indices
        top_indices = [topterms.index(x) for x in sentence if x in topterms]
        # update nw dict, and co-occurrence matrix
        for term in sentence:
            nw[term] = nw.get(term, 0) + total_terms
            for index in top_indices:
                co_occur[term][index] += (sentence[term] * sentence[topterms[index]])
    # pg is just nw[term]/total vocabulary of text
    Pg = {}
    N = sum(list(vocabulary.values()))
    for x in topterms:
        Pg[x] = float(nw[x]) / N

    return topterms, co_occur, Pg, nw


def get_top_n_terms(vocabulary, sentence_terms, n=50):
    """Return the top 'n' terms from a block of text, in the form of a list, from most important to least.

    'vocabulary' should be a dict mapping each term to the number of its occurrences in the entire text.
    'sentence_terms' should be an interable of dicts, each denoting the vocabulary of the corresponding sentence.
    """
    # first compute the matrices
    topterms, co_occur, Pg, nw = _get_param_matrices(vocabulary, sentence_terms)
    # this dict will map each term to its weightage with respect to document
    result = {}
    N = sum(list(vocabulary.values()))
    # iterates over all terms in vocabulary
    for term in co_occur:
        term = str(term)
        org_term = str(term)
        for x in Pg:
            # expected_cooccur is the expected co-occurrence of term with this term
            # based on nw value of this and Pg value of the other
            expected_cooccur = nw[term] * Pg[x]
            # result measures the difference (in no. of terms) of expected co-occur and actual co-occur
            result[org_term] = (co_occur[term][topterms.index(x)] - expected_cooccur) ** 2 / float(expected_cooccur)
    terms = list(result.keys())
    terms.sort(key=lambda x: result[x], reverse=True)

    return terms[:n]


from scipy.spatial.distance import cosine
import networkx as nx


def build_mind_map(model, stemmer, root, nodes, alpha=0.2):
    """Returns the mindmap in the form of a NetworkX Graph instance.
    :param model: an instance of gensim.models.Word2Vec
    :param nodes: a list of terms, included in the vocabulary of 'model'
    :param root: node that is to be used as root of mindmap
    :param stemmer: an instance of StemmingHelper
    :return: the mind-map in the form of a NetworkX Graph instance
    """
    # this will be the mindmap
    g = nx.Graph()
    g = nx.DiGraph()

    # ensure that every node is in the vocabulary of model
    # and the root is included in the given nodes
    for node in nodes:
        if node not in model.vocab:
            raise ValueError(node + ' not in model vocabulary')
    if root not in nodes:
        raise ValueError('root not in nodes')

    ## containers for algorithm run
    # initially, all nodes are unvisited
    unvisited_nodes = set(nodes)
    visited_nodes = set()
    # map visited node to its contextual vector
    visited_node_vectors = {}
    # map unvisited nodes to (closest_distance, parent) where parent is a visited node
    node_distances = {}

    current_node = root
    visited_node_vectors[root] = model[root]
    unvisited_nodes.remove(root)
    visited_nodes.add(root)

    # build the mind-map in n-1 iterations
    for _ in range(len(nodes) - 1):
        # for every unvisited node 'x'
        for x in unvisited_nodes:
            # compute contextual distance between current node and x
            dist_from_current = cosine(visited_node_vectors[current_node], model[x])
            # get the leasts contextual distance to x found until now
            distance = node_distances.get(x, (100, ''))
            # if current node provides a shorter path to x, update x's distance and parent information
            if distance[0] > dist_from_current:
                node_distances[x] = (dist_from_current, current_node)
        # choose next 'current' as that unvisited node, which has the lowest
        # contextual distance from any of the visited nodes
        next_node = min(unvisited_nodes, key=lambda x: node_distances[x][0])
        # update all containers
        parent = node_distances[next_node][1]
        del node_distances[next_node]
        next_node_vect = (1 - alpha) * model[next_node] + alpha * visited_node_vectors[parent]
        visited_node_vectors[next_node] = next_node_vect
        unvisited_nodes.remove(next_node)
        visited_nodes.add(next_node)

        # add the link between newly selected node and its parent
        g.add_edge(stemmer.original_form(parent).capitalize(), stemmer.original_form(next_node).capitalize())

        # the new node becomes the current node for the next iteration
        current_node = next_node

    return g


def test_mindmap():
    sentences = pre_processing(get_content('Machine learning'))
    model = gen_model(sentences)
    print('model vocab', model.vocab.keys())
    g = build_mind_map(model, StemmingHelper(), 'learn', list(model.vocab.keys()))

    import matplotlib.pyplot as plt
    # plt.draw()
    nx.draw_networkx(g, prog='dot')
    plt.draw()


if __name__ == '__main__':
    # test_Stemming()
    # gen_model('')
    test_mindmap()
