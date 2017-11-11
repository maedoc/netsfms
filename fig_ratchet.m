% here we try to setup up the simplest rackets

Gt1 = 4*(ones(3) - eye(3));
Gt2 = 3*(ones(3) - eye(3) + G_seq([1 1 0.5])/2.5);

Gts = {Gt1, Gt2, Gt2, Gt2};
Gt = G_cat(Gts{:});


Gt(7:12, 1) = 2.5;
Gt([4:6 10:12], 2) = 2.5; 
Gt(4:9, 3) = 2.5;

Gt(1, 6) = 2; Gt(2, 6) = -1;
Gt(2, 9) = 2; Gt(3, 9) = -1;
Gt(3, 12) = 2; Gt(1, 12) = -1;

Gt(4, 1) = -1/2; Gt(7, 2) = -1/2; Gt(10, 2) = -1/2;

% compile templates to full network
n_modes = sum(cellfun(@(A) size(A, 1), Gts));
n_per_mode = 5;
ns = netsfm_init(n_modes*n_per_mode);
ns.G = G_dist(Gt, n_per_mode, 0.1);
ns.I = I_dist(zeros(n_modes, 1), n_per_mode, 0.1);
ns.omega = I_dist([1 0 0 1 0 0 0 0 0 0 0 0],n_per_mode, 0.);

ns = netsfm_cont(ns, 5000);

subplot 121, imshow(ns.G, []), axis normal
subplot 222, 
imshow(ns.G*ns.ys(ns.n+1:end, :), []), colorbar, axis normal
subplot 224, imshow(ns.ys(ns.n+1:end, :), []), colorbar, axis normal