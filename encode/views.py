from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import random


def example(request):
    """图片加密示例页面"""
    return render(request, 'encode/example.html')


@csrf_exempt
def encode_images(request):
    """图片加密处理 - 使用随机噪声图"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '仅支持POST请求'})

    image_a = request.FILES.get('imageA')

    if not image_a:
        return JsonResponse({'success': False, 'error': '请上传图片'})

    try:
        # 打开图片
        img_a = Image.open(image_a)

        # 转换为RGB模式
        if img_a.mode != 'RGB':
            img_a = img_a.convert('RGB')

        # 获取尺寸
        width, height = img_a.size

        # 生成随机彩色噪声图 (密钥)
        key_pixels = []
        for _ in range(width * height):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            key_pixels.append((r, g, b))

        key_image = Image.new('RGB', (width, height))
        key_image.putdata(key_pixels)

        # 获取原图像素
        pixels_a = list(img_a.getdata())

        # 进行XOR运算生成加密图片
        encrypted_data = []
        for i in range(len(pixels_a)):
            pixel_a = pixels_a[i]
            key_pixel = key_pixels[i]

            r = pixel_a[0] ^ key_pixel[0]
            g = pixel_a[1] ^ key_pixel[1]
            b = pixel_a[2] ^ key_pixel[2]

            encrypted_data.append((r, g, b))

        # 创建加密图片
        encrypted_image = Image.new('RGB', (width, height))
        encrypted_image.putdata(encrypted_data)

        # 保存到内存
        key_buffer = io.BytesIO()
        key_image.save(key_buffer, format='PNG')
        key_buffer.seek(0)

        enc_buffer = io.BytesIO()
        encrypted_image.save(enc_buffer, format='PNG')
        enc_buffer.seek(0)

        # 将图片转为base64
        import base64
        key_str = base64.b64encode(key_buffer.getvalue()).decode()
        enc_str = base64.b64encode(enc_buffer.getvalue()).decode()

        return JsonResponse({
            'success': True,
            'message': '加密成功',
            'key_image': f'data:image/png;base64,{key_str}',
            'encrypted_image': f'data:image/png;base64,{enc_str}',
            'width': width,
            'height': height
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'处理失败: {str(e)}'})


@csrf_exempt
def decode_images(request):
    """图片解密处理"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '仅支持POST请求'})

    encrypted_image = request.FILES.get('encryptedImage')
    key_image = request.FILES.get('keyImage')

    if not encrypted_image or not key_image:
        return JsonResponse({'success': False, 'error': '请上传加密图片和密钥图片'})

    try:
        # 打开图片
        img_enc = Image.open(encrypted_image)
        img_key = Image.open(key_image)

        # 转换为RGB模式
        if img_enc.mode != 'RGB':
            img_enc = img_enc.convert('RGB')
        if img_key.mode != 'RGB':
            img_key = img_key.convert('RGB')

        # 获取像素数据
        pixels_enc = list(img_enc.getdata())
        pixels_key = list(img_key.getdata())

        # 进行XOR运算解密
        decrypted_data = []
        for i in range(len(pixels_enc)):
            pixel_enc = pixels_enc[i]
            key_pixel = pixels_key[i]

            r = pixel_enc[0] ^ key_pixel[0]
            g = pixel_enc[1] ^ key_pixel[1]
            b = pixel_enc[2] ^ key_pixel[2]

            decrypted_data.append((r, g, b))

        # 创建解密图片
        width, height = img_enc.size
        decrypted_image = Image.new('RGB', (width, height))
        decrypted_image.putdata(decrypted_data)

        # 保存到内存
        buffer = io.BytesIO()
        decrypted_image.save(buffer, format='PNG')
        buffer.seek(0)

        # 转为base64
        import base64
        dec_str = base64.b64encode(buffer.getvalue()).decode()

        return JsonResponse({
            'success': True,
            'message': '解密成功',
            'decrypted_image': f'data:image/png;base64,{dec_str}'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'处理失败: {str(e)}'})