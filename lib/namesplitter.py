from sklearn_crfsuite import CRF

import os

class NameSplitter():
    """
    Machine Learning based splitter for usernames.  Uses L-BFGS algo to classify where
    names should be split.

    kwargs --
    model_filename (sklearn_crfsuite "model" filename):
        A custom trained model to use for the name splitter.
    """
    def __init__(self, model_filename=os.path.join(os.path.dirname(__file__), 'model/default_namesplitter')):
        # __splitter is the model that is trained to split names, and will be retrained if precision falls too low.
        self.__splitter = self.__get_splitter(model_filename)

        # __training_list is the current training list, this starts empty, and is added to as the __splitter is retrained.
        self.__training_list = list()

    def tune_with(self, namelist):
        # TODO: Implement tuning if a list of names is given after doing some more research on if it is useful.
        raise NotImplementedError('Tuning has not been implemented, but is being investigated.  If you are interested, please contact the maintainer.')

    def dissect(self, name):
        name = name.replace(' ', '')
        features = self.__name_features(name)
        pred = self.__splitter.predict_single(features)

        parts = list()
        curr = 0

        for i in range(len(pred)):
            if pred[i] == 'yes_split_next':
                parts.append(name[curr:i - curr])

        return parts

    @staticmethod
    def __get_splitter(model_filename):
        if model_filename:
            return CRF(
                algorithm='lbfgs',
                c1=0.1,
                c2=0.1,
                max_iterations=100,
                all_possible_transitions=True,
                model_filename=model_filename
            )

        return CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )

    @staticmethod
    def __char_features(char, i, prefix):
        return {
            prefix + 'lower': char.lower(),
            prefix + 'isupper': char.isupper(),
            prefix + 'isdigit': char.isdigit(),
            prefix + 'islower': char.islower(),
            prefix + 'isalpha': char.isalpha(),
            prefix + 'position': i
        }

    def __get_features(self, name, i):
        char = name[i]

        features = self.__char_features(char, i, '')
        features.update({
            'length': len(name)
        })

        if i == 0:
            features['BON'] = True

        if i == len(name) - 1:
            features['EON'] = True

        for j in range(3):
            if i > j:
                features.update(self.__char_features(name[i - j], i - j, '-' + str(j)))
            if i < len(name) - (j + 1):
                features.update(self.__char_features(name[i + j], i + j, '+' + str(j)))

        return features

    def __name_features(self, name):
        features = list()
        for i in range(len(name)):
            features.append(self.__get_features(name, i))

        return features
