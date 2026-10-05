"""Figura explicativa del ajuste completo; nunca sustituye las métricas OOF."""
from pathlib import Path
import csv,json,warnings
import numpy as np
import Orange
from Orange.data import Table,Domain
from Orange.classification import LogisticRegressionLearner,Model
from Orange.preprocess import Continuize,Normalize,RemoveNaNColumns,SklImpute
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore',message="'penalty' was deprecated.*",category=FutureWarning)
warnings.filterwarnings('ignore',message="'n_jobs' has no effect.*",category=FutureWarning)
BASE=Path(__file__).resolve().parent
data=Table(str(BASE/'datos/wdbc_texture_mean.tab'))
learner=LogisticRegressionLearner(penalty='l2',C=1,class_weight=None,random_state=42,max_iter=1000,preprocessors=[Continuize(),Normalize(),RemoveNaNColumns(),SklImpute()])
model=learner(data)
positive=data.domain.class_var.values.index('M')
p=model(data,Model.Probs)[:,positive]
x=np.linspace(data.X[:,0].min(),data.X[:,0].max(),400)
grid=Table.from_numpy(Domain(data.domain.attributes,data.domain.class_var),x.reshape(-1,1),np.zeros(len(x)))
q=model(grid,Model.Probs)[:,positive]
z=np.log(q/(1-q))
assert np.allclose(1/(1+np.exp(-z)),q)
for name,headers,rows in [('curva_ajuste_completo.csv',['texture_mean','logit_z_full_fit','p_M_full_fit'],zip(x,z,q)),('observaciones_ajuste_completo.csv',['row_id','texture_mean','diagnosis_observed_binary','p_M_full_fit'],zip(range(1,len(data)+1),data.X[:,0],(data.Y==positive).astype(int),p))]:
 with (BASE/name).open('w',newline='') as stream:
  writer=csv.writer(stream,lineterminator='\n'); writer.writerow(headers); writer.writerows(rows)
fig,ax=plt.subplots(figsize=(8.4,3.7))
for cls,color in [('B','#257584'),('M','#a53b4d')]:
 ix=data.Y==data.domain.class_var.values.index(cls)
 ax.scatter(data.X[ix,0],(data.Y[ix]==positive).astype(int),s=13,alpha=.24,label=f'Diagnóstico observado {cls}',color=color)
ax.plot(x,q,color='#352b70',lw=2.2,label='Probabilidad M, ajuste completo')
ax.axhline(.5,ls='--',color='#777',lw=.8)
ax.set(xlabel='texture_mean (variable observada)',ylabel='Diagnóstico / probabilidad M',ylim=(-.1,1.1),yticks=[0,.5,1],title='Datos reales (B=0, M=1) y curva del modelo')
ax.legend(loc='center left',fontsize=8)
fig.tight_layout(); fig.savefig(BASE/'evidencias/curva_explicativa.png',dpi=180); plt.close(fig)
print('Exportada curva de ajuste completo y observaciones; métricas OOF independientes.')
