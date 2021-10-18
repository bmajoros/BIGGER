//==================================================================
// Single-cell ATAC+RNA model
// Bill Majoros - bmajoros@alumni.duke.edu 10/18/2021
//
// Library sizes should be normalized by the mean library size.
// Overall effect of enhancer on gene is beta*gamma.
//==================================================================
data {
   int N_GUIDES;         // Number of guides targeting this enhancer
   int N_CELLS;          // Total number of cells
   real<lower=0,upper=1> G[N_GUIDES,N_CELLS]; // P(guide present)
   int Y[N_CELLS];       // RNA counts
   real L_RNA[N_CELLS];  // Normalized library sizes for RNA
   real L_ATAC[N_CELLS]; // Normalized library sizes for ATAC
   int A[N_CELLS];       // ATAC counts
}
parameters {
   real muATAC;  // Mean of NB under null
   real phiATAC; // Dispersion of NB
   real gamma;   // Effect of guides on accessibility
   real<lower=0,upper=1> W[N_GUIDES]; // P(guide works)
   real muRNA;   // Mean of NB under null
   real phiRNA;  // Dispersion of NB
   real beta;    // Effect of enhancer on gene
}
model {
   // Priors: ATAC
   muATAC ~ lognormal(4,0.1); // ???
   phiATAC ~ lognormal(1,0.1); // ???
   gamma ~ lognormal(0,1); // ???

   // Priors: RNA
   muRNA ~ lognormal(4,1); // ???
   phiRNA ~ lognormal(1,0.1); // ???
   beta ~ lognormal(0,1); // ???

   // Prior: guide works
   for(i in 1:N_GUIDES) W[i] ~ beta(1,3); // ???

   // Likelihoods:
   for (j in 1:N_CELLS) {
      // Likelihood of ATAC data:
      real log_r=0;
      for(i in 1:N_GUIDES)
         log_r += log1m_exp(log(G[i][j])+log(W[i]));
      log_r=log1m_exp(log_r);
      target += log_sum_exp(log_r+
         neg_binomial_2_lpmf(A[j]|muATAC*L_ATAC[j]*gamma,phiATAC),
	 log1m_exp(log_r)+neg_binomial_2_lpmf(A[j]|muATAC*L_ATAC[j],phiATAC));

      // Likelihood of RNA data:
      Y[j] ~ neg_binomial_2(muRNA*L_RNA[j]*beta*gamma,phiRNA);
   }
}
