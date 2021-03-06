## SOURCE: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
import collections

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.pipeline import Pipeline


df1 = pd.read_csv('bot_comments.tsv', encoding='utf-8', sep='\t', index_col=0)
df2 = pd.read_csv('human_comments.tsv', encoding='utf-8', sep='\t', index_col=0)
df = pd.concat([df1, df2])
print(df.describe())
categories = ['human', 'bot']
def testing_code(input_list):
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(df.body)
    print(X_train_counts.shape)

    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    print(X_train_tf.shape)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print(X_train_tfidf.shape)

    clf = MultinomialNB().fit(X_train_tfidf, df.label)
    docs_new = ['Hello I am not a bot', "oh wow. this is a great idea! If I understand you correctly, it's sorta like how I would perform a sentiment analysis, but instead train it using bot comments?",
            "I am 99.91083% sure that cokelemon is not a bot."]

    X_new_counts = count_vect.transform(input_list)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)
    counter = collections.Counter(predicted)
    print(counter.most_common(1)[0][0])
    for doc, category in zip(input_list, predicted):
        print('%r => %s' % (doc, category))

def pipeline_cls(input_list):
    text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()), ])
    text_clf.fit(df.body, df.label)
    docs_test = input_list
    predicted = text_clf.predict(docs_test)
    #print(np.mean(predicted == df.label))
    counter = collections.Counter(predicted)
    print(counter.most_common(2))

