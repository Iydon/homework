function paint = paintItBack(rows, cols, threshold, scale, steps)
    %{
    Argument:
        - row: cell[vector]
        - col: cell[vector]
        - threshold: int
        - scale: int
        - steps: int
    %}
    % check arguments
    if nargin<5, steps=-1; end
    if nargin<4, scale=2; end
    if nargin<3, threshold=64; end
    % initialize values
    [n_rows, n_cols] = deal(length(rows), length(cols));
    self = struct( ...
        'rows', {rows}, ...
        'cols', {cols}, ...
        'n_rows', n_rows, ...
        'n_cols', n_cols, ...
        'iths', true(1, n_rows), ...
        'jths', true(1, n_cols), ...
        'threshold', threshold, ...
        'scale', scale, ...
        'steps', steps, ...
        'paint', -ones(n_rows, n_cols) ...
    );
    % return value
    self = doit(self);
    paint = self.paint;
end

function self = doit(self)
    previous_hash = 0;
    while self.steps ~= 0
        self.steps = self.steps - 1;
        current_hash = sum(sum(self.paint));
        % fill by rows and columns
        for ith = 1: self.n_rows
            if self.iths(ith)
                self.paint(ith, :) = intersection(self, self.paint(ith, :), self.rows{ith});
                if all(self.paint(ith, :)>-1)
                    self.iths(ith) = false;
                end
            end
        end
        for jth = 1: self.n_cols
            if self.jths(jth)
                self.paint(:, jth) = intersection(self, self.paint(:, jth)', self.cols{jth});
                if all(self.paint(:, jth)>-1)
                    self.jths(jth) = false;
                end
            end
        end
        % check whether the paint is finished
        if all(all(self.paint>-1))
            break
        end
        % check whether the paint is changed
        if current_hash == previous_hash
            self.threshold = self.scale * self.threshold;
        end
        previous_hash = current_hash;
    end
end

function origin = intersection(self, origin, choices)
    if choices(1) < 0  % isempty(choices)
        return;
    end
    len = length(origin);
    m = length(choices) + 1;
    n = len - sum(choices) - m + 2;
    count = zeros(1, len);
    total = 0;
    number = nchoosek(n+m-1, m-1);
    if number > self.threshold
        return;
    end
    numbers = n_balls_m_boxes(n, m);
    for ith = 1: number
        temp = convert_choices_and_expand(choices, numbers(ith, :));
        pmet = true(1, len);
        pmet(temp) = false;
        if all(origin(temp)~=0) && all(origin(pmet)~=1)
            if total > self.threshold
                return;
            end
            total = total + 1;
            count(temp) = count(temp) + 1;
        end
    end
    origin(count==total) = 1;
    origin(count==0) = 0;
end

function result = convert_choices_and_expand(choices, numbers)
    result = zeros(1, sum(choices));
    ith = 0;
    jth = 1;
    for kth = 1: length(choices)
        ith = ith + numbers(kth) + 1;
        result(jth: jth+choices(kth)-1) = ith: ith+choices(kth)-1;
        ith = ith + choices(kth);
        jth = jth + choices(kth);
    end
end

function result = n_balls_m_boxes(n, m)
    global ITH_GLOBAL;
    ITH_GLOBAL = 1;
    number = nchoosek(n+m-1, m-1);
    result = zeros(number, m-1);
    result = nested(n, m, zeros(1, m-1), result);
end

function result = nested(n, m, r, result)
    global ITH_GLOBAL;
    if m == 1
        result(ITH_GLOBAL, :) = r;
        ITH_GLOBAL = ITH_GLOBAL + 1;
    else
        for jth = 1: n+1
            r(end-m+2) = jth-1;
            result = nested(n-jth+1, m-1, r, result);
        end
    end
end
