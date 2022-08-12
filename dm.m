%imshow(psf, [,])

f = log(abs(fftshift(fft2(psf)))+1);

%imshow(f, []);

pol = ImToPolar(f, 0, .8, 300, 50); %rMin, rMax, M, N
%imshow(pol, []);

%plt(mean(pol, 2))
meanpol = mean(pol, 2);
metric = mean(meanpol(10:40));

judp('send',10022,'localhost', cast(num2str(metric), 'int8'))

