import sys
sys.path.append('..')
import os
import numpy as np

id_to_char = {}
char_to_id = {}

def _update_vocab(txt):
  chars = list(txt)
  
  for i, char in enumerate(chars):
    if char not in char_to_id:
      new_id = len(id_to_char)
      id_to_char[new_id] = char
      char_to_id[char] = new_id


def load_data(file_name='addition.txt', seed=1984):
  file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name
  
  assert os.path.exists(file_path), 'No file: %s' % file_name
  
  questions, answers = [], []
  
  for line in open(file_path, 'r'):
    idx = line.find('_')
    questions.append(line[:idx])
    answers.append(line[idx:-1])
    
  # create vocab dict
  for i in range(len(questions)):
    q, a = questions[i], answers[i]
    _update_vocab(q)
    _update_vocab(a)
    
  # create numpy array
  x = np.zeros((len(questions), len(questions[0])), dtype=int)
  t = np.zeros((len(answers), len(answers[0])), dtype=int)
  
  for i, sentence in enumerate(questions):
    x[i] = [char_to_id[char] for char in list(sentence)]
  for i, sentence in enumerate(answers):
    t[i] = [char_to_id[char] for char in list(sentence)]
    
  # shuffle
  indices = np.arange(len(x))
  if seed is not None:
    np.random.seed(seed)
  np.random.shuffle(indices)
  
  x = x[indices]
  t = t[indices]
  
  # 10% for validation set
  split_at = len(x) - len(x) // 10
  (x_train, x_test) = x[:split_at], x[split_at:]
  (t_train, t_test) = t[:split_at], t[split_at:]
  
  return (x_train, t_train), (x_test, t_test)


def get_vocab():
  return char_to_id, id_to_char