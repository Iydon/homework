function Paint = python_api(row, col)
    % load api from model
    model = py.importlib.import_module('model');
    % py.importlib.reload(model);
    Tuple = model.matlab_api(row, col);
    % convert python object to matlab matrix
    Paint = zeros(length(row), length(col));
    for ith = 1: length(row)
        Paint(ith, :) = Tuple{ith};
    end
end
