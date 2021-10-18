functions {
   real logP_perturbed(int N_GUIDES,int cell,real[,] G,real[] W) {
      real log_r=0;
      for(i in 1:N_GUIDES)
         log_r += log1m_exp(log(G[i][cell])+log(W[i]));
      log_r=log1m_exp(log_r);
      return log_r;
   }
}
data {
   int N_GUIDES1; // Guides in enhancer 1
   int N_GUIDES2; // Guides in enhancer 2
   int N_CELLS;
   real<lower=0,upper=1> G1[N_GUIDES1,N_CELLS]; // P(guide present, enh1)
   real<lower=0,upper=1> G2[N_GUIDES2,N_CELLS]; // P(guide present, enh2)
   int Y[N_CELLS]; // RNA counts
   real L[N_CELLS]; // Normalized RNA library sizes
}
parameters {
   real<lower=0,upper=1> W1[N_GUIDES1]; // P(guide works, enh1)
   real<lower=0,upper=1> W2[N_GUIDES2]; // P(guide works, enh2)
   real mu; // Mean of NB under null
   real phi; // Dispersion of NB
   real beta1; // Marginal effect, enh1
   real beta2; // Marginal effect, enh2
   real beta12; // Interaction effect
}
model {
   mu ~ lognormal(4,1); // ???
   phi ~ lognormal(1,0.1); // ???
   beta1 ~ lognormal(0,1); // ???
   beta2 ~ lognormal(0,1); // ???
   beta12 ~ lognormal(0,1); // ???
   for(i in 1:N_GUIDES1) W1[i] ~ beta(1,3); // ???
   for(i in 1:N_GUIDES2) W2[i] ~ beta(1,3); // ???
   for (j in 1:N_CELLS) {
      real logP1=logP_perturbed(N_GUIDES1,j,G1,W1);
      real logP2=logP_perturbed(N_GUIDES2,j,G2,W2);
      real notP1=log1m_exp(logP1); real notP2=log1m_exp(logP2);
      real muLj=mu*L[j];
      real array[4]={
         notP1+notP2+neg_binomial_2_lpmf(Y[j]|muLj,phi),
         logP1+notP2+neg_binomial_2_lpmf(Y[j]|muLj*beta1,phi),
         notP1+logP2+neg_binomial_2_lpmf(Y[j]|muLj*beta2,phi),
         logP1+logP2+neg_binomial_2_lpmf(Y[j]|muLj*beta1*beta2*beta12,phi)
      };
      target += log_sum_exp(array);
   }
}
