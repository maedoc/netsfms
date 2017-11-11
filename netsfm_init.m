function ns = netsfm_init(n)
% 
%   ns = netsfm_init(N)
% 
%   Create a struct with all the information necessary to simulate
%   the neural network model.
%
%   input:  n,  number of neurons in the network
%
%   output: ns, struct with network & simulation information 
%
%   marmaduke 13/05/2012

ns = struct('n', n, 'indices', 1:n);

% state
ns.t = 0;
ns.theta = (rand(n, 1) - 0.5)*2*pi;
ns.omega = rand(n, 1);
ns.rmega = ns.omega;

% parameters of network model
ns.G = zeros(n);
ns.I = zeros(n, 1);
ns.tw = 20.0;
ns.k = pi;

% dt is solver timestep, ds is output timestep
ns.dt = 2^-3;
ns.ds = 10;
ns.integrate_reduced = 0;

% simulation output
ns.ts = [0];
ns.ys = [ns.theta; ns.omega];
ns.rs = ns.rmega;
ns.Is = [ns.I];





