imagefiles = dir('C:\Users\Kent\Desktop\Kent\Projects\Thea\tests\imageOutputs\*.jpg');      
nfiles = length(imagefiles);    % Number of files found
im = im2double(imread('C:\Users\Kent\Desktop\Kent\Projects\Thea\region_8_3.jpg'));
rmin = 30;
rmax = 100;

for ii=1:nfiles
   try
    currentfilename = strcat('C:\Users\Kent\Desktop\Kent\Projects\Thea\tests\imageOutputs\',imagefiles(ii).name);
    %currentimage = imread(currentfilename);
    [ci,cp,o]=thresh(currentfilename,rmin,rmax);
   catch
       
   end
   display(ii)
end
% [ci,cp,o]=thresh('C:\Users\Kent\Desktop\Kent\Projects\Thea\tests\imageOutputs\me2.JPG.jpg',rmin,rmax)


