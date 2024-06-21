当然，让我们深入探讨之前提供的代码，它是关于利用小波变换（Wavelet Transform）在图像中嵌入和提取数字水印的过程。我们将分步解析：

第一部分：导入必要的库
import numpy as np
import pywt
from PIL import Image
numpy: 数值计算库，用于高效的数据操作。
pywt: Python Wavelets库，用于小波变换。
PIL.Image: Python Imaging Library的一部分，用于图像处理。
第二部分：嵌入水印的函数
函数定义
def embed_watermark(image_path, watermark_text):
接收两个参数：图像路径和要嵌入的水印文本。

图像加载与预处理
img = Image.open(image_path).convert('L')
img_array = np.array(img)
打开图像文件，转换为灰度模式，然后转换成NumPy数组。

水印文本转二进制
watermark_binary = ''.join(format(ord(i), '08b') for i in watermark_text)
将文本转换为其ASCII值对应的二进制形式。

小波分解
coeffs = pywt.dwt2(img_array, 'haar')
LL, (LH, HL, HH) = coeffs
使用Haar小波基对图像进行二维离散小波变换(DWT)，得到四个子带：近似(LL)、水平(LH)、垂直(HL)和对角(HH)细节。

嵌入水印
watermark_length = len(watermark_binary)
watermark_index = 0
for row in range(HH.shape[0]):
    for col in range(HH.shape[1]):
        if watermark_index < watermark_length:
            if watermark_binary[watermark_index] == '1':
                HH[row, col] += 1
            watermark_index += 1
遍历HH子带，根据水印二进制位修改系数值，'1'则增加1，从而嵌入水印。

小波重构
coeffs = (LL, (LH, HL, HH))
watermarked_image = pywt.idwt2(coeffs, 'haar')
使用逆离散小波变换(IDWT)恢复图像，此时图像已含水印。

第三部分：提取水印的函数
图像加载
img_array = np.array(watermarked_image)
直接从带有水印的图像开始。

小波分解
coeffs = pywt.dwt2(img_array, 'haar')
_, (LH, HL, HH) = coeffs
再次进行小波分解。

提取水印
watermark_bits = []
for row in range(HH.shape[0]):
    for col in range(HH.shape[1]):
        if HH[row, col] % 2 == 1:
            watermark_bits.append('1')
        else:
            watermark_bits.append('0')
遍历HH子带，根据系数值的奇偶性判断水印位。

解码水印
watermark_text = ''
for i in range(0, len(watermark_bits), 8):
    byte = watermark_bits[i:i+8]
    watermark_text += chr(int(''.join(byte), 2))
每8个比特构成一个字节，转换为字符，拼接成原始水印文本。

总结
这套流程巧妙地利用了小波变换的局部化性质，在图像的高频区域（通常是边缘和纹理）嵌入水印，而这些变化对于人眼来说往往是不可见的。这种方法既保证了水印的存在又保持了图像的质量，是一种常见的数字水印技术。
