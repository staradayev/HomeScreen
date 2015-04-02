#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.contrib import admin
from care.models import Tag, TagTranslation, Category, CategoryTranslation, Picture, PictureTranslation, Link, UserProfile, Organization, OrganizationTranslation, Download, LinkType, Like 
from multilingual_model.admin import TranslationStackedInline  

class TagTranslationInline(TranslationStackedInline):
   model = TagTranslation

class TagAdmin(admin.ModelAdmin):
	list_display = ('get_name', 'date_pub', 'approve_status')
	inlines = [TagTranslationInline]

	def get_name(self, obj):
		return obj.name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'translations'

admin.site.register(Tag, TagAdmin)

class CategoryTranslationInline(TranslationStackedInline):
   model = CategoryTranslation

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('get_name', 'date_pub', 'approve_status')
	inlines = [CategoryTranslationInline]

	def get_name(self, obj):
		return obj.name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'translations'

admin.site.register(Category, CategoryAdmin)

class PictureTranslationInline(TranslationStackedInline):
   model = PictureTranslation

class PictureAdmin(admin.ModelAdmin):
	list_display = ('admin_thumbnail', 'get_name', 'approve_status')
	readonly_fields = ('admin_image',)
	inlines = [PictureTranslationInline]

	def get_name(self, obj):
		return obj.name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'translations'

admin.site.register(Picture, PictureAdmin)

class LinkAdmin(admin.ModelAdmin):
	list_display = ('get_name', 'link_url')

	def get_name(self, obj):
		return obj.link_type.type_tag
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'translations'

admin.site.register(Link, LinkAdmin)

class LinkTypeAdmin(admin.ModelAdmin):
	list_display = ('get_name', 'date_pub')

	def get_name(self, obj):
		return obj.type_tag
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'translations'

admin.site.register(LinkType, LinkTypeAdmin)

admin.site.register(UserProfile)

class OrganizationTranslationInline(TranslationStackedInline):
   model = OrganizationTranslation

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('get_name', 'date_pub')
	inlines = [OrganizationTranslationInline]

	def get_name(self, obj):
		return obj.name
	get_name.short_description = 'Name'
	get_name.admin_order_field = 'translations'

admin.site.register(Organization, OrganizationAdmin)

class LikeAdmin(admin.ModelAdmin):
	list_display = ('admin_thumbnail', 'photo', 'user')

admin.site.register(Like, LikeAdmin)

class DownloadAdmin(admin.ModelAdmin):
	list_display = ('amount', 't_uuid', 'donator')
	

admin.site.register(Download, DownloadAdmin)



