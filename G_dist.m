function Gd = G_dist(Gt, N, sig)
%
% Gd = G_dist(Gt, n, sig)
%
%   creates a new connectivity matrix, Gd, which contains a distributed
%   connectivity based on the template connectivity, Gt, where each weight
%   Gt(i, j) is replaced by Gt(i, j)*(1 + randn(N)*sig)/N
%
%   If the given N is negative, the absolute value is used, and the
%   matrices will be plotted automatically for viewing.
%
%   marmaduke 15/05/2012
%

if N<0
    plot_matrices = 1;
    N = -N;
else
    plot_matrices = 0;
end

Gd = zeros(N*size(Gt));

for ii=1:size(Gt, 1)
    for jj=1:size(Gt, 2)
                
        Gd(N*(ii-1)+1:N*ii, N*(jj-1)+1:N*jj) = ...
            Gt(ii, jj)*(1 + randn(N)*sig)/N;
        
    end
end

if plot_matrices
    subplot 121, imshow(Gt) 
    subplot 122, imshow(Gd/max(max(Gd)))
end
