from django.contrib import admin

from .models import (ChildCourse, ChildCoursePreview, ChildCourseReview,
                     ChildLesson, ChildSubunit, ChildUnit)

admin.site.register(ChildCourse)
admin.site.register(ChildLesson)
admin.site.register(ChildUnit)
admin.site.register(ChildSubunit)
admin.site.register(ChildCoursePreview)
admin.site.register(ChildCourseReview)
