function timescale_invariance_asset_path(S0, mu, sigma, ends, point_number, path_number)
	%{
		Compute and plot `path_number` asset paths for the given `S0`, `mu`, and `sigma`,
		at `numpoint_numberber` equally spaced time points in [0, `end`] for `end` in `ends`.

		Argument
		--------
		S0: double
		mu: double
		sigma: double
		ends: matrix_{1xn}, denote n subplots
		point_number: integer, number of points in interval
		path_number: integer, number of paths

		Return
		------
		None, but plot a figure of subplots.

		Example
		-------
		>>> S0=1; mu=0.05; sigma=0.5; ends=[1,0.1,0.01]; point_number=100; path_number=10;
		>>> timescale_invariance_asset_path(S0, mu, sigma, ends, point_number, path_number)
	%}

	if nargin<6, path_number=10; end
	if nargin<5, point_number=100; end
	if nargin<4, ends=[1, 0.1]; end
	if nargin<3, sigma=0.5; end
	if nargin<2, mu=0.05; end
	if nargin<1, S0=1; end

	figure;
	suptitle(['S_0:', num2str(S0), '; \mu:', num2str(mu), '; \sigma:', num2str(sigma)]);

	for i = 1 : length(ends)
		subplot(length(ends), 1, i);
		dt = ends(i) / point_number;
		t = linspace(0, ends(i), point_number);
		S = S0*cumprod( ...
			exp( ...
				(mu-sigma^2/2) * dt + ...
				sigma * sqrt(dt) * randn(path_number,point_number) ...
			), 2 ...
		);
		plot(t, S);
	end
end
