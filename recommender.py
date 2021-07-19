import torch
import numpy as np
from torch.autograd import Variable
from tqdm import tqdm_notebook
from main import reccommend

ratings_df = reccommend()

n_users = len(ratings_df.user_id.unique())
n_items = len(ratings_df.beer_id.unique())

class MatrixFactorization(torch.nn.Module):
    def __init__(self, n_users, n_items, n_factors=20):
        super().__init__()
        # create user embeddings
        self.user_factors = torch.nn.Embedding(n_users, n_factors) # think of this as a lookup table for the input.
        # create item embeddings
        self.item_factors = torch.nn.Embedding(n_items, n_factors) # think of this as a lookup table for the input.
        self.user_factors.weight.data.uniform_(0, 0.05)
        self.item_factors.weight.data.uniform_(0, 0.05)
        
    def forward(self, data):
        # matrix multiplication
        users, items = data[:,0], data[:,1]
        return (self.user_factors(users)*self.item_factors(items)).sum(1)
    # def forward(self, user, item):
    # 	# matrix multiplication
    #     return (self.user_factors(user)*self.item_factors(item)).sum(1)
    
    def predict(self, user, item):
        return self.forward(user, item)

# Creating the dataloader (necessary for PyTorch)
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader # package that helps transform your data to machine learning readiness

# Note: This isn't 'good' practice, in a MLops sense but we'll roll with this since the data is already loaded in memory.
class Loader(Dataset):
    def __init__(self):
        self.ratings = ratings_df.copy()
        
        # Extract all user IDs and movie IDs
        users = ratings_df.user_id.unique()  # users IDs
        beers = ratings_df.beer_id.unique()  # beers IDs
        
        #--- Producing new continuous IDs for users and movies ---
        
        # Unique values : index
        self.userid2idx = {o:i for i,o in enumerate(users)}
        self.beerid2idx = {o:i for i,o in enumerate(beers)}
        
        # Obtained continuous ID for users and movies
        self.idx2userid = {i:o for o,i in self.userid2idx.items()}
        self.idx2beerid = {i:o for o,i in self.beerid2idx.items()}
        
        # return the id from the indexed values as noted in the lambda function down below.
        self.ratings.beer_id = ratings_df.beer_id.apply(lambda x: self.beerid2idx[x])
        self.ratings.user_id = ratings_df.user_id.apply(lambda x: self.userid2idx[x])
        
        
        self.x = self.ratings.drop(['rating'], axis=1).values
        self.y = self.ratings['rating'].values
        self.x, self.y = torch.tensor(self.x), torch.tensor(self.y) # Transforms the data to tensors (ready for torch models.)

    def __getitem__(self, index):
        return (self.x[index], self.y[index])

    def __len__(self):
        return len(self.ratings)

    
num_epochs = 128
cuda = torch.cuda.is_available()

print("Is running on GPU:", cuda)

model = MatrixFactorization(n_users, n_items, n_factors=8)
print(model)
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.data)
# GPU enable if you have a GPU...
if cuda:
    model = model.cuda()

# MSE loss
loss_fn = torch.nn.MSELoss()

# ADAM optimizier
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Train data
train_set = Loader()
train_loader = DataLoader(train_set, 128, shuffle=True)

for it in tqdm_notebook(range(num_epochs)):
    losses = []
    for x, y in train_loader:
         if cuda:
            x, y = x.cuda(), y.cuda()
            optimizer.zero_grad()
            outputs = model(x)
            loss = loss_fn(outputs.squeeze(), y.type(torch.float32))
            losses.append(loss.item())
            loss.backward()
            optimizer.step()
    print("iter #{}".format(it), "Loss:", sum(losses) / len(losses))

# By training the model, we will have tuned latent factors for movies and users.
c = 0
uw = 0
iw = 0 
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.data)
        if c == 0:
          uw = param.data
          c +=1
        else:
          iw = param.data
        #print('param_data', param_data)
    
trained_beer_embeddings = model.item_factors.weight.data.cpu().numpy()