function G = G_seq(mu)
%
% G = G_seq(mu)
%
%   creates a connectivity matrix corresponding, typically, to sequential
%   dynamics, with a sequence of asymmetries around 0, equal to the values
%   of the mu vector.
%
%   marmaduke 15/05/2012
%

n = length(mu);
G = zeros(n);

for ii=1:n
    % matlab indexing is unhealthy for python/C programmers
    if ii+1 == n, from=n; elseif ii==n, from=1; else from=ii+1; end
    G(ii, from) = mu(ii);
    G(from, ii) = -mu(ii);
end
