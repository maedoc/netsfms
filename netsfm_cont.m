function ns = netsfm_cont(ns, len)
% 
%   ns = netsfm_cont(ns, len)
% 
%   Runs or continues simulation by a specified amount of time.
%
%   input:  ns      struct with network & simulation information
%           len     length of continuation
%
%   output: ns, struct with network & updated simulation information
%
%   marmaduke 12/05/2012

n_steps = floor(len/ns.dt);
n_output = floor(n_steps/ns.ds);

ts = zeros(1, n_output);
ys = zeros(size(ns.ys, 1), n_output);
rs = zeros(size(ns.rs, 1), n_output);
Is = zeros(size(ns.I), n_output);
ii_out = 1;

t = ns.t;
dt = ns.dt;
ds = ns.ds;
theta = ns.theta;
omega = ns.omega;
rmega = ns.rmega;
G = ns.G;
I = ns.I;
tw = ns.tw;
k = ns.k;
n = ns.n;
r_on = ns.integrate_reduced;

for ii=1:n_steps
    
    fired = theta > pi;
    theta(fired) = theta(fired) - 2*pi;
    
    dtheta = 1 + (G*omega + I).*sin(theta);
    domega = -omega + k*fired/dt;
    
    theta = theta + dt*dtheta;
    omega = omega + dt*domega/tw;
    
    if r_on % ns.integrate_reduced
        sqrt0 = 1 - (G*rmega + I).^2;
        sqrt0(sqrt0<0) = 0;
        drmega = -rmega + sqrt0;
        rmega = rmega + dt*drmega/tw;
    end
            
    t = t + dt*1;
    
    theta(theta<-pi) = -pi;
    
    if mod(ii, ds) == 0
        ts(ii_out) = t;
        ys(:, ii_out) = [theta; omega];
        rs(:, ii_out) = rmega;
        ii_out = ii_out + 1;

	% record input pattern
	Is(:, ii_out) = ns.I;
    end
    
end

ns.t = t;
ns.theta = theta;
ns.omega = omega;
ns.ts = [ns.ts ts];
ns.ys = [ns.ys ys];
ns.Is = [ns.Is Is];

if r_on % ns.integrate_reduced
    ns.rs = [ns.rs rs];
    ns.rmega = rmega;
end

