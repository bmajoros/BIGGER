data {
   int N_GUIDES;
   int N_CELLS;
   real<lower=0,upper=1> G[N_GUIDES,N_CELLS]; // P(guide present)
   int Y[N_CELLS]; // RNA counts
   real L[N_CELLS]; // Normalized library sizes
}
parameters {
   real<lower=0,upper=1> W[N_GUIDES]; // P(guide works)
   real mu; // Mean of NB under null
   real phi; // Dispersion of NB
   real beta; // Effect of enhancer on gene
}
model {
   mu ~ lognormal(4,1); // ???
   phi ~ lognormal(1,0.1); // ???
   beta ~ lognormal(0,1); // ???
   for(i in 1:N_GUIDES) W[i] ~ beta(1,3); // ???
   for (j in 1:N_CELLS) {
      real log_r=0;
      for(i in 1:N_GUIDES) {
         log_r += log1m_exp(log(G[i][j])+log(W[i]));
      }
      log_r=log1m_exp(log_r);
      target += log_sum_exp(log_r+neg_binomial_2_lpmf(Y[j]|mu*L[j]*beta,phi),
                log1m_exp(log_r)+neg_binomial_2_lpmf(Y[j]|mu*L[j],phi));
   }
}

