import numpy as np
import pywt
from PIL import Image
def embed_watermark(image_path, watermark_text):
    # 加载图像
    img = Image.open(image_path).convert('L')  # 转换为灰度图
    img_array = np.array(img)

    # 将水印转换为二进制字符串
    watermark_binary = ''.join(format(ord(i), '08b') for i in watermark_text)
    
    # 进行小波变换
    coeffs = pywt.dwt2(img_array, 'haar')
    LL, (LH, HL, HH) = coeffs
    
    # 嵌入水印到高频系数中
    watermark_length = len(watermark_binary)
    watermark_index = 0
    for row in range(HH.shape[0]):
        for col in range(HH.shape[1]):
            if watermark_index < watermark_length:
                if watermark_binary[watermark_index] == '1':
                    HH[row, col] += 1
                watermark_index += 1
                
    # 反变换得到带水印的图像
    coeffs = (LL, (LH, HL, HH))
    watermarked_image = pywt.idwt2(coeffs, 'haar')
    
    return watermarked_image
def extract_watermark(watermarked_image):
    img_array = np.array(watermarked_image)
    
    # 进行小波变换
    coeffs = pywt.dwt2(img_array, 'haar')
    _, (LH, HL, HH) = coeffs
    
    # 提取水印
    watermark_bits = []
    for row in range(HH.shape[0]):
        for col in range(HH.shape[1]):
            if HH[row, col] % 2 == 1:
                watermark_bits.append('1')
            else:
                watermark_bits.append('0')
                
    # 将二进制字符串转换回文本
    watermark_text = ''
    for i in range(0, len(watermark_bits), 8):
        byte = watermark_bits[i:i+8]
        watermark_text += chr(int(''.join(byte), 2))
    
    return watermark_text.rstrip('\x00')
# 嵌入水印
watermarked_img = embed_watermark('path_to_your_image.jpg', 'YourWatermarkText')

# 保存带水印的图像
Image.fromarray(np.uint8(watermarked_img)).save('watermarked_image.png')

# 提取水印
extracted_watermark = extract_watermark(Image.open('watermarked_image.png'))
print(extracted_watermark)

