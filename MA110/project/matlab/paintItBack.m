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
            self.paint(:, jth) = intersection(self, self.paint(:, jth), self.cols{jth});
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
    len = length(origin);
    m = length(choices) + 1;
    n = len - sum(choices) - m + 2;
    count = zeros(1, len);
    total = 0;
    numbers = n_balls_m_boxes(n, m);
    for ith = 1: length(numbers)
        temp = convert_choices_and_expand(choices, numbers{ith});
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
    result = cell(1, nchoosek(n+m-1, m-1));
    ith = 1;
    function nested(n, m, r)
        if m == 1
            result{ith} = r;
            ith = ith + 1;
        else
            for i = 1: n+1
                r(end-m+2) = i-1;
                nested(n-i+1, m-1, r);
            end
        end
    end
    nested(n, m, zeros(1, m-1));
end
