function dm_callback(src,evt,varargin)
   % in myUserFcn.m somewhere on the matlab path.

   disp(['Got Event: ' evt.EventName]); % prints the event
   disp(src);                           % prints the source object (UserFunctions)
   disp(src.hSI);                       % each source object has access to the main

                                        % ScanImage® Model object
   disp(src.hSI.imagingSystem)          % from which we can access ScanImage
                                        % methods and properties

   image = src.hSI.hDisplay.lastFrame{1};
   
   f = log(abs(fftshift(fft2(image)))+1);
   pol = ImToPolar(f, 0, .8, 300, 50);
   meanpol = mean(pol,2);
   metric = mean(meanpol(10:40));

   judp('SEND', 10022,'localhost', cast(num2str(metric), 'int8'));

end
