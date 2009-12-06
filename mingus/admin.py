from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from basic.blog.models import Post
from basic.blog.admin import PostAdmin

class WMDEditor(forms.Textarea):

    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {'class':'vLargeTextField'})
        # if 'cols' not in attrs:
        #     attrs['cols'] = 58
        # if 'rows' not in attrs:
        #     attrs['rows'] = 8
        super(WMDEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        rendered = super(WMDEditor, self).render(name, value, attrs)
        return rendered + mark_safe(u'''
            <div id='wmd-container'>
            <div id='wmd-button-bar'></div>
            <div id='wmd-preview'></div>
            <script type="text/javascript">
            wmd_options = {
                output: "Markdown",
                buttons: "bold italic | link blockquote code image | ol ul"
            };
            </script>
            <script type="text/javascript" src="%sstatic/js/wmd.js"></script>
            </div>''' % settings.MEDIA_URL)
    
class PostForm(forms.ModelForm):
    body = forms.CharField(widget=WMDEditor)
    class Meta:
        model = Post

class WMDPostAdmin(PostAdmin):
    form = PostForm

    class Media:
        css = {
            "all": ("static/css/wmd.css",)
        }
        js = ("static/js/showdown.js",)



admin.site.unregister(Post)

admin.site.register(Post, WMDPostAdmin)