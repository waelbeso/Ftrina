#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from report_bug.models import Bug


class BugSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True, max_length=1000,min_length=10)
    img = serializers.CharField(required=False,allow_blank=True,allow_null=True)

    class Meta:
        model = Bug
        fields = ('message','img')