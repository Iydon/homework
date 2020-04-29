if isempty(pyversion)
    fprintf('此问题为非数值，使用 MATLAB 可能不是很合适，所以使用较为熟悉的 Python 进行合理的封装。');
    fprintf('如果您能看到这些信息，说明您的 MATLAB 无法调用 Python 程序，请先进行相应的配置。');
end

dir_name = 'data';
verbose = false;

number = length({dir(dir_name).name}) - 2;  % . and ..
[File, Size] = deal(string(NaN(number, 1)));
Time = zeros(number, 1);
for ith = 1: number
    % Paint, cKey, rKey
    file_name = fullfile(dir_name, [num2str(ith),'.mat']);
    load(file_name);
    % calculate and time it
    [result, time] = python_api(rKey, cKey);
    % record and display
    File(ith) = string(file_name);
    Size(ith) = sprintf('%dx%d', size(Paint));
    Time(ith) = time;
    if verbose
        fprintf('Data path (%dx%d): %s\n', size(Paint), file_name);
        fprintf('Is corrected? %d\n', ~sum(sum(result ~= Paint)));
        fprintf('Elapsed time is %.3f seconds.\n', time);
        fprintf('\n');
    end
end
Records = table(File, Size, Time);
disp(Records);


function [Paint, time] = python_api(row, col)
    % call api
    api = py.importlib.import_module('main');
    % py.importlib.reload(api);
    tic;
    Tuple = api.matlab_api(row, col);
    time = toc;
    % convert python object to matlab matrix
    Paint = zeros(length(row), length(col));
    for ith = 1: length(row)
        Paint(ith, :) = Tuple{ith};
    end
end
