from django.db import models


class Image(models.Model):
    """图片模型"""
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='图片')
    name = models.CharField(max_length=100, blank=True, verbose_name='图片名称')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        db_table = 'upload_image'
        verbose_name = '图片'
        verbose_name_plural = '图片'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.name or f'Image {self.pk}'