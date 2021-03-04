#I didn't actually end up using anything from this file, this was mainly a bunch of experiments
#and functions that I didn't end up using.

standard_file = "s_out.txt"
first_per = ['we','i']

def highlight(oldfile, newfile = standard_file):
	with open(newfile, 'w') as outfile, open(oldfile, 'r', encoding='utf-8') as infile:
		for line in infile:
			print(line, end = '')
			words = line.split()
			for word in words:
				if word in first_per:
					outfile.write("*******")
				else:
					outfile.write(word +" ")

#highlight("scitext.txt")

#personal pronouns
#put verbs in past tense
#basic spelling/grammar
#anecdotes?
#subjectivity
#superlatives:  "huge," "incredible," "wonderful," "exciting,"
#assumption vs. deduction
#citations? years 1500 - 2021, suggest a paper being cited


class ObjectivityDetector():
    '''SVM predicts the objectivity/subjectivity of a sentence. Trained on pang/lee 2004 with NER removal. Pre-grid searched and 5 fold validated and has a 90% accuracy and 0.89 F1 macro'''
    def __init__(self,train,model_file=None):
        self.pipeline = Pipeline(
            [
                ('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', CalibratedClassifierCV( #calibrated CV wrapping SGD to get probability outputs
                        SGDClassifier(
                        loss='hinge',
                        penalty='l2',
                        alpha=1e-4,
                        max_iter=1000,
                        learning_rate='optimal',
                        tol=None,),
                    cv=5)),
            ]
        )
        self.train(train)

    def train(self,train):
        learner = self.pipeline.fit(train['text'],train['truth'])
        self.learner = learner

    def predict(self,test):
        predicted = self.learner.predict(test)
        probs = self.learner.predict_proba(test)
        certainty = certainty_(probs)
        return predicted,certainty

    def score(self,predicted,test):
        acc = accuracy_score(test['truth'].to_numpy(),predicted[0])*100
        f1 = f1_score(test['truth'].to_numpy(),predicted[0], average='macro')
        print("Accuracy: {}\nMacro F1-score: {}".format(acc, f1))
        return acc,f1