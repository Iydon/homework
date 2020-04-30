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
    n_rows = length(rows);
    n_cols = length(cols);
    self = struct;
    self.rows = rows;
    self.cols = cols;
    self.iths = 1: n_rows;
    self.jths = 1: n_cols;
    self.threshold = threshold;
    self.scale = scale;
    self.steps = steps;
    self.paint = -ones(n_rows, n_cols);
    % return value
    paint = doit(self).paint;
end

function self = doit(self)
    while self.steps ~= 0
        self.steps = self.steps - 1;
        comparison = self.paint;
        for ith = self.iths
            self.paint(ith, :) = intersection(self, self.paint(ith, :), self.rows{ith});
            if all(self.paint(ith, :)>-1)
                self.iths(find(self.iths==ith, 1)) = [];
            end
        end
        for jth = self.jths
            self.paint(:, jth) = intersection(self, self.paint(:, jth)', self.cols{jth});
            if all(self.paint(:, jth)>-1)
                self.jths(find(self.jths==jth, 1)) = [];
            end
        end
        if all(all(self.paint>-1))
            break
        end
        if all(all(self.paint==comparison))
            self.threshold = self.scale * self.threshold;
        end
    end
end

function origin = intersection(self, origin, choices)
    if isempty(choices), return; end
    m = length(choices) + 1;
    n = length(origin) - sum(choices) - m + 2;
    count = zeros(1, length(origin));
    total = 0;
    f = @(ns, m, n) expand(convert_choices(choices, ns, m), n);
    numbers = n_balls_m_boxes(n, m);
    for ith = 1: length(numbers)
        temp = f(numbers{ith}, 2*m-1, length(origin));
        if all((origin==-1) | (origin==temp))
            if total > self.threshold
                return;
            end
            total = total + 1;
            count = count + temp;
        end
    end
    origin(count==0) = 0;
    origin(count==total) = 1;
end

% utilities
function result = expand(marks, number)
    result = zeros(1, number);
    ith = 1;
    for mark = marks
        if mark > 0
            result(ith: ith+mark-1) = 1;
            ith = ith + mark;
        else
            ith = ith - mark;
        end
    end
end

function result = convert_choices(choices, numbers, number)
    result = zeros(1, number);
    result([1, end]) = -numbers([1, end]);
    result(2: 2: end-1) = choices;
    result(3: 2: end-2) = -1 - numbers(2: end-1);
end

function result = n_balls_m_boxes(n, m)
    result = cell(1, nchoosek(n+m-1, m-1));
    ith = 1;
    function nested(n, m, r)
        if m == 1
            r(end) = n;
            result{ith} = r;
            ith = ith + 1;
        else
            for i = 1: n+1
                r(end-m+1) = i-1;
                nested(n-i+1, m-1, r);
            end
        end
    end
    nested(n, m, zeros(1, m));
end
