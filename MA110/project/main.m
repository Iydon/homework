for ith = 1: 7
    % Paint, cKey, rKey
    file_name = ['data/', num2str(ith),'.mat'];
    load(file_name);
    % calculate and time
    tic;
    result = python_api(rKey, cKey);
    time = toc;
    fprintf('Data path (%dx%d): %s\n', size(Paint), file_name);
    fprintf('Is corrected? %d\n', ~sum(sum(result ~= Paint)));
    fprintf('Elapsed time is %.3f seconds.\n', time);
    fprintf('\n');
end


function Paint = python_api(row, col)
    % call api
    api = py.importlib.import_module('main');
    % py.importlib.reload(api);
    Tuple = api.matlab_api(row, col);
    % convert python object to matlab matrix
    Paint = zeros(length(row), length(col));
    for ith = 1: length(row)
        Paint(ith, :) = Tuple{ith};
    end
end
