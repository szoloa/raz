from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
import torch

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("fill-mask", model="google-bert/bert-base-chinese")

# 1. 数据集类，适应中文处理
class MyDataset(Dataset):
    def __init__(self, words, labels, tokenizer, max_len):
        self.words = words
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.words)

    def __getitem__(self, idx):
        word = self.words[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            word,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

# 2. 加载预训练的BERT中文模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)


w = []
v = []

# 读取 outputfile.txt 文件，获取词汇和标签
w = []
v = []

with open('outputfile.txt', encoding='utf-8') as f:
    for i in f.readlines():
        seq = i.strip().split()  # 使用 strip 去掉换行符
        w.append(seq[0])         # 词汇列表
        v.append(int(seq[1]))    # 标签列表

# 读取 data.txt 文件，获取有用的词汇
useful = []
with open('data.txt', encoding='utf-8') as f:
    useful = [line.strip() for line in f.readlines()]  # 去掉每行的换行符

# 准备数据：将 useful 和 w 中的词汇合并
words = useful + w

# 准备标签：为 useful 中的词汇分配标签 (比如有用的词为 1，无用的词为 0，或根据你的实际逻辑)
# 假设 useful 中的词汇默认是有价值的，标签为 1，outputfile 中的 v 标签已定义
labels = [1] * len(useful) + v  # useful 里的所有词设为 1，加上 outputfile.txt 里的标签 v




dataset = MyDataset(words, labels, tokenizer, max_len=10)
dataloader = DataLoader(dataset, batch_size=2)

# 4. 训练模型
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

for epoch in range(3):  # 多次迭代
    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['label']
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

# 5. 模型评估（略）
