function G = G_mex_hat(n, width, inhib_div)
% 
%   G = G_mex_hat(n, width, inhib_div)
% 
%   Creates a connectivity matrix with a mexican hat kernel
%
%   marmaduke 13/05/2012

xs = repmat(1:n, [n 1]);
ds = xs - xs';

G = pdf('norm', ds, 0, width) ...
  - pdf('norm', ds, width*2, width)/inhib_div ...
  - pdf('norm', ds, -width*2, width)/inhib_div;
