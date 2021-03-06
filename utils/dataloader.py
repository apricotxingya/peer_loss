import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class DataLoader(object):
    def __init__(self, name, args):
        self.name = name
        if name == 'susy':
            self.df = pd.read_csv(f'uci/large/SUSY.csv', header=None)
            self.preprocess_susy()
        if name == 'noisy':
            file = args['noisy_file']
            # print('\n\n#####{}\n'.format(args['noisy_file']))
            self.df = pd.read_csv(file)
        if name == 'higgs':
            self.df = pd.read_csv(f'uci/large/HIGGS.csv', header=None)
            self.preprocess_susy()
        if name == 'heart':
            self.df = pd.read_csv(f'uci/heart.csv')
            self.preprocess_heart()
        elif name == 'breast':
            self.df = pd.read_csv(f'uci/breast-cancer.data', header=None, sep=',')
            self.preprocess_breast()
        elif name == 'breast2':
            self.df = pd.read_csv(f'uci/breast.csv')
            self.preprocess_breast2()
        elif name == 'german':
            self.df = pd.read_csv('uci/german.data', header=None, sep=' ')
            self.preprocess_german()
        elif name == 'banana':
            self.df = pd.read_csv('uci/banana.csv')
        elif name == 'image':
            self.df = pd.read_csv('uci/image.csv')
        elif name == 'titanic':
            self.df = pd.read_csv('uci/titanic.csv')
        elif name == 'thyroid':
            self.df = pd.read_csv('uci/thyroid.csv')
        elif name == 'twonorm':
            self.df = pd.read_csv('uci/twonorm.csv')
        elif name == 'waveform':
            self.df = pd.read_csv('uci/waveform.csv')
        elif name == 'flare-solar':
            self.df = pd.read_csv('uci/flare-solar.csv')
            self.categorical()
        elif name == 'waveform':
            self.df = pd.read_csv('uci/waveform.csv')
        elif name == 'splice':
            self.df = pd.read_csv('uci/splice.csv')
            self.categorical()
        elif name == 'diabetes':
            self.df = pd.read_csv('uci/diabetes.csv')
            self.preprocess_diabetes()

    def load(self, path):
        df = open(path).readlines()
        df = list(map(lambda line: list(map(float, line.split())), df))
        self.df = pd.DataFrame(df)
        return self

    def categorical(self):
        self.df = onehot(self.df, [col for col in self.df.columns if col != 'target'])

    def preprocess_susy(self):
        self.df.rename(columns={0: 'target'}, inplace=True)

    def preprocess_hotel(self):
        self.df.rename(columns={0: 'target'}, inplace=True)

    def preprocess_heart(self):
        self.df = onehot(self.df, ['cp', 'slope', 'thal', 'restecg'])

    def preprocess_german(self):
        self.df.rename(columns={20: 'target'}, inplace=True)
        self.df.target.replace({2: 0}, inplace=True)
        cate_cols = [i for i in self.df.columns if self.df[i].dtype == 'object']
        self.df = onehot(self.df, cate_cols)

    def preprocess_breast(self):
        self.df.rename(columns={0: 'target'}, inplace=True)
        self.df.target.replace({'no-recurrence-events': 0, 'recurrence-events': 1}, inplace=True)
        self.categorical()

    def preprocess_breast2(self):
        self.df.replace({'M': 1, 'B': 0}, inplace=True)
        self.df.rename(columns={'diagnosis': 'target'}, inplace=True)
        self.df.drop(['id', 'Unnamed: 32'], axis=1, inplace=True)

    def preprocess_diabetes(self):
        self.df.rename(columns={'Outcome': 'target'}, inplace=True)

    def equalize_prior(self, target='target'):
        pos = self.df.loc[self.df[target] == 1]
        neg = self.df.loc[self.df[target] == 0]
        n = min(pos.shape[0], neg.shape[0])
        pos = pos.sample(n=n)
        neg = neg.sample(n=n)
        self.df = pd.concat([pos, neg], axis=0)
        return self

    def train_test_split(self, test_size=0.25, normalize=True):
        X = self.df.drop(['target'], axis=1).values
        y = self.df.target.values
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size)
        sc = StandardScaler()
        if normalize:
            self.X_train = sc.fit_transform(self.X_train)
            self.X_test = sc.transform(self.X_test)
        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_test_val_split(self, e0, e1, test_size=0.2, val_size=0.1, normalize=True):
        X = self.df.drop(['target'], axis=1).values
        y = self.df.target.values
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=test_size)
        if normalize:
            sc = StandardScaler()
            self.X_train = sc.fit_transform(self.X_train)
            self.X_test = sc.transform(self.X_test)
        self.X_train, self.X_val, self.y_train, self.y_val = \
            train_test_split(self.X_train, self.y_train, test_size=val_size/(1-test_size))
        self.y_train = make_noisy_data(self.y_train, e0, e1)
        self.y_val = make_noisy_data(self.y_val, e0, e1)
        return self.X_train, self.X_test, self.X_val, self.y_train, self.y_test, self.y_val

    def prepare_train_test(self, kargs):
        if kargs['equalize_prior']:
            self.equalize_prior()
        X_train, X_test, y_train, y_test = self.train_test_split(kargs['test_size'], kargs['normalize'])
        y_noisy = make_noisy_data(y_train, kargs['e0'], kargs['e1'])
        return X_train, X_test, y_noisy, y_test

    def prepare_train_test_val(self, kargs):
        if kargs['equalize_prior']:
            self.equalize_prior()
        X_train, X_test, X_val, y_train, y_test, y_val = self.train_test_val_split(
            e0=kargs['e0'], e1=kargs['e1'],
            test_size=kargs['test_size'],
            val_size=kargs['val_size'],
            normalize=kargs['normalize'],
        )
        return X_train, X_test, X_val, y_train, y_test, y_val


def onehot(df, cols):
    dummies = [pd.get_dummies(df[col]) for col in cols]
    df.drop(cols, axis=1, inplace=True)
    df = pd.concat([df] + dummies, axis=1)
    return df


def make_noisy_data(y, e0, e1):
    num_neg = np.count_nonzero(y == 0)
    num_pos = np.count_nonzero(y == 1)
    flip0 = np.random.choice(np.where(y == 0)[0], int(num_neg * e0), replace=False)
    flip1 = np.random.choice(np.where(y == 1)[0], int(num_pos * e1), replace=False)
    flipped_idxes = np.concatenate([flip0, flip1])
    y_noisy = y.copy()
    y_noisy[flipped_idxes] = 1 - y_noisy[flipped_idxes]
    return y_noisy
