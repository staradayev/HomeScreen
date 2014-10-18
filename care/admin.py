#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.contrib import admin
from care.models import Tag, Category, Picture

class TagAdmin(admin.ModelAdmin):
	list_display = ('tag_name', 'date_pub', 'approve_status')

admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category_name', 'date_pub', 'approve_status')

admin.site.register(Category, CategoryAdmin)

class PictureAdmin(admin.ModelAdmin):
	list_display = ('picture_name', 'date_pub', 'approve_status')

admin.site.register(Picture, PictureAdmin)
