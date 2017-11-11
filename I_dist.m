function Id = I_dist(It, N, sig)
%
% Id = I_dist(I, N, sig)
%
%   creates a stimulation pattern Id that distributes the input stimulation
%   template, It, by N such that Id has length N x length(It). This is
%   analogous to G_dist, but no scaling occurs, of course.
%
%   marmaduke 15/05/2012
%

Id = zeros(length(It)*N, 1);

for ii=1:length(It)
    Id( N*(ii-1)+1:N*ii ) = It(ii) + randn(N,1)*sig;
end
