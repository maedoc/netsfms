% 
% fig_03_neuron.m
%
% make figure demonstrating aspects of the neuron model used
%
% marmaduke 13/05/2012
%

%% left panel f-i curve

subplot(121)
I_values = 0:0.01:1.1;
sqrt0 = 1 - I_values.^2;
sqrt0(sqrt0<0) = 0;
sqrt0 = sqrt(sqrt0)/(2*pi)*1000;
hold on
plot(I_values, sqrt0, 'k');
xlabel('I(t)'), ylabel('rate (Hz)'), xlim([0, 1.1])
plot([0.5 0.99], 1000*sqrt(1 - [0.5 0.99].^2)/2/pi, 'ko')
ylim([-5 max(sqrt0)+5])

%% right panel, time series

subplot(222)
ns = netsfm_init(1);
ns.ds = 1;
ns.I = 0.5;
ns = netsfm_cont(ns, 20);
hold on
plot(ns.ts, ns.ys(1, :), 'k--');
plot(ns.ts, ns.ys(2, :), 'k');
ylabel('\theta, \omega')
grid on

subplot(224)
ns = netsfm_init(1);
ns.ds = 1;
ns.I = 0.99;
ns = netsfm_cont(ns, 150);
hold on
plot(ns.ts, ns.ys(1, :), 'k--');
plot(ns.ts, ns.ys(2, :), 'k');
grid on
xlabel('time (ms)'), ylabel('\theta, \omega')

%% save fig

print -dpng doc\fig\theta-neuron-flow-ts.png