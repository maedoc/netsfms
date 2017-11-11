% neural field with network model
% 
% marmaduke 13/05/2012


%% simulate

% construct a neural field with spatial mexican hat kernel and 
% critical spiking excitability
ns = netsfm_init(600);
ns.G = G_mex_hat(ns.n, 50, 2.5);
ns.I = 1 + randn(ns.n, 1)/1000;

% simulate 10 s
ns = netsfm_cont(ns, 6000);


%% plot

figure('units','normalized','outerposition',[0 0 0.95 1])
subplot 211, imshow(ns.ts, 1:ns.n, (ns.ys(1:ns.n,:)+pi)/(2*pi)), axis normal
subplot 245, 
field = sum(ns.ys(ns.n:end-1, 50:end), 1);
mean_field = (field - mean(field))/std(field);
plot(ns.ts(50:end), mean_field);
subplot 246,
f = (1000/(ns.ds*ns.dt))*linspace(0, 1, floor(length(mean_field)/2)); 
mean_spectrum = conv(abs(fft(mean_field)), ones(1, 10), 'same');
loglog(f, mean_spectrum(1:floor(length(mean_field)/2)));
subplot 247
spike_cov = cov(ns.ys(1:ns.n,:)');
imshow(spike_cov, [min(min(spike_cov)) max(max(spike_cov))]), axis normal
subplot 248
[n, xout] = hist(reshape(spike_cov, [], 1), 100);
loglog(xout, n);