function [gs, stds] = data_rate_mode
%
% [gs, stds] = data_rate_mode
%
%   Generate data for mode stability figure by simulating a network
%   with various global coupling strengths and computing standard
%   deviation of long time behavior.
%
%   * currently has a bug: std goes to zero around gs=0
%
%   marmaduke 13/05/2012
%

ns = netsfm_init(100);
ns.tw = 100; 
ns.I = 0. + randn(ns.n, 1)/4;
ns.ds = 30;

gs = -0.5:0.005:0.5;
stds = zeros(size(gs));

wbar = waitbar(0, 'Please wait');
tic
for ii=1:length(gs)
    ns.G(:, :) = gs(ii);
    ns_res = netsfm_cont(ns, 2000);
    stds(ii) = std(mean(ns_res.ys(ns.n+1:end, size(ns_res.ys, 2):end), 2));
    waitbar(ii/length(gs), wbar, ['Estimated time left: '...
        num2str(floor(toc * (length(gs) - ii))) ' (s)']); tic;
end

close(wbar)
save('rate_mode.mat', 'gs', 'stds');

    