function a = idst2(arg1,mrows,ncols)
%Idst2 2-D inverse discrete cosine transform.
%   B = Idst2(A) returns the two-dimensional inverse discrete
%   cosine transform of A.
%
%   B = Idst2(A,[M N]) or B = Idst2(A,M,N) pads A with zeros (or
%   truncates A) to create a matrix of size M-by-N before
%   transforming. 
%
%   For any A, Idst2(dst2(A)) equals A to within roundoff error.
%
%   The discrete cosine transform is often used for image
%   compression applications.
%
%   Class Support
%   -------------
%   The input matrix A can be of class double or of any
%   numeric class. The output matrix B is of class double.
%
%   References:
%   -----------
%   [1] A. K. Jain, "Fundamentals of Digital Image
%       Processing", pp. 150-153.
%   [2] Wallace, "The JPEG Still Picture Compression Standard",
%       Communications of the ACM, April 1991.
%
%   Example
%   -------
%   % Perform inverse dst on an image.
%       RGB = imread('autumn.tif');
%       I = rgb2gray(RGB);
%       J = dst2(I);
%       imshow(log(abs(J)),[]), colormap(gca,jet), colorbar
%
%   % The commands below set values less than magnitude 10 in the
%   % dst matrix to zero, then reconstruct the image using the
%   % inverse dst function Idst2.
%
%       J(abs(J)<10) = 0;
%       K = idst2(J);
%       figure, imshow(I)
%       figure, imshow(K,[0 255])
%
%   See also dst2, dstMTX, FFT2, IFFT2.

%   Copyright 1992-2018 The MathWorks, Inc.



[m, n] = size(arg1);
% Basic algorithm.
if (nargin == 1),
  if (m > 1) && (n > 1),
    a = idst(idst(arg1).').';
    return;
  else
    mrows = m;
    ncols = n;
  end
end

% Padding for vector input.

b = arg1;
if nargin==2, 
    ncols = mrows(2); 
    mrows = mrows(1); 
end

mpad = mrows; npad = ncols;
if m == 1 && mpad > m, b(2, 1) = 0; m = 2; end
if n == 1 && npad > n, b(1, 2) = 0; n = 2; end
if m == 1, mpad = npad; npad = 1; end   % For row vector.

% Transform.

a = idst(b, mpad);
if m > 1 && n > 1, a = idst(a.', npad).'; end
