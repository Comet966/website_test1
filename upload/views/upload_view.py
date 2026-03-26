import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from upload.models import Image


def upload_image(request):
    """图片上传页面"""
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        name = request.POST.get('name', '')

        if not image_file:
            return JsonResponse({'success': False, 'error': '请选择图片'})

        # 验证文件类型
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
        ext = os.path.splitext(image_file.name)[1].lower().lstrip('.')
        if ext not in allowed_extensions:
            return JsonResponse({'success': False, 'error': '不支持的图片格式'})

        # 验证文件大小 (最大20MB)
        if image_file.size > 20 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': '图片大小不能超过20MB'})

        # 保存图片
        image = Image.objects.create(image=image_file, name=name)

        return JsonResponse({
            'success': True,
            'message': '上传成功',
            'data': {
                'id': image.pk,
                'name': image.name,
                'url': image.image.url,
                'uploaded_at': image.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    return render(request, 'upload/upload.html')


def image_list(request):
    """图片列表"""
    images = Image.objects.all()[:20]
    return render(request, 'upload/list.html', {'images': images})


@csrf_exempt
def api_upload(request):
    """API接口 - 图片上传"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '仅支持POST请求'})

    image_file = request.FILES.get('image')
    name = request.POST.get('name', '')

    if not image_file:
        return JsonResponse({'success': False, 'error': '请选择图片'})

    # 验证文件类型
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    ext = os.path.splitext(image_file.name)[1].lower().lstrip('.')
    if ext not in allowed_extensions:
        return JsonResponse({'success': False, 'error': '不支持的图片格式'})

    # 验证文件大小 (最大10MB)
    if image_file.size > 10 * 1024 * 1024:
        return JsonResponse({'success': False, 'error': '图片大小不能超过10MB'})

    # 保存图片
    image = Image.objects.create(image=image_file, name=name)

    return JsonResponse({
        'success': True,
        'message': '上传成功',
        'data': {
            'id': image.pk,
            'name': image.name,
            'url': image.image.url,
            'uploaded_at': image.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })


def show_images(request):
    """图片展示页面"""
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'upload/show.html', {'images': images})