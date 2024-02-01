import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import pandas as pd

# Carregando o conjunto de dados
df = pd.read_csv('reclamacoes_data.csv')

# Dividindo o conjunto de dados em treino e teste
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Carregando o tokenizer e o modelo BERT para TensorFlow
tokenizer = BertTokenizer.from_pretrained('bert-base-portuguese-cased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-portuguese-cased', num_labels=2)

# Preparando os dados
def tokenize_batch(batch):
    return tokenizer(batch['mensagem'].tolist(), padding=True, truncation=True, max_length=256, return_tensors='tf'), batch['tipo_reclamacao'].tolist()

# Criando um conjunto de dados personalizado
class ReclamacaoDataset(tf.keras.utils.Sequence):
    def __init__(self, dataframe, tokenizer, max_length=128, batch_size=8):
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.batch_size = batch_size

    def __len__(self):
        return len(self.data) // self.batch_size

    def __getitem__(self, idx):
        batch_data = self.data.iloc[idx * self.batch_size:(idx + 1) * self.batch_size]
        inputs, labels = tokenize_batch(batch_data)
        return inputs, tf.constant(labels, dtype=tf.int32)

# Criando instâncias do conjunto de dados
train_dataset = ReclamacaoDataset(train_df, tokenizer)
test_dataset = ReclamacaoDataset(test_df, tokenizer)

# Configurando o otimizador e a função de perda
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# Compilando o modelo
model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])

# Treinando o modelo
model.fit(train_dataset, epochs=3)

# Salvando o modelo
model.save('modelo_bert_reclamacoes')


# Avaliando o modelo no conjunto de teste
predictions = model.predict(test_dataset)
predicted_labels = tf.argmax(predictions.logits, axis=1)
true_labels = tf.concat([label for _, label in test_dataset], axis=0)

# Avaliando a precisão do modelo
accuracy = accuracy_score(true_labels.numpy(), predicted_labels.numpy())
print(f'Acurácia do modelo: {accuracy * 100:.2f}%')
