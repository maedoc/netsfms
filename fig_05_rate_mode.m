% 
% fig_05_rate_mode.m
%
% make figure demonstrating firing rate mode formation
%
% formula derived in section 4.1 of Maxima file analytics.wxm
%
% marmaduke 13/05/2012
%

figure(1)
clf

g = -0.5:0.05:0.5; m=20;
%lam = 1-(g.^2.*m.^2.*sqrt(4.*g.^2.*m.^2+4))./((g.^2.*m.^2+1).*...
%    sqrt(4-(g.*m.*sqrt(4.*g.^2.*m.^2+4))./(g.^2.*m.^2+1)));

% ignore I0
lam = - 1 - g.^2*m;

if ~exist('rate_mode.mat'), data_rate_mode, end
data = load('rate_mode.mat');

[ax, h1, h2] = plotyy(g, lam, data.gs, data.stds);
set(get(ax(1), 'Ylabel'), 'String', '\lambda')
set(get(ax(2), 'Ylabel'), 'String', 'std(\omega)')
xlabel('coupling strength')
grid on

print -dpng doc\fig\rate-mode-formation.png
