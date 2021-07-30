from collections import Counter

from torchtext.vocab import Vocab

from doctypes import Document, LanguageModel, TokenizedDocument
from util import test, test_search


def test_process_docs():
    import process_docs

    def test_preprocess_docs():
        test(process_docs.preprocess_docs,
             [TokenizedDocument(0, ['kirkuk', 'seized'], ['iraq', 'takes', 'kirkuk'])],
             [Document(0, 'Kirkuk seized', 'Iraq takes over Kirkuk')])
    test_preprocess_docs()

    def test_create_language_models():
        test(process_docs.create_language_models,
             [LanguageModel(0, Counter('abcdef'), 13, 1)],
             [TokenizedDocument(0, list('abc'), list('def'))],
             Vocab(Counter('abbbccdeefggg'), specials=[]),
             1)
    test_create_language_models()

    def test_create_collection_model():
        test(process_docs.create_collection_model,
             LanguageModel(None, Counter('aabbccdee'), 24, 3),
             [LanguageModel(0, Counter('abc'), 8, 1),
              LanguageModel(1, Counter('cde'), 8, 1),
              LanguageModel(2, Counter('aeb'), 8, 1)])
    test_create_collection_model()

    def test_create_vocab():
        test(process_docs.create_vocab,
             lambda vocab: (vocab.freqs, Counter('aaabbbcccddddeee')),
             [TokenizedDocument(0, list('cd'), list('ab')),
              TokenizedDocument(1, list('bc'), list('ed')),
              TokenizedDocument(2, list('ad'), list('eb')),
              TokenizedDocument(3, list('da'), list('ec'))])
    test_create_vocab()

    def test_create_inverted_index():
        test(process_docs.create_inverted_index,
             {'a': [0, 2, 3],
              'b': [0, 1, 2],
              'c': [0, 1, 3],
              'd': [0, 1, 2, 3],
              'e': [1, 2, 3]},
             [TokenizedDocument(0, list('cd'), list('ab')),
              TokenizedDocument(1, list('bc'), list('ed')),
              TokenizedDocument(2, list('ad'), list('eb')),
              TokenizedDocument(3, list('da'), list('ec'))],
             Vocab(Counter('aaabbbcccddddeee'), specials=[]))
    test_create_inverted_index()


def test_ranker():
    import ranker

    def test_calculate_precision_at_k():
        test(ranker.calculate_precision_at_k,
             0.5,
             [1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
             10)
    test_calculate_precision_at_k()

    def test_calculate_average_precision():
        test(ranker.calculate_average_precision,
             0.78333333333333333,
             [1, 1, 0, 1, 0, 1, 0, 0, 0, 1])
    test_calculate_average_precision()

    def test_calculate_mean_average_precision():
        test(ranker.calculate_mean_average_precision,
             0.5833333333333333,
             [[1, 1, 0, 1], [0, 1, 0], [0, 0, 1]])
    test_calculate_mean_average_precision()

    def test_calculate_dcg_at_k():
        test(ranker.calculate_dcg_at_k,
             9.6051177391888114,
             [3, 2, 3, 0, 0, 1, 2, 2, 3, 0],
             10)
    test_calculate_dcg_at_k()

    def test_calculate_ndcg_at_k():
        test(ranker.calculate_ndcg_at_k,
             0.9203032077642922,
             [2, 1, 2, 0],
             4)
    test_calculate_ndcg_at_k()

    def test_calculate_jaccard_similarity():
        test(ranker.calculate_jaccard_similarity,
             0.25,
             list('abcde'),
             list('bdfhj'))
    test_calculate_jaccard_similarity()

    def test_calculate_word_probability():
        test(ranker.calculate_word_probability,
             0.06666666666666667,
             LanguageModel(0, Counter('abbcccdddd'), 15, 1),
             'e',
             False)
    test_calculate_word_probability()

    def test_calculate_sentence_probability():
        test(ranker.calculate_sentence_probability,
             0.0044444444444444444,
             LanguageModel(0, Counter('abbcccdddd'), 15, 1),
             list('bde'),
             False)
    test_calculate_sentence_probability()

    def test_calculate_interpolated_sentence_probability():
        test(ranker.calculate_interpolated_sentence_probability,
             0.005890000000000001,
             LanguageModel(0, Counter('abbcccdddd'), 15, 1),
             LanguageModel(None, Counter('abbcccccddddeee'), 25, 2),
             list('bde'),
             0.75,
             False)
    test_calculate_interpolated_sentence_probability()

    def test_calculate_tf():
        test(ranker.calculate_tf,
             Counter('abcddefg'),
             TokenizedDocument(0, list('abcd'), list('defg')))
    test_calculate_tf()

    def test_calculate_df():
        test(ranker.calculate_df,
             Counter('abbcccdde'),
             [TokenizedDocument(0, list('abc'), list('baa')),
              TokenizedDocument(1, list('bcd'), list('dbd')),
              TokenizedDocument(2, list('cde'), list('eec'))])
    test_calculate_df()

    def test_calculate_idf():
        test(ranker.calculate_idf,
             {'a': 1.0986122886681098,
              'b': 0.4054651081081644,
              'c': 0.0,
              'd': 0.4054651081081644,
              'e': 1.0986122886681098},
             Counter('abbcccdde'),
             3)
    test_calculate_idf()

    def test_calculate_bm25():
        test(ranker.calculate_bm25,
             [(2, 1.0986122886681098),
              (0, 0.4054651081081644),
              (1, 0.4054651081081644)],
             list('bce'),
             [TokenizedDocument(0, list('a'), list('bc')),
              TokenizedDocument(1, list('b'), list('cd')),
              TokenizedDocument(2, list('c'), list('de'))],
             1.2,
             0.75)
    test_calculate_bm25()


def test_searcher():
    import searcher

    def test_bm25_search():
        test_search(searcher.bm25_search,
                    test_data_path='files/test_queries.csv',
                    processed_data_path='files/test_data_processed.pickle',
                    raw_data_path='files/test_data.csv',
                    verbose=False, topk=10)
    test_bm25_search()

    def test_qlm_search():
        test_search(searcher.qlm_search,
                    test_data_path='files/test_queries.csv',
                    processed_data_path='files/test_data_processed.pickle',
                    raw_data_path='files/test_data.csv',
                    verbose=False, topk=10)
    test_qlm_search()

    def test_ranknet_lstm_search():
        test_search(searcher.ranknet_lstm_search,
                    test_data_path='files/test_queries.csv',
                    processed_data_path='files/test_data_processed.pickle',
                    raw_data_path='files/test_data.csv',
                    verbose=False, model_path='files/ranknet_lstm.pt',
                    topk=10, max_query_len=50, max_doc_len=200)
    test_ranknet_lstm_search()


def test_util():
    import util

    def test_clean_words():
        test(util.clean_words,
             ['3', 'kill', 'islam', 'milit', 'attack', 'town'],
             '3 killed as Islamic militants attack town',
             True)
    test_clean_words()

    def test_get_doc():
        test(util.get_doc,
             lambda doc: (doc.id, 315201),
             315201,
             'files/test_data.csv')
    test_get_doc()


if __name__ == '__main__':
    test_process_docs()
    test_ranker()
    test_searcher()
    test_util()