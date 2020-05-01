function result = n_balls_m_boxes(n, m)
    global ITH_GLOBAL;
    ITH_GLOBAL = 1;
    result = zeros(nchoosek(n+m-1, m-1), m-1);
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
