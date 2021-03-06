import numpy as np
from bert_serving.client import BertClient
bc = BertClient()
prefix_q = '##### **Q:** '
with open('README.md') as fp:
    questions = [v.replace(prefix_q, '').strip()
                 for v in fp if v.strip() and v.startswith(prefix_q)]
    print(questions)
    print('%d questions loaded, avg. len of %d' %
          (len(questions), np.mean([len(d.split()) for d in questions])))
doc_vecs = bc.encode(questions)
test = ["Do you have a paper or other written explanation to introduce your model's details?",
        'Where is the BERT code come from?', 'How large is a sentence vector?',
        'How do you get the fixed representation? Did you do pooling or something?',
        'Are you suggesting using BERT without fine-tuning?',
        'Can I get a concatenation of several layers instead of a single layer ?',
        'What are the available pooling strategies?',
        'Why not use the hidden state of the first token as default strategy, i.e. the `[CLS]`?', 'BERT has 12/24 layers, so which layer are you talking about?', 'Why not the last hidden layer? Why second-to-last?',
        'So which layer and which pooling strategy is the best?', 'Could I use other pooling techniques?',
        'Do I need to batch the data before `encode()`?', 'Can I start multiple clients and send requests to one server simultaneously?',
        'How many requests can one service handle concurrently?', 'So one request means one sentence?',
        'How about the speed? Is it fast enough for production?', 'Did you benchmark the efficiency?',
        'What is backend based on?', 'What is the parallel processing model behind the scene?',
        'Why does the server need two ports?', 'Do I need Tensorflow on the client side?',
        'Can I use multilingual BERT model provided by Google?', 'Can I use my own fine-tuned BERT model?',
        'Can I run it in python 2?',
        'Do I need to do segmentation for Chinese?',
        'Why my (English) word is tokenized to `##something`?',
        'Can I use my own tokenizer?',
        'I encounter `zmq.error.ZMQError: Operation cannot be accomplished in current state` when using `BertClient`, what should I do?',
        'After running the server, I have several garbage `tmpXXXX` folders. How can I change this behavior ?',
        "The cosine similarity of two sentence vectors is unreasonably high (e.g. always > 0.8), what's wrong?",
        "I'm getting bad performance, what should I do?", 'Can I run the server side on CPU-only machine?',
        'How can I choose `num_worker`?', 'Can I specify which GPU to use?']
carrray = []
for qn in test:
    query = qn
    print('Question:', qn)
    query_vec = bc.encode([query])[0]
    print('Encoding Question')
    # compute normalized dot product as score
    score = np.sum(query_vec * doc_vecs, axis=1) / \
        np.linalg.norm(doc_vecs, axis=1)
    print('Encoding done, Calculating Score...')
    topk_idx = np.argsort(score)[::-1][:1]
    for idx in topk_idx:
        correctness = round(score[idx] * 7, ndigits=2)
        carrray.append(correctness)
        print('> %s\t%s' % (correctness, qn))
print(min(carrray), max(carrray), sum(carrray)/len(carrray))
