function G = G_cat(varargin)

rows = cellfun(@(A) size(A, 1), varargin);
cols = cellfun(@(A) size(A, 2), varargin);

G = zeros(sum(rows), sum(cols));

row = 1;
col = 1;
for ii=1:length(varargin)
    G(row:row+rows(ii)-1, col:col+cols(ii)-1) = varargin{ii};
    row = row + rows(ii);
    col = col + cols(ii);
end

    