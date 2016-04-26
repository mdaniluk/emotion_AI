
# coding: utf-8

# In[2]:

import pandas as pd

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import tsne
from sklearn.manifold import TSNE
import numpy as np

# In[3]:

path1='features_total_moins1_2.csv'


# In[4]:

features = pd.read_csv(path1)


# In[5]:

#generate dataframe with all the datas
winning_points=pd.DataFrame(columns=features.columns)
losing_points=pd.DataFrame(columns=features.columns)
winning_points_michal=pd.DataFrame(columns=features.columns)
winning_points_thomas=pd.DataFrame(columns=features.columns)
losing_points_michal=pd.DataFrame(columns=features.columns)
losing_points_thomas=pd.DataFrame(columns=features.columns)
for i in range(len(features)-1):
    element=features[features['id']==i+1]
    if element.empty==False:
        if element['winner'].values[0]==1:       
            winning_points.loc[len(winning_points)]=element.values[0]
            if element['player'].values[0]=='michal':
                winning_points_michal.loc[len(winning_points_michal)]=element.values[0]
            else:
                winning_points_thomas.loc[len(winning_points_thomas)]=element.values[0]
        else:
            losing_points.loc[len(losing_points)]=element.values[0]
            if element['player'].values[0]=='michal':
                losing_points_michal.loc[len(losing_points_michal)]=element.values[0]
            else:
                losing_points_thomas.loc[len(losing_points_thomas)]=element.values[0]
        


# In[33]:

#defining X=features
X = winning_points.copy()
X = X.drop('id',1)
X=X.drop('winner',1)
X=X.drop('player',1)
#X = X.drop('Match',1)
#X = X.drop('winner',1)
#defining X=label (1=won,0=lost)
Y = features['winner']


# In[40]:

#defining estimator: number of clusters:4 if winner (want to imprive, happy, excited, doesnt care), 3 if loser (frustrated, 
#doesnt care, annoyed)
est = KMeans(n_clusters=3)
est.fit(X.values)
labels = est.labels_

# In[41]:

labels
print(labels)


# In[31]:

colors = ['r' if d == 0 else 'y' if d==1 else  'b' for d in labels]
pca = PCA(n_components=2)
Y=pca.fit(X).transform(X)
#Y = tsne.bh_sne(X)
plt.scatter(Y[:,0], Y[:,1], c=colors)
plt.show()


## In[32]:
#
columns=['id','cluster']
points_cluster=pd.DataFrame(columns=columns)
for i in range(len(X)):
    points_cluster.loc[len(points_cluster)]=[losing_points.loc[i]['id'],labels[i]]
points_cluster.to_csv('winning_points')
#    

## In[57]:
#--------Working on validation
#
print('importing validation set')
validation_set = pd.read_csv('validation_set_moins1_2.csv')
print('imported')
##build label by majority of vote
majority_label_losing=pd.DataFrame(columns=['id','majority_label'])
majority_label_winning=pd.DataFrame(columns=['id','majority_label'])
majority_label_losing_thomas=pd.DataFrame(columns=['id','majority_label'])
majority_label_losing_michal=pd.DataFrame(columns=['id','majority_label'])
majority_label_winning_thomas=pd.DataFrame(columns=['id','majority_label'])
majority_label_winning_michal=pd.DataFrame(columns=['id','majority_label'])
#
validation_set_losing=validation_set[validation_set['winner']==0]
validation_set_winning=validation_set[validation_set['winner']==1]
#
#
#
#
score={}
#
for i in range(len(validation_set)):
    score[0]=0
    score[1]=0
    score[2]=0
    score[3]=0
    score[validation_set.loc[i]['thomas']]+=1
 
    score[validation_set.loc[i]['michal']]+=1
    
    score[validation_set.loc[i]['hipo']]+=1
    max=0
    index=0
    for j in range(4):
        if score[j]>max: 
            index=j
            max=score[j]
           
    if validation_set.loc[i]['winner']==1:
        majority_label_winning.loc[len(majority_label_winning)]=[validation_set.loc[i]['id'],index]
        if validation_set.loc[i]['player']=='michal':
            majority_label_winning_michal.loc[len(majority_label_winning_michal)]=[validation_set.loc[i]['id'],index]
        else:
            majority_label_winning_thomas.loc[len(majority_label_winning_thomas)]=[validation_set.loc[i]['id'],index]
    else:
        majority_label_losing.loc[len(majority_label_losing)]=[validation_set.loc[i]['id'],index]
        if validation_set.loc[i]['player']=='michal':
            majority_label_losing_michal.loc[len(majority_label_losing_michal)]=[validation_set.loc[i]['id'],index]
        else:
            majority_label_losing_thomas.loc[len(majority_label_losing_thomas)]=[validation_set.loc[i]['id'],index]
        
#            
#
##defining X=features
X_validation = validation_set_winning.copy()
X_validation = X_validation.drop('id',1)
X_validation=X_validation.drop('winner',1)
X_validation=X_validation.drop('player',1)
X_validation=X_validation.drop('michal',1)
X_validation=X_validation.drop('thomas',1)
X_validation=X_validation.drop('hipo',1)

#
true_labels=majority_label_winning['majority_label']
print(len(true_labels))
## In[ ]:
#
colors = ['r' if d == 1 else 'y' if d==2 else 'b' for d in true_labels.values]
pca = PCA(n_components=2)
Y=pca.fit(X_validation).transform(X_validation)
#Y = tsne.bh_sne(X)
plt.scatter(Y[:,0], Y[:,1], c=colors)
plt.show()
#
## In[ ]:
#
our_Kmeans_labels=labels[-62:]
print(our_Kmeans_labels)
colors = ['r' if d == 0 else 'y' if d==1 else 'b' for d in our_Kmeans_labels]
plt.scatter(Y[:,0], Y[:,1], c=colors)
plt.show()

#building confusion matrix
confusion_matrix=np.zeros((3,3))

for i in range(len(true_labels)):
    print(our_Kmeans_labels[i])
    if true_labels[i]==2:
         confusion_matrix[2,our_Kmeans_labels[i]]+=1
    elif true_labels[i]==1:
        confusion_matrix[0,our_Kmeans_labels[i]]+=1
    else:
        confusion_matrix[1,our_Kmeans_labels[i]]+=1
    
   
print('confusion_matrix')
print(confusion_matrix)



