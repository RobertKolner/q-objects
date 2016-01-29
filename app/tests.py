from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.test import TestCase


class QTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('user')
        user.groups.add(Group.objects.create(name='group1'))
        user.groups.add(Group.objects.create(name='group2'))

    def test_setup(self):
        q1 = Q(groups__pk=1)
        q2 = Q(groups__pk=2)

        query_simple = q1 & q2
        query_neg = ~(~q1 | ~q2)

        def count(query):
            return User.objects.filter(query).distinct().count()

        # This fails with AssertionError: 0 != 1
        self.assertEqual(count(query_simple), count(query_neg))
