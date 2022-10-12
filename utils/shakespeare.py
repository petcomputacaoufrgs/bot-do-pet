import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical

torch.device("cpu")

chunk_size = 100
vocab = ['\n', ' ', '!', '$', '&', "'", ',', '-', '.', '3', ':', ';', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
len_buffer_index = 1115394
char2index = {c:i  for i,c in enumerate(vocab)}

def text2index(buffer):
    text_list = []
    for char in buffer:
        text_list.append(char2index[char])
    return text_list

class ShakespeareLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, n_layers):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.embedding_layer = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_size, n_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, h0=None, c0=None):
        x = self.embedding_layer(x)
        if h0 is None or c0 is None:
            out, (hf, cf) = self.lstm(x)
        else:
            out, (hf, cf) = self.lstm(x, (h0, c0))
        out = self.linear(out)
        return out, (hf, cf)


#Hyperparameters and LSTM definition
vocab_size = 65
embedding_dim = 256
hidden_size = 1024
n_layers = 1
loss_fn = nn.CrossEntropyLoss()

shakespeare_lstm = ShakespeareLSTM(vocab_size, embedding_dim, hidden_size, n_layers)
shakespeare_lstm.load_state_dict(torch.load('data/shakespeare_25_cross_entropy.pt', map_location=torch.device('cpu')))

def generate_until_dot_temperature_pedro(sequence, temperature=1.0):
    sequence_fn = text2index(sequence)
    sequence_fn = torch.tensor(sequence_fn).int()
    output_str = []
    hidden = cell = None
    loop = True
    counter = 0
    while(loop):
        with torch.no_grad():
            output, (hidden, cell) = shakespeare_lstm(sequence_fn.unsqueeze(0), hidden, cell)
            last_output = output.squeeze(0)[-1]
            last_output = torch.nn.functional.softmax(last_output / temperature, dim=0)
            if counter == 0:
                last_output[char2index[':']] = 0
                last_output[char2index['\n']] = 0
            elif not (' ' in output_str):
                last_output[char2index[':']] = 0
                last_output[char2index['\n']] = 0
            categorial_output = Categorical(last_output)
            char_index = categorial_output.sample()
            char = vocab[char_index.item()]
            output_str.append(char)
            sequence_fn = char_index.unsqueeze(0)
            counter += 1
            if char == ":" or char == "\n" or (char.isupper() == False and char != ' '):
                if " " in output_str:
                    return f"{sequence+''.join([char for char in output_str])}"
                else:
                    return ""

def generate_until_dot_temperature(sequence, temperature=1.0):
    sequence_fn = text2index(sequence)
    sequence_fn = torch.tensor(sequence_fn).int()
    output_str = []
    hidden = cell = None
    loop = True
    while(loop):
        with torch.no_grad():
            output, (hidden, cell) = shakespeare_lstm(sequence_fn.unsqueeze(0), hidden, cell)
            last_output = output.squeeze(0)[-1]
            last_output = torch.nn.functional.softmax(last_output / temperature, dim=0)
            categorial_output = Categorical(last_output)
            char_index = categorial_output.sample()
            char = vocab[char_index.item()]
            if char in '.?!--' and len(output_str) > 2:
                loop = False
            output_str.append(char)
            sequence_fn = char_index.unsqueeze(0)
    return (sequence+''.join([char for char in output_str]))