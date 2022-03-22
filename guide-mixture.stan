data {
  int<lower=1> N;
  int X[N];
  real L[N];
}
parameters {
  real<lower=0.001> lambda; // Poison rate parameter
  real<lower=0.001,upper=0.999> r;  // Mixture proportion
  real<lower=lambda> nbMean; // neg binomial mean parameter
  real<lower=0.001> nbDisp; // neg binomial dispersion parameter
}
model {
   // Priors:
   r ~ beta(1,10);
   lambda ~ uniform(0,nbMean);
   nbMean ~ lognormal(log(50),log(2));
   nbDisp ~ lognormal(log(5),log(5));

   // Likelihoods:
   for(i in 1:N) {
      real slambda = lambda * L[i];
      real snbDisp = nbDisp;
      real snbMean = nbMean * L[i];
      target+= log_sum_exp(log(1-r)+poisson_lpmf(X[i]|slambda),log(r)+neg_binomial_2_lpmf(X[i]|snbMean,snbDisp))-log_diff_exp(log(1),log_sum_exp((log(1-r)+log(exp(-slambda))),(log(r)+snbDisp*(log(snbDisp)-log_sum_exp(log(snbDisp),log(snbMean))))));
      }
}
generated quantities {
   real<lower=0,upper=1> PZi[N];
   real likeli_poisson[N];
   real likeli_negbin[N];
   real lambdasum=0;
   real nbsum=0;
   for(i in 1:N) {
      real slambda = lambda * L[i];
      real snbDisp = nbDisp; // sqrt(L[i]);
      real snbMean = nbMean * L[i];
      real LP0=log(1-r)+poisson_lpmf(X[i]|slambda);
      real LP1=log(r)+neg_binomial_2_lpmf(X[i]|snbMean,snbDisp);
      PZi[i]=exp(LP1-log_sum_exp(LP0,LP1));
      likeli_poisson[i] = LP0-log(1-r);
      likeli_negbin[i] = LP1-log(r);
   }
}

