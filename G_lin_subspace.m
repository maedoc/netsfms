function G = G_lin_subspace(n, m, sval)
%
% doesn't do what I wanted... 
%
% marmaduke 14/05/2012
%

[Q, R] = qr(rand(n));
[U, S, VT] = svd(Q);
Sd = diag(S);
Sd(m+1:end) = sval;
Sd = diag(Sd);
G = U*Sd*VT';