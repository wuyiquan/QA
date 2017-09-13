#! /usr/env/bin python
# -*-coding: utf-8 -*-

import gensim

def get_vector(word,gensim_model):
    model = gensim.models.Word2Vec.load(gensim_model)
    vector = model[word]
    return vector
    
    
if __name__ == '__main__':
    word = u"白癜风长什么样"
    gensim_model = "word2vec.model"
    print get_vector(word,gensim_model)
    print len(get_vector(word,gensim_model))
    word = u"什么是白癜风"
    print get_vector(word,gensim_model)
    print len(get_vector(word,gensim_model))