% 
% fig_12_complex.m
%
% make figure demonstrating complex dynamics
%
% marmaduke 15/05/2012
%

% loose idea behind this one: 3 primitive actions represented by three
% fast sequences, 6 structural sequences for each permutation of the 
% three actions, and a metasequence to coordinate structural seqs. 
% competition in meta level driven by action-sequence performance should
% yield a primitive architecture that finds the right action seq.

%% setup network pieces

% sequence templates
s1 = 2*(ones(6) - eye(6)) + G_seq(ones(6, 1))*0.3;
s2 = 2*(ones(3) - eye(3)) + G_seq(ones(3, 1))*0.8;
s3 = 2*(ones(3) - eye(3)) + G_seq([1 1 1])*3;

% put together skeleton
Gts = {s1, s2, s2, s2, s2, s2, s2, s3, s3, s3};
Gt = G_cat(Gts{:});

% wire pieces together
Gt(6+1:6+6*3, 1:6) = -3;
Gt(6+6*3+1:end, 6+1:6+6*3) = -3;
seqs = perms(1:3);
for ii=1:6
    Gt(3*(ii-1)+1 + 6:3*ii + 6, ii) = 2.;
    for jj=1:3
        target = (seqs(ii, jj)-1)*3 + 1;
        Gt(6+6*3+target:6+6*3+target+2, 6+(ii-1)*3+jj) = 2.;
    end
end
  
n_modes = sum(cellfun(@(A) size(A, 1), Gts));
Its = zeros(n_modes, 1);

% compile templates to full network
n_per_mode = 1;
ns = netsfm_init(n_modes*n_per_mode);
ns.G = G_dist(Gt, n_per_mode, 0.3);
ns.I = I_dist(Its, n_per_mode, 0.3);
ns.n
%subplot 121, imshow(ns.G, []), axis normal

%% run and plot simulation

ns = netsfm_cont(ns, 10000);

%subplot 122, 
plot(ns.ys(ns.n+1:end, 50:10:end)')
