
s1 = 3*(ones(s1n) - eye(s1n) + G_seq([1 1 1])/3);
s2 = 3*(G_seq([1 1 1])/3);

s2_ = G_dist(s1, 9, 0.3);

G = G_dist(s1, 27, 0.5) + G_cat(s2_, s2_, s2_)*0.;

subplot 121, imshow(G, []), axis square, colorbar

ns = netsfm_init(size(G, 1));
ns.G = G;
ns = netsfm_cont(ns, 2000);

subplot 222, imshow(ns.ys(ns.n+1:end,50:end), []), axis normal, colorbar
subplot 224, imshow(G*ns.ys(ns.n+1:end,50:end), []), axis normal, colorbar
