data {
   int N_GUIDES;
   int N_CELLS;
   real<lower=0,upper=1> G[N_GUIDES][N_CELLS]; // P(guide present)
   int Y[N_CELLS]; // RNA counts
   real L[N_CELLS]; // Normalized library sizes
}
parameters {
   real<lower=0,upper=1> W; // P(guide works)
   real mu; // Mean of NB under null
   real phi; // Dispersion of NB
   real beta; // Effect of enhancer on gene
}
model {
   mu ~ lognormal(?,?); // ???
   phi ~ lognormal(?,?); // ???
   beta ~ lognormal(0,1); // ???
   W ~ beta(1,3); // ???
   for (j in 1:N_CELLS) {
      real log_r=0;
      for(i in 1:N_GUIDES) {
         log_r += log1m_exp(log(G[i][j])+log(W[i]));
      }
      log_r=log1m_exp(log_r);
      Y[j] ~ sum_log_exp(log_r+neg_binomial_2(beta*mu*L[j],phi),
             log1m_exp(r)+neg_binomial_2(mu*L[j],phi));
   }
}
