dir_name = '../data';
verbose = false;

number = length({dir(dir_name).name}) - 2;  % . and ..
[File, Size] = deal(string(NaN(number, 1)));
[Time, Correct] = deal(zeros(number, 1));
for ith = 1: number
    % Paint, cKey, rKey
    file_name = fullfile(dir_name, [num2str(ith),'.mat']);
    load(file_name);
    for kth = 1: length(rKey)
        if isempty(rKey{kth})
            rKey{kth} = -1;
        end
    end
    for kth = 1: length(cKey)
        if isempty(cKey{kth})
            cKey{kth} = -1;
        end
    end
    % calculate and time it
    tic;
    result = paintItBack(rKey, cKey, 64, 2, -1);
    time = toc;
    % record and display
    File(ith) = string(file_name);
    Size(ith) = sprintf('%dx%d', size(Paint));
    Time(ith) = time;
    Correct(ith) = ~sum(sum(result ~= Paint));
    if verbose
        fprintf('Data path (%s): %s\n', Size(ith), file_name);
        fprintf('Is corrected? %d\n', Correct(ith));
        fprintf('Elapsed time is %.3f seconds.\n', time);
        fprintf('\n');
    end
end
Records = table(File, Size, Time, Correct);
disp(Records);
