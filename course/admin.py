from django.contrib import admin

from .models import Course, CoursePreview, CourseReview, Lesson, Subunit, Unit

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Unit)
admin.site.register(Subunit)
admin.site.register(CoursePreview)
admin.site.register(CourseReview)
