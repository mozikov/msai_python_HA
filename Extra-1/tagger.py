from abc import ABC, abstractmethod

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import pickle


class BaseTagger(ABC):
    @abstractmethod
    def get_tags(self, texts: list) -> list:
        """['Text1', 'Text2', ...] -> [['text1_tag1', 'text1_tag2', ...], ...]"""
        ...


class BaseChoiceTagger(BaseTagger, ABC):
    def __init__(self, tags: list):
        self.tags = tags


class SGDClassifierBuilder:
    '''
    This builder works with SGDClassifierTagger class. It fits (and opionally dumps)
    or loads classifier which needed for text tagging
    '''
    def __init__(self, tags: list, count_vect_path: str = None, tfidf_path: str = None, clf_path: str = None, dump=False):
        self.count_vect_path = count_vect_path
        self.tfidf_path = tfidf_path
        self.clf_path = clf_path
        self.tags = tags
        self.dump = dump

    def add_count_vect(self):
        
        self.count_vect = CountVectorizer()
        self.X_train_counts = self.count_vect.fit_transform(self.twenty_train.data)
        if self.dump:
            filename = 'count_vect.sav'
            pickle.dump(self.count_vect, open(filename, 'wb'))
        return self
    
    def add_tfidf_transformer(self):
        self.tfidf_transformer = TfidfTransformer()
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(self.X_train_counts)
        if self.dump:
            filename = 'tfidf_transformer.sav'
            pickle.dump(self.tfidf_transformer, open(filename, 'wb'))
        return self
    
    def add_clf(self):
        self.clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)
        self.clf.fit(self.X_train_tfidf, self.twenty_train.target)
        if self.dump:
            filename = 'clf.sav'
            pickle.dump(self.clf, open(filename, 'wb'))
        return self
    
    def build_clf(self):
        self.twenty_train = fetch_20newsgroups(subset='train', categories=self.tags, shuffle=True, random_state=42)
        if not self.count_vect_path:
            self.add_count_vect()
        else:
            self.count_vect = pickle.load(open(self.count_vect_path, 'rb'))

        if not self.tfidf_path:
            self.add_tfidf_transformer()
        else:
            self.tfidf_transformer = pickle.load(open(self.tfidf_path, 'rb'))

        if not self.clf_path:
            self.add_clf()
        else:
            self.clf = pickle.load(open(self.clf_path, 'rb'))
        return self


class SGDClassifierTagger(BaseChoiceTagger):
    """
    Text tagger based on sklearn. Able to build and dump or load pretrained models.
    Chooses tags from provided text list
    """
    default_tags_candidates = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

    def __init__(self, count_vect_path: str = None, tfidf_path: str = None, clf_path: str = None,  tags: list = None, dump = False):
        
        super().__init__(tags=tags or self.default_tags_candidates)
        self.count_vect_path = count_vect_path
        self.tfidf_path = tfidf_path
        self.clf_path = clf_path
        self.dump = dump

    def get_tags(self, texts: list) -> list:
        
        model = SGDClassifierBuilder(self.tags, self.count_vect_path, self.tfidf_path, self.clf_path, self.dump).build_clf()
        X_new_counts = model.count_vect.transform(texts)
        X_new_tfidf = model.tfidf_transformer.transform(X_new_counts)
        # TODO predict probability and filter by threshold
        predicted = model.clf.predict(X_new_tfidf)
        tags = [[model.twenty_train.target_names[category]] for category in predicted]
        return tags 


example = '''
In software engineering, a software design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into source or machine code. Rather, it is a description or template for how to solve a problem that can be used in many different situations. Design patterns are formalized best practices that the programmer can use to solve common problems when designing an application or system.
Object-oriented design patterns typically show relationships and interactions between classes or objects, without specifying the final application classes or objects that are involved. Patterns that imply mutable state may be unsuited for functional programming languages. Some patterns can be rendered unnecessary in languages that have built-in support for solving the problem they are trying to solve, and object-oriented patterns are not necessarily suitable for non-object-oriented languages.
Design patterns may be viewed as a structured approach to computer programming intermediate between the levels of a programming paradigm and a concrete algorithm.
'''

# test 1
print(SGDClassifierTagger(dump=True).get_tags([example]))
print(SGDClassifierTagger().get_tags(['God is love', 'OpenGL on the GPU is fast']))
# test 2
print(SGDClassifierTagger('count_vect.sav', 'tfidf_transformer.sav', 'clf.sav').get_tags([example]))
print(SGDClassifierTagger('count_vect.sav', 'tfidf_transformer.sav', 'clf.sav').get_tags(['God is love', 'OpenGL on the GPU is fast']))

# Output:
# [['comp.graphics']]
# [['soc.religion.christian'], ['comp.graphics']]
# The output is obviously the same for both tests, 
# but test 1 took 2.7 seconds, test 2 took only 0.8