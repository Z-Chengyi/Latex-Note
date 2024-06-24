function watermarkedImg = embedWatermark(originalImgPath, watermarkText)
% Load the original image and convert it to grayscale.
originalImg = imread(originalImgPath);
grayImg = rgb2gray(originalImg);

% Perform a discrete wavelet transform on the image using the Haar wavelet.
[cA, cH, cV, cD] = dwt2(double(grayImg), 'haar');

% Convert the watermark text into binary form.
binaryWatermark = dec2bin(uint8(watermarkText), 8) - '0';

% Embed the watermark into the detail coefficients of the DWT.
% Here we use the diagonal detail coefficients (cD).
watermarkLength = numel(binaryWatermark);
watermarkIndex = 1;

% Modify the diagonal detail coefficients based on the watermark bits.
for i = 1:size(cD, 1)
    for j = 1:size(cD, 2)
        if watermarkIndex <= watermarkLength
            if binaryWatermark(watermarkIndex) == 1
                cD(i, j) = cD(i, j) + 1;
            end
            watermarkIndex = watermarkIndex + 1;
        end
    end
end

% Reconstruct the watermarked image from its modified wavelet coefficients.
watermarkedImg = idwt2(cA, cH, cV, cD, 'haar');
end




function extractedWatermark = extractWatermark(watermarkedImg)
% Perform a discrete wavelet transform on the watermarked image.
[cA, cH, cV, cD] = dwt2(double(watermarkedImg), 'haar');

% Extract the watermark from the diagonal detail coefficients.
watermarkBits = mod(cD(:), 2);

% Convert the binary watermark back to text.
% Note that you need to know the length of the original watermark text.
watermarkLength = ...; % Specify the expected length here.
watermarkBits = reshape(watermarkBits, [], watermarkLength);
extractedWatermark = char(bin2dec(dec2bin(watermarkBits + '0')));

% Remove trailing null characters.
extractedWatermark = strtrim(extractedWatermark);
end
